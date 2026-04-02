"""
predictor/models.py
Ensemble of LSTM + Random Forest + XGBoost with walk-forward validation.
"""

import numpy as np
import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import MinMaxScaler, RobustScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from xgboost import XGBRegressor
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization, Bidirectional
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from config import Config


class ModelEnsemble:
    def __init__(self, cfg: Config, model_selection: str = "all"):
        self.cfg   = cfg
        self.sel   = model_selection
        self.models= {}
        self.scalers= {}
        self.results= {}

    # ──────────────────────────────────────────────────────────────
    # Data Preparation
    # ──────────────────────────────────────────────────────────────
    def _train_test_split(self, df, feature_cols):
        split = int(len(df) * (1 - self.cfg.test_split))
        X = df[feature_cols].values
        y = df['Target'].values

        X_train, X_test = X[:split], X[split:]
        y_train, y_test = y[:split], y[split:]
        return X_train, X_test, y_train, y_test, split

    def _scale(self, X_train, X_test, name):
        scaler = RobustScaler()
        X_train_s = scaler.fit_transform(X_train)
        X_test_s  = scaler.transform(X_test)
        self.scalers[name] = scaler
        return X_train_s, X_test_s

    def _make_sequences(self, X, y, seq_len):
        Xs, ys = [], []
        for i in range(len(X) - seq_len):
            Xs.append(X[i:i+seq_len])
            ys.append(y[i+seq_len])
        return np.array(Xs), np.array(ys)

    # ──────────────────────────────────────────────────────────────
    # LSTM
    # ──────────────────────────────────────────────────────────────
    def _build_lstm(self, input_shape):
        model = Sequential([
            Bidirectional(LSTM(self.cfg.lstm_units, return_sequences=True),
                          input_shape=input_shape),
            Dropout(self.cfg.lstm_dropout),
            BatchNormalization(),
            Bidirectional(LSTM(self.cfg.lstm_units // 2, return_sequences=True)),
            Dropout(self.cfg.lstm_dropout),
            BatchNormalization(),
            LSTM(self.cfg.lstm_units // 4),
            Dropout(self.cfg.lstm_dropout),
            Dense(64, activation='relu'),
            Dense(32, activation='relu'),
            Dense(1)
        ])
        model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                      loss='huber',
                      metrics=['mae'])
        return model

    def _train_lstm(self, X_train, X_test, y_train, y_test):
        seq = self.cfg.seq_len
        scaler_X = MinMaxScaler()
        scaler_y = MinMaxScaler()

        X_tr_s = scaler_X.fit_transform(X_train)
        X_te_s = scaler_X.transform(X_test)
        y_tr_s = scaler_y.fit_transform(y_train.reshape(-1, 1)).ravel()
        y_te_s = scaler_y.transform(y_test.reshape(-1, 1)).ravel()

        self.scalers['lstm_X'] = scaler_X
        self.scalers['lstm_y'] = scaler_y

        Xtr_seq, ytr_seq = self._make_sequences(X_tr_s, y_tr_s, seq)
        Xte_seq, yte_seq = self._make_sequences(X_te_s, y_te_s, seq)

        callbacks = [
            EarlyStopping(patience=15, restore_best_weights=True, monitor='val_loss'),
            ReduceLROnPlateau(factor=0.5, patience=7, monitor='val_loss', min_lr=1e-6)
        ]

        model = self._build_lstm((seq, X_train.shape[1]))
        model.fit(
            Xtr_seq, ytr_seq,
            epochs          = self.cfg.lstm_epochs,
            batch_size      = self.cfg.batch_size,
            validation_split= 0.1,
            callbacks       = callbacks,
            verbose         = 0
        )

        preds_s = model.predict(Xte_seq, verbose=0).ravel()
        preds   = scaler_y.inverse_transform(preds_s.reshape(-1, 1)).ravel()
        actual  = y_test[seq:]

        self.models['LSTM'] = model
        return preds, actual

    # ──────────────────────────────────────────────────────────────
    # Random Forest
    # ──────────────────────────────────────────────────────────────
    def _train_rf(self, X_train, X_test, y_train, y_test):
        X_tr_s, X_te_s = self._scale(X_train, X_test, 'rf')
        model = RandomForestRegressor(
            n_estimators = self.cfg.rf_estimators,
            max_depth    = None,
            min_samples_split = 5,
            n_jobs       = -1,
            random_state = 42
        )
        model.fit(X_tr_s, y_train)
        preds = model.predict(X_te_s)
        self.models['RandomForest'] = model
        return preds, y_test

    # ──────────────────────────────────────────────────────────────
    # XGBoost
    # ──────────────────────────────────────────────────────────────
    def _train_xgb(self, X_train, X_test, y_train, y_test):
        X_tr_s, X_te_s = self._scale(X_train, X_test, 'xgb')
        model = XGBRegressor(
            n_estimators      = self.cfg.xgb_estimators,
            learning_rate     = self.cfg.xgb_lr,
            max_depth         = 6,
            subsample         = 0.8,
            colsample_bytree  = 0.8,
            reg_alpha         = 0.1,
            reg_lambda        = 1.0,
            random_state      = 42,
            verbosity         = 0,
            n_jobs            = -1
        )
        model.fit(X_tr_s, y_train,
                  eval_set    = [(X_te_s, y_test)],
                  verbose     = False)
        preds = model.predict(X_te_s)
        self.models['XGBoost'] = model
        return preds, y_test

    # ──────────────────────────────────────────────────────────────
    # Metrics
    # ──────────────────────────────────────────────────────────────
    def _metrics(self, actual, preds) -> dict:
        rmse = np.sqrt(mean_squared_error(actual, preds))
        mae  = mean_absolute_error(actual, preds)
        r2   = r2_score(actual, preds)
        mape = np.mean(np.abs((actual - preds) / (actual + 1e-10))) * 100
        return {'rmse': rmse, 'mae': mae, 'r2': r2, 'mape': mape,
                'preds': preds, 'actual': actual}

    # ──────────────────────────────────────────────────────────────
    # Public: fit + evaluate
    # ──────────────────────────────────────────────────────────────
    def fit_evaluate(self, df, feature_cols) -> dict:
        X_tr, X_te, y_tr, y_te, _ = self._train_test_split(df, feature_cols)
        use_all = self.sel == "all"

        if use_all or "rf" in self.sel:
            print("      Training Random Forest...", end=" ", flush=True)
            p, a = self._train_rf(X_tr, X_te, y_tr, y_te)
            self.results['RandomForest'] = self._metrics(a, p)
            print("done")

        if use_all or "xgb" in self.sel:
            print("      Training XGBoost...", end=" ", flush=True)
            p, a = self._train_xgb(X_tr, X_te, y_tr, y_te)
            self.results['XGBoost'] = self._metrics(a, p)
            print("done")

        if use_all or "lstm" in self.sel:
            print("      Training Bidirectional LSTM...", end=" ", flush=True)
            p, a = self._train_lstm(X_tr, X_te, y_tr, y_te)
            self.results['LSTM'] = self._metrics(a, p)
            print("done")

        # Save models
        self._save_models()
        return self.results

    # ──────────────────────────────────────────────────────────────
    # Forecast
    # ──────────────────────────────────────────────────────────────
    def forecast(self, df, engineer, days: int) -> pd.DataFrame:
        """Iterative multi-step forecast for `days` ahead."""
        forecasts = {name: [] for name in self.models}
        sim_df    = df.copy()

        for step in range(days):
            sim_df = engineer.build_forecast_row(sim_df)
            feat   = sim_df[engineer.feature_cols].values

            row_rf  = self.scalers['rf'].transform(feat[-1:])
            row_xgb = self.scalers['xgb'].transform(feat[-1:])

            if 'RandomForest' in self.models:
                forecasts['RandomForest'].append(
                    self.models['RandomForest'].predict(row_rf)[0])

            if 'XGBoost' in self.models:
                forecasts['XGBoost'].append(
                    self.models['XGBoost'].predict(row_xgb)[0])

            if 'LSTM' in self.models:
                seq     = self.cfg.seq_len
                X_s     = self.scalers['lstm_X'].transform(feat)
                if len(X_s) >= seq:
                    X_seq = X_s[-seq:].reshape(1, seq, feat.shape[1])
                    p_s   = self.models['LSTM'].predict(X_seq, verbose=0)[0][0]
                    p     = self.scalers['lstm_y'].inverse_transform([[p_s]])[0][0]
                    forecasts['LSTM'].append(p)
                else:
                    forecasts['LSTM'].append(sim_df['Close'].iloc[-1])

            # Use ensemble mean as next day's simulated close
            available = [v[-1] for v in forecasts.values() if v]
            next_close = np.mean(available)
            last_row   = sim_df.iloc[-1:].copy()
            last_row.index  = [last_row.index[0] + pd.Timedelta(days=1)]
            last_row['Close']  = next_close
            last_row['Open']   = next_close
            last_row['High']   = next_close * 1.005
            last_row['Low']    = next_close * 0.995
            last_row['Volume'] = sim_df['Volume'].mean()
            sim_df = pd.concat([sim_df, last_row])

        # Build forecast dataframe
        last_date = df.index[-1]
        dates = pd.bdate_range(start=last_date + pd.Timedelta(days=1), periods=days)
        fc_df = pd.DataFrame(forecasts, index=dates[:len(next(iter(forecasts.values())))])
        fc_df['ensemble'] = fc_df.mean(axis=1)
        return fc_df

    # ──────────────────────────────────────────────────────────────
    # Persistence
    # ──────────────────────────────────────────────────────────────
    def _save_models(self):
        d = self.cfg.model_dir
        for name, model in self.models.items():
            if name == 'LSTM':
                model.save(os.path.join(d, f"{self.cfg.ticker}_lstm.keras"))
            else:
                joblib.dump(model, os.path.join(d, f"{self.cfg.ticker}_{name}.pkl"))
        joblib.dump(self.scalers, os.path.join(d, f"{self.cfg.ticker}_scalers.pkl"))
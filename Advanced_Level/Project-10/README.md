# 🖼️ Image Recognition Classifier

> CNN-based image classification trained on CIFAR-10 · TensorFlow/Keras · Google Colab

[![License](https://img.shields.io/badge/License-AGPL--3.0-e8b84b?style=flat-square)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?style=flat-square&logo=tensorflow)
![Colab](https://img.shields.io/badge/Run%20on-Google%20Colab-F9AB00?style=flat-square&logo=googlecolab)

---

## 🚀 Features

- **CNN from Scratch** — 3 convolutional blocks with batch normalization and dropout, no pretrained weights required
- **Data Augmentation** — random flips, rotation, and zoom applied during training to reduce overfitting
- **Smart Training** — early stopping and learning-rate reduction automatically kick in when validation performance plateaus
- **Full Evaluation Suite** — accuracy/loss curves, a confusion matrix, and a per-class classification report
- **Upload & Predict** — test the trained model on your own photos directly in the notebook, top-3 confidence scores included
- **Model Export** — saves the trained model to a single `.keras` file you can download or reload later
- **Zero Local Setup** — runs entirely inside one Colab notebook, nothing to install on your machine

---

## 📁 Project Structure

```
image_recognition_classifier/
├── Image_Recognition_Classifier.ipynb    # The entire project — one notebook, run top to bottom
└── README.md
```

Since this is built specifically to run in Google Colab, it's structured as a single notebook rather than a package of scripts. Each section below corresponds to a group of cells inside it:

```
Image_Recognition_Classifier.ipynb
├── 1. Imports + GPU check
├── 2. Load & explore CIFAR-10        # auto-downloads, 10 classes
├── 3. Preprocess                     # normalize pixels, one-hot labels, train/val split
├── 4. Data augmentation              # random flip, rotation, zoom
├── 5. Build the CNN                  # conv blocks + dense classifier head
├── 6. Train                          # early stopping, LR reduction
├── 7. Evaluate on test set           # accuracy + training curves
├── 8. Confusion matrix + predictions
├── 9. Save the trained model
└── 10. Classify your own uploaded image
```

---

## ⚙️ Setup

```bash
# 1. Open the notebook in Google Colab
# (upload Image_Recognition_Classifier.ipynb, or open it directly from Drive/GitHub)

# 2. Runtime → Change runtime type → Hardware accelerator → GPU
# (training is much faster with a GPU; CPU works too, just slower)
```

No API keys or accounts needed — CIFAR-10 downloads automatically the first time you run the data-loading cell (~170MB).

---

## ▶️ Usage

All usage happens by running notebook cells in order, no command line involved.

```python
# Train the model (early stopping will end training automatically
# once validation accuracy stops improving)
history = model.fit(
    x_train_, y_train_,
    validation_data=(x_val, y_val),
    epochs=30,
    batch_size=64,
    callbacks=callbacks,
)

# Check performance on the held-out test set
test_loss, test_acc = model.evaluate(x_test, y_test_cat)

# Classify a photo of your own
predict_uploaded_image()
```

### Key settings

| Setting        | Default | Description                                             |
|-----------------|---------|-----------------------------------------------------------|
| `epochs`         | `30`    | Max training epochs (early stopping usually ends it sooner) |
| `batch_size`     | `64`    | Number of images per training step                        |
| `val_split`      | `5000`  | Images held out from the training set for validation      |
| Dropout rates    | `0.25–0.5` | Regularization strength across the network's layers     |

---

## 📊 Output Files

```
image_classifier.keras      # the trained model, ready to reload or download
```

Reload it later with:

```python
model = tf.keras.models.load_model('image_classifier.keras')
```

---

## ⚠️ Disclaimer

> This project is for **educational purposes only**.
> CIFAR-10 images are only 32×32px, so any real-world photo you upload gets downscaled hard before prediction — expect noticeably lower accuracy on custom images than on the CIFAR-10 test set itself.

For custom categories beyond CIFAR-10's 10 classes, or stronger real-world accuracy with less training data, swap this from-scratch CNN for transfer learning (e.g. `tf.keras.applications.MobileNetV2` with `include_top=False`).

---

## 📄 License

GNU AFFERO GENERAL PUBLIC LICENSE License — see [LICENSE](LICENSE)
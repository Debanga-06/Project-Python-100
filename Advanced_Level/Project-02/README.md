# 🎯 Facial Recognition System

> Advanced Computer Vision pipeline — OpenCV · Deep Learning · Anti-Spoofing · SQLite

[![License](https://img.shields.io/badge/License-AGPL--3.0-e8b84b?style=flat-square)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.9%2B-5C3EE8?style=flat-square&logo=opencv)
![Status](https://img.shields.io/badge/Status-Active-3fb950?style=flat-square)

---

## 🚀 Features

- **Multi-backend Detection** — Haar Cascade · DNN/SSD · MTCNN (landmark-aware)
- **Multi-model Recognition** — LBPH · Eigenfaces · Fisherfaces · Deep Embeddings (ResNet-128 / FaceNet)
- **Ensemble Mode** — Combines classical + deep models for best accuracy
- **Anti-Spoofing** — Texture analysis · Blink detection (EAR) · Motion flow · Colour diversity
- **Face Alignment** — Geometric alignment using eye landmarks
- **Temporal Smoothing** — Majority-vote buffer reduces flicker
- **SQLite Database** — Persons, embeddings, recognition event log
- **Stats Dashboard** — Matplotlib charts + CLI summary
- **Real-time HUD** — FPS, face count, model info overlay
- **File Analysis** — Process images & videos, save annotated output
- **Screenshot & Video Save** — Press `S` during live view

---

## 📁 Project Structure

```
facial_recognition/
├── main.py                    # CLI entry point
├── config.py                  # All settings in one place
├── requirements.txt
├── core/
│   ├── detector.py            # Haar / DNN / MTCNN backends
│   ├── embedding.py           # face_recognition / DeepFace / HOG
│   ├── recognizer.py          # Real-time loop + file analysis
│   ├── trainer.py             # Registration + model training
│   ├── anti_spoof.py          # Liveness detection (4 checks)
│   ├── database.py            # SQLite — persons, logs, embeddings
│   ├── visualizer.py          # Stats dashboard charts
│   └── logger.py              # Structured file + console logging
├── data/
│   ├── dataset/               # Registered face images
│   ├── models/                # Trained model files (.yml / .pkl)
│   └── logs/                  # Daily log files
└── output/                    # Annotated images / videos / charts
```

---

## ⚙️ Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# (Optional) For deep embedding recognition — best accuracy:
pip install cmake dlib face_recognition
```

---

## ▶️ Usage

### Step 1 — Register a person
```bash
# From webcam (captures 30 samples)
python main.py register --name "John Doe" --samples 30

# From a folder of photos
python main.py register --name "Jane Smith" --source ./photos/jane
```

### Step 2 — Train the model
```bash
python main.py train
```

### Step 3 — Real-time recognition
```bash
# Basic
python main.py recognize

# With anti-spoofing + save video
python main.py recognize --source 0 --spoof --save

# From a video file
python main.py recognize --source video.mp4
```

### Analyze an image or video
```bash
python main.py analyze --input photo.jpg --output result.jpg
python main.py analyze --input clip.mp4
```

### View statistics
```bash
python main.py stats
```

---

## ⚙️ Configuration (`config.py`)

| Setting | Default | Description |
|---|---|---|
| `detector_backend` | `haarcascade` | `haarcascade` / `dnn` / `mtcnn` |
| `recognizer_type` | `lbph` | `lbph` / `eigenfaces` / `fisherfaces` / `deep` |
| `recognition_threshold` | `70.0` | LBPH confidence threshold |
| `deep_threshold` | `0.40` | Cosine distance cutoff for deep model |
| `face_padding` | `0.20` | Padding around face crop |
| `spoof_blink_threshold` | `3` | Blinks required to pass liveness |

---

## ⌨️ Live Controls

| Key | Action |
|---|---|
| `Q` | Quit |
| `S` | Save screenshot |

---

## ⚠️ Disclaimer

> For educational purposes only. Do not deploy in production without proper consent, privacy policies, and legal compliance.

---

## 📄 License

GNU Affero General Public License v3.0
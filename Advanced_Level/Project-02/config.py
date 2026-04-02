"""
config.py — Central configuration for Facial Recognition System
"""

import os
from dataclasses import dataclass, field
from typing import Tuple


@dataclass
class Config:
    # ── Paths ─────────────────────────────────────────────────────
    data_dir:       str = "data"
    dataset_dir:    str = "data/dataset"       # registered face images
    model_dir:      str = "data/models"        # trained model files
    log_dir:        str = "data/logs"
    output_dir:     str = "output"
    cascade_dir:    str = "data/cascades"

    # ── Detection ─────────────────────────────────────────────────
    detector_backend:    str   = "haarcascade"  # haarcascade | dnn | mtcnn
    dnn_confidence:      float = 0.5
    min_face_size:       Tuple = (60, 60)
    scale_factor:        float = 1.1
    min_neighbors:       int   = 5
    face_padding:        float = 0.20           # padding % around detected face

    # ── Recognition ───────────────────────────────────────────────
    recognizer_type:     str   = "lbph"         # lbph | eigenfaces | fisherfaces | deep
    recognition_threshold: float = 70.0         # LBPH confidence threshold (lower = stricter)
    deep_threshold:      float = 0.40           # cosine distance for deep embeddings
    embedding_size:      int   = 128

    # ── Face Image Settings ───────────────────────────────────────
    face_size:           Tuple = (160, 160)     # resize for recognition
    gray_equalize:       bool  = True           # histogram equalization

    # ── Capture / Registration ────────────────────────────────────
    capture_delay_ms:    int   = 200            # ms between sample captures
    min_registration_samples: int = 10

    # ── Anti-Spoofing ──────────────────────────────────────────────
    spoof_blink_threshold:   int   = 3          # blinks required to pass
    spoof_texture_threshold: float = 10.0       # Laplacian variance threshold
    spoof_motion_frames:     int   = 5

    # ── Display ───────────────────────────────────────────────────
    window_width:        int   = 1280
    window_height:       int   = 720
    font_scale:          float = 0.65
    box_thickness:       int   = 2
    fps_display:         bool  = True

    # ── Logging ───────────────────────────────────────────────────
    log_level:           str   = "INFO"
    log_to_file:         bool  = True
    log_recognition_events: bool = True

    def __post_init__(self):
        for d in [self.data_dir, self.dataset_dir, self.model_dir,
                  self.log_dir, self.output_dir, self.cascade_dir]:
            os.makedirs(d, exist_ok=True)

    @property
    def lbph_model_path(self) -> str:
        return os.path.join(self.model_dir, "lbph_model.yml")

    @property
    def label_map_path(self) -> str:
        return os.path.join(self.model_dir, "label_map.pkl")

    @property
    def embeddings_path(self) -> str:
        return os.path.join(self.model_dir, "embeddings.pkl")

    @property
    def dnn_prototxt(self) -> str:
        return os.path.join(self.cascade_dir, "deploy.prototxt")

    @property
    def dnn_caffemodel(self) -> str:
        return os.path.join(self.cascade_dir, "res10_300x300_ssd_iter_140000.caffemodel")
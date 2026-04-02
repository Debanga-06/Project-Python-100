"""
core/detector.py
Multi-backend face detector:
  • Haar Cascade   (fast, CPU-only)
  • DNN / SSD      (accurate, supports GPU)
  • MTCNN          (landmark-aware, optional)
"""

import cv2
import numpy as np
from typing import List, Tuple
from config import Config


class FaceDetection:
    """Represents a single detected face."""
    def __init__(self, x, y, w, h, confidence=1.0, landmarks=None):
        self.x          = x
        self.y          = y
        self.w          = w
        self.h          = h
        self.confidence = confidence
        self.landmarks  = landmarks or {}

    @property
    def bbox(self):
        return (self.x, self.y, self.w, self.h)

    @property
    def center(self):
        return (self.x + self.w // 2, self.y + self.h // 2)

    def padded(self, img_h, img_w, pad: float = 0.15):
        """Return bbox with percentage padding, clamped to image bounds."""
        px = int(self.w * pad)
        py = int(self.h * pad)
        x1 = max(0,     self.x - px)
        y1 = max(0,     self.y - py)
        x2 = min(img_w, self.x + self.w + px)
        y2 = min(img_h, self.y + self.h + py)
        return x1, y1, x2 - x1, y2 - y1

    def area(self):
        return self.w * self.h

    def __repr__(self):
        return f"FaceDetection(x={self.x}, y={self.y}, w={self.w}, h={self.h}, conf={self.confidence:.2f})"


# ──────────────────────────────────────────────────────────────────
class HaarDetector:
    """Classic Haar Cascade detector — fast, no GPU needed."""

    def __init__(self, cfg: Config):
        self.cfg      = cfg
        self._cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self._eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_eye.xml"
        )

    def detect(self, frame: np.ndarray) -> List[FaceDetection]:
        gray   = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray   = cv2.equalizeHist(gray) if self.cfg.gray_equalize else gray
        faces  = self._cascade.detectMultiScale(
            gray,
            scaleFactor  = self.cfg.scale_factor,
            minNeighbors = self.cfg.min_neighbors,
            minSize      = self.cfg.min_face_size,
            flags        = cv2.CASCADE_SCALE_IMAGE
        )
        results = []
        if len(faces) == 0:
            return results
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            eyes     = self._eye_cascade.detectMultiScale(roi_gray, 1.1, 4)
            lm       = {"eyes_count": len(eyes)}
            results.append(FaceDetection(x, y, w, h, landmarks=lm))
        return results


# ──────────────────────────────────────────────────────────────────
class DNNDetector:
    """SSD / ResNet-10 DNN detector — more accurate, handles angles."""

    def __init__(self, cfg: Config):
        self.cfg = cfg
        try:
            self.net = cv2.dnn.readNetFromCaffe(
                cfg.dnn_prototxt, cfg.dnn_caffemodel
            )
        except Exception:
            print("  ⚠️  DNN model files not found. Falling back to Haar Cascade.")
            self.net = None

    def detect(self, frame: np.ndarray) -> List[FaceDetection]:
        if self.net is None:
            return HaarDetector(self.cfg).detect(frame)

        h, w    = frame.shape[:2]
        blob    = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)), 1.0,
            (300, 300), (104.0, 177.0, 123.0)
        )
        self.net.setInput(blob)
        detections = self.net.forward()
        results    = []

        for i in range(detections.shape[2]):
            conf = float(detections[0, 0, i, 2])
            if conf < self.cfg.dnn_confidence:
                continue
            box  = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            x1, y1, x2, y2 = box.astype(int)
            fx, fy = max(0, x1), max(0, y1)
            fw, fh = min(w, x2) - fx, min(h, y2) - fy
            if fw > 0 and fh > 0:
                results.append(FaceDetection(fx, fy, fw, fh, confidence=conf))
        return results


# ──────────────────────────────────────────────────────────────────
class MTCNNDetector:
    """MTCNN — landmark-aware, best accuracy, requires mtcnn package."""

    def __init__(self, cfg: Config):
        self.cfg = cfg
        try:
            from mtcnn import MTCNN
            self._det = MTCNN()
        except ImportError:
            print("  ⚠️  mtcnn not installed. pip install mtcnn")
            self._det = None

    def detect(self, frame: np.ndarray) -> List[FaceDetection]:
        if self._det is None:
            return HaarDetector(self.cfg).detect(frame)
        rgb     = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self._det.detect_faces(rgb)
        faces   = []
        for r in results:
            x, y, w, h = r['box']
            conf = r['confidence']
            lm   = r.get('keypoints', {})
            faces.append(FaceDetection(max(0,x), max(0,y), w, h,
                                       confidence=conf, landmarks=lm))
        return faces


# ──────────────────────────────────────────────────────────────────
class FaceDetector:
    """Unified detector — selects backend from config."""

    def __init__(self, cfg: Config):
        self.cfg = cfg
        backend  = cfg.detector_backend.lower()
        if backend == "dnn":
            self._backend = DNNDetector(cfg)
        elif backend == "mtcnn":
            self._backend = MTCNNDetector(cfg)
        else:
            self._backend = HaarDetector(cfg)
        print(f"   🔍 Detector backend : {backend.upper()}")

    def detect(self, frame: np.ndarray) -> List[FaceDetection]:
        return self._backend.detect(frame)

    def detect_largest(self, frame: np.ndarray):
        """Return only the largest face (most prominent)."""
        faces = self.detect(frame)
        return max(faces, key=lambda f: f.area()) if faces else None

    def extract_face(self, frame: np.ndarray,
                     detection: FaceDetection,
                     size: Tuple = None) -> np.ndarray:
        """Crop & resize face ROI from frame."""
        size = size or self.cfg.face_size
        h, w = frame.shape[:2]
        x, y, fw, fh = detection.padded(h, w, self.cfg.face_padding)
        roi  = frame[y:y+fh, x:x+fw]
        roi  = cv2.resize(roi, size)
        return roi

    def extract_faces(self, frame: np.ndarray,
                      size: Tuple = None) -> List[np.ndarray]:
        """Detect all faces and return list of cropped ROIs."""
        detections = self.detect(frame)
        return [self.extract_face(frame, d, size) for d in detections]

    def align_face(self, frame: np.ndarray,
                   detection: FaceDetection) -> np.ndarray:
        """Geometric alignment using eye landmarks if available."""
        lm = detection.landmarks
        if 'left_eye' in lm and 'right_eye' in lm:
            le = np.array(lm['left_eye'])
            re = np.array(lm['right_eye'])
            dY = re[1] - le[1]
            dX = re[0] - le[0]
            angle = np.degrees(np.arctan2(dY, dX))
            center = detection.center
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            frame = cv2.warpAffine(frame, M, (frame.shape[1], frame.shape[0]),
                                   flags=cv2.INTER_CUBIC)
        return self.extract_face(frame, detection)
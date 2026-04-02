"""
core/anti_spoof.py
Liveness detection using multiple passive cues:
  1. Texture analysis   — Laplacian variance (real skin ≠ flat print)
  2. Blink detection    — Eye Aspect Ratio (EAR) via dlib/landmarks
  3. Motion analysis    — Optical flow variance
  4. Colour histogram   — Real face has more varied skin tones
"""

import cv2
import numpy as np
from collections import deque
from typing import Optional
from config          import Config
from core.detector   import FaceDetection


class AntiSpoofing:
    def __init__(self, cfg: Config):
        self.cfg          = cfg
        self._blink_count = 0
        self._ear_buf     = deque(maxlen=10)
        self._prev_gray   = None
        self._motion_buf  = deque(maxlen=cfg.spoof_motion_frames)
        self._passed      = False    # once liveness verified, keep flag

        # Try to load dlib for EAR-based blink detection
        try:
            import dlib
            self._shape_predictor = dlib.shape_predictor(
                "data/shape_predictor_68_face_landmarks.dat"
            )
            self._dlib_available = True
        except Exception:
            self._dlib_available = False

    # ── Texture Score ─────────────────────────────────────────────
    def _texture_score(self, face_roi: np.ndarray) -> float:
        """Laplacian variance — blurry prints score low."""
        gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        return float(cv2.Laplacian(gray, cv2.CV_64F).var())

    # ── Colour Diversity ──────────────────────────────────────────
    def _colour_diversity(self, face_roi: np.ndarray) -> float:
        """Std of HSV channels — printed faces are more uniform."""
        hsv = cv2.cvtColor(face_roi, cv2.COLOR_BGR2HSV)
        return float(np.std(hsv[:,:,0]))   # Hue std

    # ── Motion Score ──────────────────────────────────────────────
    def _motion_score(self, gray: np.ndarray) -> float:
        if self._prev_gray is None or self._prev_gray.shape != gray.shape:
            self._prev_gray = gray
            return 1.0
        flow = cv2.calcOpticalFlowFarneback(
            self._prev_gray, gray, None,
            0.5, 3, 15, 3, 5, 1.2, 0
        )
        self._prev_gray = gray.copy()
        mag, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        return float(mag.mean())

    # ── EAR Blink Detection ───────────────────────────────────────
    def _eye_aspect_ratio(self, eye_pts: np.ndarray) -> float:
        A = np.linalg.norm(eye_pts[1] - eye_pts[5])
        B = np.linalg.norm(eye_pts[2] - eye_pts[4])
        C = np.linalg.norm(eye_pts[0] - eye_pts[3])
        return (A + B) / (2.0 * C + 1e-6)

    def _detect_blink_dlib(self, frame: np.ndarray,
                            detection: FaceDetection) -> bool:
        import dlib
        x, y, w, h = detection.bbox
        rect = dlib.rectangle(x, y, x+w, y+h)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        shape = self._shape_predictor(gray, rect)
        pts   = np.array([[shape.part(i).x, shape.part(i).y]
                          for i in range(68)])

        left_ear  = self._eye_aspect_ratio(pts[42:48])
        right_ear = self._eye_aspect_ratio(pts[36:42])
        ear       = (left_ear + right_ear) / 2.0
        self._ear_buf.append(ear)

        EAR_THRESH = 0.25
        if ear < EAR_THRESH:
            if len(self._ear_buf) >= 2 and self._ear_buf[-2] >= EAR_THRESH:
                self._blink_count += 1
        return self._blink_count >= self.cfg.spoof_blink_threshold

    def _detect_blink_simple(self, face_roi: np.ndarray) -> bool:
        """Haar-based eye detection as blink proxy (less accurate)."""
        gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_eye.xml"
        )
        eyes = eye_cascade.detectMultiScale(gray, 1.1, 4, minSize=(20,20))
        # If eyes not found → likely blinking
        if len(eyes) == 0:
            self._blink_count += 1
        return self._blink_count >= self.cfg.spoof_blink_threshold

    # ── Main Decision ──────────────────────────────────────────────
    def is_real(self, face_roi: np.ndarray, frame: np.ndarray,
                detection: Optional[FaceDetection] = None) -> bool:
        """Returns True if face passes liveness checks."""
        if self._passed:
            return True

        scores = {}

        # 1. Texture
        tex = self._texture_score(face_roi)
        scores['texture'] = tex > self.cfg.spoof_texture_threshold

        # 2. Colour diversity
        cdiv = self._colour_diversity(face_roi)
        scores['colour'] = cdiv > 8.0

        # 3. Motion
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        mot   = self._motion_score(face_gray)
        self._motion_buf.append(mot)
        scores['motion'] = np.mean(self._motion_buf) > 0.3

        # 4. Blink
        if self._dlib_available and detection:
            blinked = self._detect_blink_dlib(frame, detection)
        else:
            blinked = self._detect_blink_simple(face_roi)
        scores['blink'] = blinked

        passed_count = sum(scores.values())
        result       = passed_count >= 3    # at least 3/4 checks pass

        if result:
            self._passed = True

        return result

    def reset(self):
        """Reset state between subjects."""
        self._blink_count = 0
        self._ear_buf.clear()
        self._motion_buf.clear()
        self._prev_gray = None
        self._passed    = False

    def get_status(self) -> dict:
        return {
            "blinks":  self._blink_count,
            "passed":  self._passed,
            "needed":  self.cfg.spoof_blink_threshold,
        }
"""
core/recognizer.py
Core recognition engine — real-time camera loop & file analysis.
Supports LBPH + deep embedding matching with confidence smoothing.
"""

import cv2
import os
import time
import pickle
import numpy as np
from datetime import datetime
from typing import Optional, Dict, List, Tuple
from collections import deque

from config          import Config
from core.detector   import FaceDetector, FaceDetection
from core.database   import FaceDatabase
from core.anti_spoof import AntiSpoofing
from core.logger     import SystemLogger
from core.embedding  import EmbeddingExtractor


class RecognitionResult:
    def __init__(self, name: str, confidence: float,
                 is_spoof: bool = False, method: str = "lbph"):
        self.name       = name
        self.confidence = confidence
        self.is_spoof   = is_spoof
        self.method     = method
        self.timestamp  = datetime.now()

    @property
    def is_known(self):
        return self.name != "Unknown"

    @property
    def display_confidence(self):
        return f"{self.confidence:.1f}%"


# ──────────────────────────────────────────────────────────────────
class FacialRecognizer:
    def __init__(self, cfg: Config, db: FaceDatabase,
                 det: FaceDetector, spoof: Optional[AntiSpoofing],
                 log: SystemLogger):
        self.cfg   = cfg
        self.db    = db
        self.det   = det
        self.spoof = spoof
        self.log   = log

        self._lbph_model   = None
        self._label_map    = {}
        self._embeddings   = {}
        self._emb_extractor= None
        self._smooth_buf   : Dict[int, deque] = {}   # per-face smoothing

        self._load_models()

    # ── Model Loading ─────────────────────────────────────────────
    def _load_models(self):
        rtype = self.cfg.recognizer_type.lower()

        # LBPH
        if os.path.exists(self.cfg.lbph_model_path) and rtype in ("lbph","all"):
            self._lbph_model = cv2.face.LBPHFaceRecognizer_create()
            self._lbph_model.read(self.cfg.lbph_model_path)
            print("   ✅ LBPH model loaded")

        # Eigenfaces
        ef_path = os.path.join(self.cfg.model_dir, "eigenfaces.yml")
        if os.path.exists(ef_path) and rtype == "eigenfaces":
            self._lbph_model = cv2.face.EigenFaceRecognizer_create()
            self._lbph_model.read(ef_path)
            print("   ✅ Eigenfaces model loaded")

        # Fisherfaces
        ff_path = os.path.join(self.cfg.model_dir, "fisherfaces.yml")
        if os.path.exists(ff_path) and rtype == "fisherfaces":
            self._lbph_model = cv2.face.FisherFaceRecognizer_create()
            self._lbph_model.read(ff_path)
            print("   ✅ Fisherfaces model loaded")

        # Deep embeddings
        if os.path.exists(self.cfg.embeddings_path):
            with open(self.cfg.embeddings_path, 'rb') as f:
                self._embeddings = pickle.load(f)
            self._emb_extractor = EmbeddingExtractor(self.cfg)
            print(f"   ✅ Deep embeddings loaded ({len(self._embeddings)} persons)")

        # Label map
        self._label_map = self.db.load_label_map()
        if not self._lbph_model and not self._embeddings:
            print("   ⚠️  No trained model found. Run: python main.py train")

    # ── Recognition Logic ─────────────────────────────────────────
    def _recognize_lbph(self, gray_face: np.ndarray) -> Tuple[str, float]:
        if self._lbph_model is None:
            return "Unknown", 0.0
        gray_face = cv2.resize(gray_face, self.cfg.face_size)
        label, dist = self._lbph_model.predict(gray_face)
        # LBPH: lower distance = better match
        conf = max(0.0, 100.0 - dist)
        if dist > self.cfg.recognition_threshold:
            return "Unknown", conf
        name = self._label_map.get(label, "Unknown")
        return name, conf

    def _recognize_deep(self, face_img: np.ndarray) -> Tuple[str, float]:
        if not self._embeddings or self._emb_extractor is None:
            return "Unknown", 0.0
        query_emb = self._emb_extractor.extract(face_img)
        if query_emb is None:
            return "Unknown", 0.0

        best_name = "Unknown"
        best_dist = float('inf')

        for person_name, emb_list in self._embeddings.items():
            for emb in emb_list:
                dist = self._emb_extractor.compare(query_emb, emb, "cosine")
                if dist < best_dist:
                    best_dist = dist
                    best_name = person_name

        if best_dist > self.cfg.deep_threshold:
            return "Unknown", max(0.0, (1.0 - best_dist) * 100)
        return best_name, max(0.0, (1.0 - best_dist) * 100)

    def _recognize_face(self, frame: np.ndarray,
                        detection: FaceDetection) -> RecognitionResult:
        face_bgr  = self.det.extract_face(frame, detection)
        face_gray = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2GRAY)

        rtype = self.cfg.recognizer_type.lower()
        if rtype == "deep":
            name, conf = self._recognize_deep(face_bgr)
            method = "deep"
        elif self._embeddings and self._lbph_model:
            # Ensemble: average both
            n1, c1 = self._recognize_lbph(face_gray)
            n2, c2 = self._recognize_deep(face_bgr)
            name   = n1 if c1 >= c2 else n2
            conf   = (c1 + c2) / 2
            method = "ensemble"
        else:
            name, conf = self._recognize_lbph(face_gray)
            method = "lbph"

        return RecognitionResult(name, conf, method=method)

    # ── Temporal Smoothing ────────────────────────────────────────
    def _smooth_result(self, face_id: int, result: RecognitionResult,
                       window: int = 5) -> RecognitionResult:
        if face_id not in self._smooth_buf:
            self._smooth_buf[face_id] = deque(maxlen=window)
        self._smooth_buf[face_id].append(result.name)
        # Majority vote
        names    = list(self._smooth_buf[face_id])
        majority = max(set(names), key=names.count)
        result.name = majority
        return result

    # ── Overlay Drawing ───────────────────────────────────────────
    def _draw_overlay(self, frame: np.ndarray, detection: FaceDetection,
                      result: RecognitionResult) -> np.ndarray:
        x, y, w, h = detection.bbox
        is_known   = result.is_known and not result.is_spoof

        # Box colour
        color = (0, 220, 80) if is_known else (0, 60, 220)
        if result.is_spoof:
            color = (0, 0, 255)

        # Bounding box
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, self.cfg.box_thickness)

        # Corner accents
        clen = min(w, h) // 5
        for (cx, cy), (dx, dy) in [
            ((x,y),     (1,1)),  ((x+w,y),   (-1,1)),
            ((x,y+h),   (1,-1)), ((x+w,y+h), (-1,-1))
        ]:
            cv2.line(frame, (cx, cy), (cx + dx*clen, cy), color, 3)
            cv2.line(frame, (cx, cy), (cx, cy + dy*clen), color, 3)

        # Label background
        label   = f"{'🔒 SPOOF' if result.is_spoof else result.name}"
        conf_str= f"{result.confidence:.1f}%"
        font    = cv2.FONT_HERSHEY_SIMPLEX
        fs      = self.cfg.font_scale
        (lw, lh), _ = cv2.getTextSize(f"{label} {conf_str}", font, fs, 2)
        cv2.rectangle(frame, (x, y - lh - 14), (x + lw + 10, y), color, -1)
        cv2.putText(frame, f"{label} {conf_str}",
                    (x + 5, y - 6), font, fs, (255,255,255), 2)

        # Landmarks
        if 'left_eye' in detection.landmarks and 'right_eye' in detection.landmarks:
            for pt in [detection.landmarks['left_eye'],
                       detection.landmarks['right_eye']]:
                cv2.circle(frame, tuple(pt), 3, color, -1)

        return frame

    def _draw_hud(self, frame, fps, n_faces, frame_num):
        h, w = frame.shape[:2]
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (280, 110), (15,15,15), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

        lines = [
            f"FPS        : {fps:.1f}",
            f"Faces      : {n_faces}",
            f"Frame      : {frame_num}",
            f"Model      : {self.cfg.recognizer_type.upper()}",
            f"Anti-Spoof : {'ON' if self.spoof else 'OFF'}",
        ]
        for i, line in enumerate(lines):
            cv2.putText(frame, line, (10, 22 + i * 18),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.48, (180,220,180), 1)
        # Controls hint
        cv2.putText(frame, "Q: Quit  S: Screenshot",
                    (10, h - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    0.45, (120,120,120), 1)
        return frame

    # ── Real-Time Loop ────────────────────────────────────────────
    def run_realtime(self, source: str, save: bool = False):
        src = int(source) if source.isdigit() else source
        cap = cv2.VideoCapture(src)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,  self.cfg.window_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cfg.window_height)

        writer = None
        if save:
            out_path = os.path.join(self.cfg.output_dir,
                                    f"recognition_{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi")
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            writer = cv2.VideoWriter(out_path, fourcc, 20.0,
                                     (self.cfg.window_width, self.cfg.window_height))
            print(f"   📹 Saving to {out_path}")

        print("\n   🎥 Recognition running. Press 'Q' to quit, 'S' for screenshot.\n")
        fps_timer  = time.time()
        fps        = 0.0
        frame_num  = 0
        fps_count  = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame_num += 1
            fps_count += 1

            if time.time() - fps_timer >= 1.0:
                fps       = fps_count / (time.time() - fps_timer)
                fps_timer = time.time()
                fps_count = 0

            detections = self.det.detect(frame)

            for i, det in enumerate(detections):
                result = self._recognize_face(frame, det)
                result = self._smooth_result(i, result)

                # Anti-spoofing check
                if self.spoof:
                    face_roi = self.det.extract_face(frame, det)
                    result.is_spoof = not self.spoof.is_real(face_roi, frame, det)

                frame = self._draw_overlay(frame, det, result)

                if self.cfg.log_recognition_events and result.is_known:
                    self.db.log_recognition(result.name, result.confidence,
                                            spoof=result.is_spoof)
                    self.log.info(f"Recognized: {result.name} ({result.confidence:.1f}%)")

            frame = self._draw_hud(frame, fps, len(detections), frame_num)

            if writer:
                writer.write(frame)

            cv2.imshow("Facial Recognition System", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                ss_path = os.path.join(self.cfg.output_dir,
                    f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
                cv2.imwrite(ss_path, frame)
                print(f"   📸 Screenshot saved → {ss_path}")

        cap.release()
        if writer:
            writer.release()
        cv2.destroyAllWindows()

    # ── File Analysis ─────────────────────────────────────────────
    def analyze_file(self, input_path: str, output_path: Optional[str],
                     viz=None):
        ext = os.path.splitext(input_path)[1].lower()
        if ext in ('.jpg', '.jpeg', '.png', '.bmp', '.webp'):
            self._analyze_image(input_path, output_path)
        elif ext in ('.mp4', '.avi', '.mov', '.mkv'):
            self._analyze_video(input_path, output_path)
        else:
            print(f"   ❌ Unsupported file type: {ext}")

    def _analyze_image(self, path: str, out: Optional[str]):
        frame      = cv2.imread(path)
        detections = self.det.detect(frame)
        results    = []

        for det in detections:
            result = self._recognize_face(frame, det)
            frame  = self._draw_overlay(frame, det, result)
            results.append(result)
            print(f"   👤 {result.name:<20} conf={result.confidence:.1f}%  method={result.method}")

        out = out or os.path.join(self.cfg.output_dir,
              "analyzed_" + os.path.basename(path))
        cv2.imwrite(out, frame)
        print(f"\n   ✅ Saved → {out}  |  {len(results)} face(s) detected")

    def _analyze_video(self, path: str, out: Optional[str]):
        cap    = cv2.VideoCapture(path)
        w      = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h      = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps    = cap.get(cv2.CAP_PROP_FPS) or 25
        out    = out or os.path.join(self.cfg.output_dir,
                 "analyzed_" + os.path.basename(path))
        writer = cv2.VideoWriter(out, cv2.VideoWriter_fourcc(*'mp4v'),
                                 fps, (w, h))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        i = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            i += 1
            if i % 50 == 0:
                print(f"   Processing frame {i}/{frame_count}...")
            for det in self.det.detect(frame):
                result = self._recognize_face(frame, det)
                frame  = self._draw_overlay(frame, det, result)
            writer.write(frame)
        cap.release()
        writer.release()
        print(f"   ✅ Saved → {out}")
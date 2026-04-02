"""
core/embedding.py
Deep face embedding extraction.
  Primary  : face_recognition library (dlib + ResNet-128d)
  Fallback : OpenCV DNN (MobileNet feature extractor)
  Manual   : Simple CNN with TensorFlow/Keras
"""

import cv2
import numpy as np
from typing import Optional
from config import Config


class EmbeddingExtractor:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        self._backend = self._init_backend()

    def _init_backend(self):
        # Try face_recognition (dlib ResNet128)
        try:
            import face_recognition
            print("   🧠 Embedding backend : face_recognition (dlib ResNet-128)")
            return "face_recognition"
        except ImportError:
            pass

        # Try DeepFace
        try:
            from deepface import DeepFace
            print("   🧠 Embedding backend : DeepFace (FaceNet)")
            return "deepface"
        except ImportError:
            pass

        # Fallback: simple HOG
        print("   🧠 Embedding backend : HOG (install face_recognition for best results)")
        return "hog"

    def extract(self, face_img: np.ndarray) -> Optional[np.ndarray]:
        """Extract 128-d embedding from a face image (BGR)."""
        if self._backend == "face_recognition":
            return self._extract_face_recognition(face_img)
        elif self._backend == "deepface":
            return self._extract_deepface(face_img)
        else:
            return self._extract_hog(face_img)

    def _extract_face_recognition(self, img: np.ndarray) -> Optional[np.ndarray]:
        import face_recognition
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encs = face_recognition.face_encodings(rgb)
        return np.array(encs[0]) if encs else None

    def _extract_deepface(self, img: np.ndarray) -> Optional[np.ndarray]:
        from deepface import DeepFace
        try:
            result = DeepFace.represent(img, model_name="Facenet",
                                        enforce_detection=False)
            return np.array(result[0]['embedding'])
        except Exception:
            return None

    def _extract_hog(self, img: np.ndarray) -> Optional[np.ndarray]:
        """HOG-based pseudo-embedding (fallback)."""
        gray   = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (64, 64))
        hog    = cv2.HOGDescriptor(
            (64,64), (16,16), (8,8), (8,8), 9
        )
        desc = hog.compute(resized)
        # Reduce to 128-d via mean pooling
        chunk = len(desc) // 128
        emb   = np.array([desc[i*chunk:(i+1)*chunk].mean()
                          for i in range(128)])
        norm  = np.linalg.norm(emb)
        return emb / (norm + 1e-10)

    # ── Similarity ────────────────────────────────────────────────
    @staticmethod
    def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10))

    @staticmethod
    def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
        return float(np.linalg.norm(a - b))

    def compare(self, emb1: np.ndarray, emb2: np.ndarray,
                metric: str = "cosine") -> float:
        if metric == "cosine":
            return 1.0 - self.cosine_similarity(emb1, emb2)   # distance
        return self.euclidean_distance(emb1, emb2)
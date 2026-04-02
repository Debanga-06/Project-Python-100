"""
core/trainer.py
Handles face registration (capture samples) and model training.
Supports LBPH, Eigenfaces, Fisherfaces, and deep embedding training.
"""

import cv2
import os
import numpy as np
import pickle
from typing import List
from config  import Config
from core.detector  import FaceDetector
from core.database  import FaceDatabase
from core.logger    import SystemLogger
from core.embedding import EmbeddingExtractor


class FaceTrainer:
    def __init__(self, cfg: Config, db: FaceDatabase,
                 det: FaceDetector, log: SystemLogger):
        self.cfg = cfg
        self.db  = db
        self.det = det
        self.log = log

    # ── Registration ──────────────────────────────────────────────
    def register(self, name: str, source: str, n_samples: int):
        """Capture face samples from camera or folder."""
        label = self.db.add_person(name)
        person_dir = os.path.join(self.cfg.dataset_dir, name)
        os.makedirs(person_dir, exist_ok=True)

        if os.path.isdir(source):
            count = self._register_from_folder(name, label, source, person_dir)
        else:
            count = self._register_from_camera(name, label, int(source),
                                               n_samples, person_dir)
        self.db.increment_sample_count(name, count)
        self.log.info(f"Registered {count} samples for '{name}' (label={label})")
        print(f"\n   ✅ Registered {count} samples for '{name}'")
        print(f"   ℹ️  Run: python main.py train")

    def _register_from_camera(self, name, label, cam_idx,
                               n_samples, save_dir) -> int:
        cap   = cv2.VideoCapture(cam_idx)
        count = 0
        print(f"\n   📷 Camera open. Capturing {n_samples} samples for '{name}'...")
        print(f"   Press 'q' to stop early.\n")

        while count < n_samples:
            ret, frame = cap.read()
            if not ret:
                break

            face = self.det.detect_largest(frame)
            display = frame.copy()

            if face:
                roi = self.det.extract_face(frame, face)
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                path = os.path.join(save_dir, f"{label}_{count:04d}.jpg")
                cv2.imwrite(path, gray_roi)
                count += 1

                x, y, w, h = face.bbox
                cv2.rectangle(display, (x,y), (x+w,y+h), (0,255,100), 2)
                pct = int(count / n_samples * 100)
                bar = '█' * (pct // 5) + '░' * (20 - pct // 5)
                cv2.putText(display, f"[{bar}] {count}/{n_samples}",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            (0,255,100), 2)
                cv2.waitKey(self.cfg.capture_delay_ms)
            else:
                cv2.putText(display, "No face detected — center your face",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                            (0,80,255), 2)

            cv2.imshow(f"Registering: {name}", display)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return count

    def _register_from_folder(self, name, label, folder, save_dir) -> int:
        exts  = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')
        files = [f for f in os.listdir(folder)
                 if f.lower().endswith(exts)]
        count = 0
        for fname in files:
            img = cv2.imread(os.path.join(folder, fname))
            if img is None:
                continue
            face = self.det.detect_largest(img)
            if face:
                roi = self.det.extract_face(img, face)
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                path = os.path.join(save_dir, f"{label}_{count:04d}.jpg")
                cv2.imwrite(path, gray_roi)
                count += 1
        return count

    # ── Training ──────────────────────────────────────────────────
    def train(self):
        """Train the selected recognizer on all registered faces."""
        print("\n   🔄 Loading dataset...")
        faces, labels = self._load_dataset()

        if len(faces) == 0:
            print("   ❌ No face data found. Register faces first.")
            return

        persons = self.db.list_persons()
        print(f"   ✅ {len(faces)} samples | {len(persons)} persons")

        rtype = self.cfg.recognizer_type.lower()

        if rtype == "lbph":
            self._train_lbph(faces, labels)
        elif rtype == "eigenfaces":
            self._train_eigenfaces(faces, labels)
        elif rtype == "fisherfaces":
            self._train_fisherfaces(faces, labels)
        elif rtype == "deep":
            self._train_deep_embeddings()
        else:
            self._train_lbph(faces, labels)

        self.db.save_label_map()
        self.log.info(f"Model trained: {rtype} | {len(faces)} samples | {len(persons)} persons")
        print(f"   ✅ Training complete → {self.cfg.model_dir}/")

    def _load_dataset(self):
        faces, labels = [], []
        dataset_dir   = self.cfg.dataset_dir

        for person_name in os.listdir(dataset_dir):
            person_dir = os.path.join(dataset_dir, person_name)
            if not os.path.isdir(person_dir):
                continue
            person = self.db.get_person_by_name(person_name)
            if not person:
                continue
            label = person['label']

            for fname in os.listdir(person_dir):
                if not fname.lower().endswith(('.jpg', '.png')):
                    continue
                img = cv2.imread(os.path.join(person_dir, fname),
                                 cv2.IMREAD_GRAYSCALE)
                if img is None:
                    continue
                img = cv2.resize(img, self.cfg.face_size)
                faces.append(img)
                labels.append(label)

        return faces, labels

    def _train_lbph(self, faces: List[np.ndarray], labels: List[int]):
        print("   🔄 Training LBPH recognizer...")
        recognizer = cv2.face.LBPHFaceRecognizer_create(
            radius=1, neighbors=8, grid_x=8, grid_y=8
        )
        recognizer.train(faces, np.array(labels))
        recognizer.save(self.cfg.lbph_model_path)
        print(f"   ✅ LBPH model saved → {self.cfg.lbph_model_path}")

    def _train_eigenfaces(self, faces: List[np.ndarray], labels: List[int]):
        print("   🔄 Training Eigenfaces recognizer...")
        recognizer = cv2.face.EigenFaceRecognizer_create(num_components=150)
        recognizer.train(faces, np.array(labels))
        recognizer.save(os.path.join(self.cfg.model_dir, "eigenfaces.yml"))
        print("   ✅ Eigenfaces model saved")

    def _train_fisherfaces(self, faces: List[np.ndarray], labels: List[int]):
        print("   🔄 Training Fisherfaces recognizer...")
        recognizer = cv2.face.FisherFaceRecognizer_create()
        recognizer.train(faces, np.array(labels))
        recognizer.save(os.path.join(self.cfg.model_dir, "fisherfaces.yml"))
        print("   ✅ Fisherfaces model saved")

    def _train_deep_embeddings(self):
        """Extract and store FaceNet embeddings for all registered persons."""
        print("   🔄 Extracting deep embeddings...")
        extractor  = EmbeddingExtractor(self.cfg)
        dataset_dir = self.cfg.dataset_dir
        all_embs   = {}

        for person_name in os.listdir(dataset_dir):
            person_dir = os.path.join(dataset_dir, person_name)
            if not os.path.isdir(person_dir):
                continue
            embs = []
            for fname in os.listdir(person_dir):
                if not fname.lower().endswith(('.jpg', '.png')):
                    continue
                img = cv2.imread(os.path.join(person_dir, fname))
                if img is None:
                    continue
                emb = extractor.extract(img)
                if emb is not None:
                    embs.append(emb)
            if embs:
                all_embs[person_name] = embs
                print(f"      {person_name}: {len(embs)} embeddings")

        with open(self.cfg.embeddings_path, 'wb') as f:
            pickle.dump(all_embs, f)
        print(f"   ✅ Embeddings saved → {self.cfg.embeddings_path}")
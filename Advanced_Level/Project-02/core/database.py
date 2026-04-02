"""
core/database.py
SQLite-backed face database — stores persons, embeddings, recognition events.
"""

import os
import sqlite3
import pickle
import json
from datetime import datetime
from typing import Optional, List, Dict
from config import Config


class FaceDatabase:
    def __init__(self, cfg: Config):
        self.cfg     = cfg
        self.db_path = os.path.join(cfg.data_dir, "faces.db")
        self._init_db()

    # ── Schema ────────────────────────────────────────────────────
    def _init_db(self):
        with self._conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS persons (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    name        TEXT    NOT NULL UNIQUE,
                    label       INTEGER NOT NULL UNIQUE,
                    registered  TEXT    NOT NULL,
                    sample_count INTEGER DEFAULT 0,
                    metadata    TEXT    DEFAULT '{}'
                );

                CREATE TABLE IF NOT EXISTS recognition_log (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    person_name TEXT,
                    confidence  REAL,
                    timestamp   TEXT    NOT NULL,
                    source      TEXT    DEFAULT 'camera',
                    spoof       INTEGER DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS embeddings (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    person_id   INTEGER NOT NULL,
                    embedding   BLOB    NOT NULL,
                    created     TEXT    NOT NULL,
                    FOREIGN KEY(person_id) REFERENCES persons(id)
                );
            """)

    def _conn(self):
        return sqlite3.connect(self.db_path)

    # ── Person Management ─────────────────────────────────────────
    def add_person(self, name: str) -> int:
        """Register new person; returns their label integer."""
        with self._conn() as conn:
            existing = conn.execute(
                "SELECT label FROM persons WHERE name=?", (name,)
            ).fetchone()
            if existing:
                return existing[0]

            max_label = conn.execute(
                "SELECT MAX(label) FROM persons"
            ).fetchone()[0]
            label = (max_label + 1) if max_label is not None else 0

            conn.execute(
                "INSERT INTO persons (name, label, registered, sample_count) VALUES (?,?,?,0)",
                (name, label, datetime.now().isoformat())
            )
            return label

    def get_person_by_label(self, label: int) -> Optional[Dict]:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT id, name, label, registered, sample_count FROM persons WHERE label=?",
                (label,)
            ).fetchone()
        if row:
            return {"id": row[0], "name": row[1], "label": row[2],
                    "registered": row[3], "sample_count": row[4]}
        return None

    def get_person_by_name(self, name: str) -> Optional[Dict]:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT id, name, label, registered, sample_count FROM persons WHERE name=?",
                (name,)
            ).fetchone()
        if row:
            return {"id": row[0], "name": row[1], "label": row[2],
                    "registered": row[3], "sample_count": row[4]}
        return None

    def list_persons(self) -> List[Dict]:
        with self._conn() as conn:
            rows = conn.execute(
                "SELECT id, name, label, registered, sample_count FROM persons ORDER BY label"
            ).fetchall()
        return [{"id": r[0], "name": r[1], "label": r[2],
                 "registered": r[3], "sample_count": r[4]} for r in rows]

    def increment_sample_count(self, name: str, count: int = 1):
        with self._conn() as conn:
            conn.execute(
                "UPDATE persons SET sample_count = sample_count + ? WHERE name=?",
                (count, name)
            )

    def delete_person(self, name: str):
        with self._conn() as conn:
            conn.execute("DELETE FROM embeddings WHERE person_id=(SELECT id FROM persons WHERE name=?)", (name,))
            conn.execute("DELETE FROM persons WHERE name=?", (name,))

    # ── Label Map ──────────────────────────────────────────────────
    def get_label_map(self) -> Dict[int, str]:
        """Returns {label: name} for all persons."""
        return {p['label']: p['name'] for p in self.list_persons()}

    def save_label_map(self):
        with open(self.cfg.label_map_path, 'wb') as f:
            pickle.dump(self.get_label_map(), f)

    def load_label_map(self) -> Dict[int, str]:
        if not os.path.exists(self.cfg.label_map_path):
            return self.get_label_map()
        with open(self.cfg.label_map_path, 'rb') as f:
            return pickle.load(f)

    # ── Embeddings ─────────────────────────────────────────────────
    def save_embeddings(self, person_name: str, embeddings: list):
        person = self.get_person_by_name(person_name)
        if not person:
            return
        with self._conn() as conn:
            for emb in embeddings:
                conn.execute(
                    "INSERT INTO embeddings (person_id, embedding, created) VALUES (?,?,?)",
                    (person['id'], pickle.dumps(emb), datetime.now().isoformat())
                )

    def load_all_embeddings(self) -> Dict[str, list]:
        """Returns {name: [embedding, ...]}"""
        result = {}
        with self._conn() as conn:
            rows = conn.execute("""
                SELECT p.name, e.embedding
                FROM embeddings e
                JOIN persons p ON e.person_id = p.id
            """).fetchall()
        for name, emb_blob in rows:
            result.setdefault(name, []).append(pickle.loads(emb_blob))
        return result

    # ── Recognition Log ───────────────────────────────────────────
    def log_recognition(self, name: str, confidence: float,
                        source: str = "camera", spoof: bool = False):
        with self._conn() as conn:
            conn.execute(
                "INSERT INTO recognition_log (person_name, confidence, timestamp, source, spoof) VALUES (?,?,?,?,?)",
                (name, confidence, datetime.now().isoformat(), source, int(spoof))
            )

    def get_recognition_stats(self) -> Dict:
        with self._conn() as conn:
            total = conn.execute("SELECT COUNT(*) FROM recognition_log").fetchone()[0]
            known = conn.execute(
                "SELECT COUNT(*) FROM recognition_log WHERE person_name != 'Unknown'"
            ).fetchone()[0]
            spoofs = conn.execute(
                "SELECT COUNT(*) FROM recognition_log WHERE spoof=1"
            ).fetchone()[0]
            top = conn.execute("""
                SELECT person_name, COUNT(*) as cnt
                FROM recognition_log
                WHERE person_name != 'Unknown'
                GROUP BY person_name
                ORDER BY cnt DESC LIMIT 5
            """).fetchall()
            recent = conn.execute("""
                SELECT person_name, confidence, timestamp
                FROM recognition_log
                ORDER BY id DESC LIMIT 10
            """).fetchall()

        return {
            "total_recognitions":   total,
            "known_recognitions":   known,
            "unknown_recognitions": total - known,
            "spoof_attempts":       spoofs,
            "top_persons":          [{"name": r[0], "count": r[1]} for r in top],
            "recent_events":        [{"name": r[0], "confidence": r[1], "time": r[2]} for r in recent],
            "registered_persons":   len(self.list_persons()),
        }
"""Progress tracking store for PPP runs."""

import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime


class ProgressStore:
    """SQLite-backed progress store for PPP runs."""

    def __init__(self, db_path: str = "data/ppp_progress.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Runs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS runs (
                    run_id TEXT PRIMARY KEY,
                    agent_id TEXT NOT NULL,
                    policy_id TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    completed_at TEXT,
                    status TEXT NOT NULL,
                    config_hash TEXT
                )
            """)
            
            # Phases table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS phases (
                    phase_id TEXT PRIMARY KEY,
                    run_id TEXT NOT NULL,
                    phase_name TEXT NOT NULL,
                    started_at TEXT,
                    completed_at TEXT,
                    status TEXT NOT NULL,
                    FOREIGN KEY(run_id) REFERENCES runs(run_id)
                )
            """)
            
            # Checkpoints table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS checkpoints (
                    checkpoint_id TEXT PRIMARY KEY,
                    run_id TEXT NOT NULL,
                    phase_name TEXT NOT NULL,
                    checkpoint_data TEXT,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(run_id) REFERENCES runs(run_id)
                )
            """)
            
            conn.commit()

    def begin_run(
        self,
        run_id: str,
        agent_id: str,
        policy_id: str,
        config_hash: str = None,
    ) -> bool:
        """Begin a new run."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO runs (run_id, agent_id, policy_id, started_at, status, config_hash)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (run_id, agent_id, policy_id, datetime.utcnow().isoformat() + "Z", "in_progress", config_hash))
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def start_phase(self, run_id: str, phase_name: str, phase_id: str = None) -> str:
        """Start a phase within a run."""
        phase_id = phase_id or f"{run_id}_{phase_name}_{datetime.utcnow().isoformat()}"
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO phases (phase_id, run_id, phase_name, started_at, status)
                VALUES (?, ?, ?, ?, ?)
            """, (phase_id, run_id, phase_name, datetime.utcnow().isoformat() + "Z", "in_progress"))
            conn.commit()
        
        return phase_id

    def complete_phase(self, phase_id: str, status: str = "completed") -> bool:
        """Mark a phase as complete."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE phases
                    SET completed_at = ?, status = ?
                    WHERE phase_id = ?
                """, (datetime.utcnow().isoformat() + "Z", status, phase_id))
                conn.commit()
            return True
        except Exception:
            return False

    def checkpoint(
        self,
        run_id: str,
        phase_name: str,
        checkpoint_data: str,
        checkpoint_id: str = None,
    ) -> str:
        """Save a checkpoint."""
        checkpoint_id = checkpoint_id or f"{run_id}_{phase_name}_{datetime.utcnow().isoformat()}"
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO checkpoints (checkpoint_id, run_id, phase_name, checkpoint_data, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (checkpoint_id, run_id, phase_name, checkpoint_data, datetime.utcnow().isoformat() + "Z"))
            conn.commit()
        
        return checkpoint_id

    def get_last_checkpoint(self, run_id: str, phase_name: str) -> Optional[Dict[str, Any]]:
        """Get the last checkpoint for a run/phase."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT checkpoint_id, checkpoint_data, created_at
                FROM checkpoints
                WHERE run_id = ? AND phase_name = ?
                ORDER BY created_at DESC
                LIMIT 1
            """, (run_id, phase_name))
            row = cursor.fetchone()
            
            if row:
                return {
                    "checkpoint_id": row[0],
                    "data": row[1],
                    "created_at": row[2],
                }
        return None

    def get_run_status(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Get run status."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT run_id, agent_id, policy_id, started_at, completed_at, status
                FROM runs
                WHERE run_id = ?
            """, (run_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    "run_id": row[0],
                    "agent_id": row[1],
                    "policy_id": row[2],
                    "started_at": row[3],
                    "completed_at": row[4],
                    "status": row[5],
                }
        return None

    def complete_run(self, run_id: str, status: str = "completed") -> bool:
        """Mark run as complete."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE runs
                    SET completed_at = ?, status = ?
                    WHERE run_id = ?
                """, (datetime.utcnow().isoformat() + "Z", status, run_id))
                conn.commit()
            return True
        except Exception:
            return False

    def list_runs(self) -> list:
        """List all runs."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT run_id, agent_id, policy_id, started_at, status FROM runs ORDER BY started_at DESC")
            rows = cursor.fetchall()
            return [
                {
                    "run_id": row[0],
                    "agent_id": row[1],
                    "policy_id": row[2],
                    "started_at": row[3],
                    "status": row[4],
                }
                for row in rows
            ]

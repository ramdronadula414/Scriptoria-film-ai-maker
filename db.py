"""
db.py — SQLite persistence layer for Scriptoria AI.

Keeps the original `users` / `outputs` tables (for backwards compatibility
with any existing database.db files) and adds a richer `projects` table
that powers the new Dashboard, Script Generator, Camera Angle Generator,
Scene Breakdown, Storyboard and Character features.
"""

import sqlite3
import json
from datetime import datetime

DB_PATH = "database.db"


def get_connection():
    """Create a new connection (safe for Streamlit's multi-threaded reruns)."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    c = conn.cursor()

    # --- Legacy tables (kept for backward compatibility) -------------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS outputs(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            content TEXT,
            created_at TEXT
        )
    """)

    # --- Export log (powers the "Exports Completed" dashboard stat) --------
    c.execute("""
        CREATE TABLE IF NOT EXISTS export_log(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            project_id INTEGER,
            format TEXT,
            created_at TEXT
        )
    """)

    # --- New, richer project table -----------------------------------------
    c.execute("""
        CREATE TABLE IF NOT EXISTS projects(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            title TEXT,
            idea TEXT,
            genre TEXT,
            duration TEXT,
            audience TEXT,
            mood TEXT,
            language TEXT,
            video_style TEXT,
            output_type TEXT,
            script TEXT,
            camera_angles TEXT,
            scene_breakdown TEXT,
            storyboard TEXT,
            characters TEXT,
            created_at TEXT,
            updated_at TEXT
        )
    """)

    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# USERS
# ---------------------------------------------------------------------------

def get_user_by_credentials(email, password_hash):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM users WHERE email=? AND password=?", (email, password_hash)
    ).fetchone()
    conn.close()
    return row


def create_user(username, email, password_hash):
    conn = get_connection()
    conn.execute(
        "INSERT INTO users(username, email, password) VALUES(?,?,?)",
        (username, email, password_hash),
    )
    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    conn.close()
    return row


# ---------------------------------------------------------------------------
# PROJECTS
# ---------------------------------------------------------------------------

def create_project(user_email, meta, script_text):
    """Insert a new project row and return its id."""
    conn = get_connection()
    now = datetime.now().isoformat(timespec="seconds")
    cur = conn.execute(
        """INSERT INTO projects(
            user_email, title, idea, genre, duration, audience, mood,
            language, video_style, output_type, script,
            camera_angles, scene_breakdown, storyboard, characters,
            created_at, updated_at
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            user_email, meta.get("title"), meta.get("idea"), meta.get("genre"),
            meta.get("duration"), meta.get("audience"), meta.get("mood"),
            meta.get("language"), meta.get("video_style"), meta.get("output_type"),
            script_text, "", "", "", "", now, now,
        ),
    )
    conn.commit()
    project_id = cur.lastrowid
    conn.close()
    return project_id


def update_project_field(project_id, field, value):
    """Update a single JSON/text field (e.g. camera_angles, scene_breakdown)."""
    assert field in {
        "script", "camera_angles", "scene_breakdown", "storyboard", "characters",
        "title",
    }
    conn = get_connection()
    now = datetime.now().isoformat(timespec="seconds")
    conn.execute(
        f"UPDATE projects SET {field}=?, updated_at=? WHERE id=?",
        (value, now, project_id),
    )
    conn.commit()
    conn.close()


def get_project(project_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM projects WHERE id=?", (project_id,)).fetchone()
    conn.close()
    return row


def get_projects_for_user(user_email, limit=50):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM projects WHERE user_email=? ORDER BY id DESC LIMIT ?",
        (user_email, limit),
    ).fetchall()
    conn.close()
    return rows


def get_stats_for_user(user_email):
    conn = get_connection()
    row = conn.execute(
        """SELECT
            COUNT(*) AS total_projects,
            SUM(CASE WHEN script IS NOT NULL AND script != '' THEN 1 ELSE 0 END) AS scripts,
            SUM(CASE WHEN scene_breakdown IS NOT NULL AND scene_breakdown != '' THEN 1 ELSE 0 END) AS scenes,
            SUM(CASE WHEN characters IS NOT NULL AND characters != '' THEN 1 ELSE 0 END) AS characters
           FROM projects WHERE user_email=?""",
        (user_email,),
    ).fetchone()
    conn.close()
    stats = dict(row) if row else {"total_projects": 0, "scripts": 0, "scenes": 0, "characters": 0}
    stats["exports"] = count_exports(user_email)
    return stats


def log_export(user_email, project_id, fmt):
    conn = get_connection()
    now = datetime.now().isoformat(timespec="seconds")
    conn.execute(
        "INSERT INTO export_log(user_email, project_id, format, created_at) VALUES (?,?,?,?)",
        (user_email, project_id, fmt, now),
    )
    conn.commit()
    conn.close()


def count_exports(user_email):
    conn = get_connection()
    row = conn.execute(
        "SELECT COUNT(*) AS n FROM export_log WHERE user_email=?", (user_email,)
    ).fetchone()
    conn.close()
    return row["n"] if row else 0


def safe_json_loads(text, default=None):
    if not text:
        return default
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return default

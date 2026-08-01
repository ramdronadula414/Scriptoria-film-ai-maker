"""
app.py — Scriptoria AI: Premium Cinematic AI Film Pre-Production Studio.

This is the main entry point. It wires together:
  db.py            - SQLite persistence (users + projects)
  styles.py        - premium cinematic CSS theme (glassmorphism, gold/navy)
  ai_engine.py      - Gemini prompt construction + generation
  auth.py          - premium login / signup / guest screen
  components.py    - sidebar navigation + shared UI widgets
  pages_*.py       - Dashboard, Script Generator, Camera Angles, Scene
                     Breakdown, Storyboard, Characters, Export, Settings,
                     Profile, About

Everything is plain Streamlit — no external HTML/CSS/JS files, per project
constraints. All original functionality (auth, Gemini script generation,
TXT/PDF/DOCX export, generation history) is preserved and extended.
"""

import streamlit as st

import db
import ai_engine
from styles import inject_global_css
from components import render_sidebar
import auth
import pages_dashboard
import pages_generator
import pages_camera
import pages_scene
import pages_storyboard
import pages_characters
import pages_export
import pages_settings
import pages_misc

# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Scriptoria AI", page_icon="🎬", layout="wide")

# ---------------------------------------------------------------------------
# INITIALIZATION
# ---------------------------------------------------------------------------
db.init_db()
ai_engine.configure(st.secrets["GEMINI_API_KEY"])

if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# ---------------------------------------------------------------------------
# THEME (settings-aware, with sensible defaults before Settings page is visited)
# ---------------------------------------------------------------------------
inject_global_css(
    animations_enabled=st.session_state.get("settings_animations", True),
    font_scale=st.session_state.get("settings_font_scale", 1.0),
)

# ---------------------------------------------------------------------------
# ROUTING
# ---------------------------------------------------------------------------
PAGE_RENDERERS = {
    "Dashboard": pages_dashboard.render,
    "Script Generator": pages_generator.render,
    "Camera Angles": pages_camera.render,
    "Scene Breakdown": pages_scene.render,
    "Storyboard": pages_storyboard.render,
    "Characters": pages_characters.render,
    "Export": pages_export.render,
    "Settings": pages_settings.render,
    "Profile": pages_misc.render_profile,
    "About": pages_misc.render_about,
}

if st.session_state.user:
    render_sidebar()
    renderer = PAGE_RENDERERS.get(st.session_state.page, pages_dashboard.render)
    renderer()
else:
    auth.login_page()

"""
pages_settings.py — Settings page: theme, typography, animation toggle,
AI model selection, default language, export preferences, default camera style.
"""

import streamlit as st
from styles import glass_open, glass_close
from components import page_header

MODEL_OPTIONS = ["gemini-2.5-flash", "gemini-2.5-pro"]
LANGUAGES = ["English", "Hindi", "Telugu"]
EXPORT_FORMATS = ["TXT", "Markdown", "JSON", "PDF", "DOCX"]
CAMERA_STYLES = ["Short Film", "YouTube Short", "Instagram Reel", "TikTok Video",
                  "Advertisement", "Trailer", "Documentary"]


def _default(key, value):
    if key not in st.session_state:
        st.session_state[key] = value


def render():
    page_header("⚙️ Settings", "Personalize your Scriptoria experience")

    _default("settings_animations", True)
    _default("settings_font_scale", 1.0)
    _default("settings_ai_model", MODEL_OPTIONS[0])
    _default("settings_default_language", "English")
    _default("settings_default_export", "PDF")
    _default("settings_default_camera_style", "Short Film")

    glass_open()
    st.markdown("#### 🎨 Appearance")
    st.session_state.settings_animations = st.toggle(
        "Enable animations & glow effects", value=st.session_state.settings_animations
    )
    st.session_state.settings_font_scale = st.slider(
        "Font size", min_value=0.85, max_value=1.3, step=0.05,
        value=st.session_state.settings_font_scale,
    )
    glass_close()

    glass_open()
    st.markdown("#### 🤖 AI Preferences")
    st.session_state.settings_ai_model = st.selectbox(
        "AI Model", MODEL_OPTIONS,
        index=MODEL_OPTIONS.index(st.session_state.settings_ai_model),
    )
    st.session_state.settings_default_language = st.selectbox(
        "Default Language", LANGUAGES,
        index=LANGUAGES.index(st.session_state.settings_default_language),
    )
    st.session_state.settings_default_camera_style = st.selectbox(
        "Default Camera Style", CAMERA_STYLES,
        index=CAMERA_STYLES.index(st.session_state.settings_default_camera_style),
    )
    glass_close()

    glass_open()
    st.markdown("#### 📤 Export Preferences")
    st.session_state.settings_default_export = st.selectbox(
        "Default Export Format", EXPORT_FORMATS,
        index=EXPORT_FORMATS.index(st.session_state.settings_default_export),
    )
    glass_close()

    st.success("Settings are applied instantly and saved for this session.")

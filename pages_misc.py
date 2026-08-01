"""
pages_misc.py — Profile and About pages.
"""

import streamlit as st
import db
from styles import glass_open, glass_close
from components import page_header, stat_card


def render_profile():
    page_header("👤 Profile", "Your Scriptoria account")

    glass_open()
    st.write(f"**Email:** {st.session_state.user}")
    st.write(f"**Account type:** {'Guest' if st.session_state.get('is_guest') else 'Registered'}")
    glass_close()

    stats = db.get_stats_for_user(st.session_state.user)
    c1, c2, c3 = st.columns(3)
    with c1:
        stat_card("Total Projects", stats.get("total_projects") or 0, "🎬")
    with c2:
        stat_card("Scripts", stats.get("scripts") or 0, "📝")
    with c3:
        stat_card("Character Sets", stats.get("characters") or 0, "🧑‍🎤")


def render_about():
    page_header("ℹ️ About Scriptoria AI", "The premium AI film pre-production studio")

    glass_open()
    st.markdown(
        """
        **Scriptoria AI** helps filmmakers, content creators and storytellers go from a
        single idea to a full pre-production package — screenplay, camera angles,
        scene breakdowns, storyboards, and character profiles — in minutes.

        **Features:**
        - AI Screenplay Generation
        - Camera Angle Generator
        - Scene Breakdown
        - Storyboard Planner
        - Character Profiles
        - Multilingual Output (English, Hindi, Telugu)
        - Export to TXT, Markdown, JSON, PDF & DOCX

        Built with Streamlit, Google Gemini, ReportLab and python-docx.
        """
    )
    glass_close()

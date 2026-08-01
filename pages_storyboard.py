"""
pages_storyboard.py — Storyboard Planner: generates visual storyboard cards.
"""

import json
import streamlit as st
import db
import ai_engine
from styles import glass_open, glass_close
from components import page_header, empty_state


def _get_active_script():
    pid = st.session_state.get("active_project_id")
    if pid:
        project = db.get_project(pid)
        if project:
            return project, project["script"]
    return None, st.session_state.get("current_script_text")


def render():
    page_header("🖼️ Storyboard Planner", "Visualize your film, scene by scene")

    project, script_text = _get_active_script()
    if not script_text:
        empty_state("Generate a script first in the Script Generator, then come back here.")
        return

    glass_open()
    st.write("Generate storyboard cards with visual description, color palette, "
              "lighting and composition notes for key scenes.")
    generate = st.button("🖼️ Generate Storyboard", use_container_width=True)
    glass_close()

    if generate:
        with st.spinner("Sketching the storyboard..."):
            try:
                cards = ai_engine.generate_storyboard(script_text)
                st.session_state["storyboard_data"] = cards
                if project:
                    db.update_project_field(project["id"], "storyboard", json.dumps(cards))
                st.success(f"✅ Created {len(cards)} storyboard cards.")
            except Exception as e:
                st.error(f"Generation failed: {e}")

    data = st.session_state.get("storyboard_data")
    if not data and project and project["storyboard"]:
        data = db.safe_json_loads(project["storyboard"], default=[])

    if not data:
        return

    cols = st.columns(2)
    for i, card in enumerate(data):
        with cols[i % 2]:
            glass_open()
            st.markdown(f"### 🎬 {card.get('scene_title', 'Untitled Scene')}")
            st.write(card.get("scene_summary", ""))
            st.write(f"**Visual:** {card.get('visual_description', '—')}")
            st.write(f"**Camera Angle:** {card.get('camera_angle', '—')}")
            st.write(f"**Color Palette:** {card.get('color_palette', '—')}")
            st.write(f"**Lighting:** {card.get('lighting', '—')}")
            st.write(f"**Composition:** {card.get('composition', '—')}")
            if card.get("notes"):
                st.caption(f"📝 {card.get('notes')}")
            glass_close()

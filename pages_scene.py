"""
pages_scene.py — Scene Breakdown page: location, time, characters, action,
emotion, dialogue, sound, music, lighting, props, costume, weather, notes.
"""

import json
import streamlit as st
import db
import ai_engine
from styles import glass_open, glass_close, chip
from components import page_header, empty_state


def _get_active_script():
    pid = st.session_state.get("active_project_id")
    if pid:
        project = db.get_project(pid)
        if project:
            return project, project["script"]
    return None, st.session_state.get("current_script_text")


def render():
    page_header("🎞️ Scene Breakdown", "Full production breakdown for every scene")

    project, script_text = _get_active_script()
    if not script_text:
        empty_state("Generate a script first in the Script Generator, then come back here.")
        return

    glass_open()
    st.write("Break the script down into a production-ready sheet: location, "
             "time of day, characters, props, costumes, weather and more.")
    generate = st.button("🎞️ Generate Scene Breakdown", use_container_width=True)
    glass_close()

    if generate:
        with st.spinner("Breaking down every scene..."):
            try:
                scenes = ai_engine.generate_scene_breakdown(script_text)
                st.session_state["scene_breakdown_data"] = scenes
                if project:
                    db.update_project_field(project["id"], "scene_breakdown", json.dumps(scenes))
                st.success(f"✅ Broke down {len(scenes)} scenes.")
            except Exception as e:
                st.error(f"Generation failed: {e}")

    data = st.session_state.get("scene_breakdown_data")
    if not data and project and project["scene_breakdown"]:
        data = db.safe_json_loads(project["scene_breakdown"], default=[])

    if not data:
        return

    for scene in data:
        with st.expander(f"🎬 Scene {scene.get('scene_number', '?')} — {scene.get('location', '')}"):
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"📍 **Location:** {scene.get('location', '—')}")
                st.write(f"🕐 **Time:** {scene.get('time_of_day', '—')}")
                st.write(f"🧍 **Characters:** {scene.get('characters', '—')}")
                st.write(f"🎭 **Action:** {scene.get('action', '—')}")
                st.write(f"💬 **Dialogue:** {scene.get('dialogue_summary', '—')}")
                st.write(f"🌦️ **Weather:** {scene.get('weather', '—')}")
            with c2:
                st.write(f"🔊 **Sound Effects:** {scene.get('sound_effects', '—')}")
                st.write(f"🎵 **Music:** {scene.get('background_music', '—')}")
                st.write(f"💡 **Lighting:** {scene.get('lighting', '—')}")
                st.write(f"🎒 **Props:** {scene.get('props', '—')}")
                st.write(f"👗 **Costume:** {scene.get('costume', '—')}")
            chip(f"Emotion: {scene.get('emotion', '—')}")
            chip(f"Camera Notes: {scene.get('camera_notes', '—')}", "blue")
            chip(f"Editing Notes: {scene.get('editing_notes', '—')}", "green")

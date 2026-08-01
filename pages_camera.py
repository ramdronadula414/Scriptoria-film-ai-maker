"""
pages_camera.py — NEW FEATURE: Camera Angle Generator.

Given a generated script, automatically produces a professional cinematic
shot list for every scene: camera angle, lens, movement, shot size, height,
subject position, lighting direction, emotion, purpose, transition & duration.
"""

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
    page_header("🎥 Camera Angle Generator", "Cinematic shot lists, generated scene by scene")

    project, script_text = _get_active_script()

    if not script_text:
        empty_state("Generate a script first in the Script Generator, then come back here.")
        return

    glass_open()
    st.write("Generate a full professional shot list — camera angle, lens, movement, "
             "lighting, emotion and more — for every scene in your script.")
    style = st.selectbox(
        "Target format",
        ["Short Film", "YouTube Short", "Instagram Reel", "TikTok Video",
         "Advertisement", "Trailer", "Documentary"],
        index=0,
    )
    generate = st.button("🎬 Generate Camera Angles", use_container_width=True)
    glass_close()

    if generate:
        with st.spinner("🎥 Directing your virtual camera crew..."):
            try:
                angles = ai_engine.generate_camera_angles(script_text, style)
                st.session_state["camera_angles_data"] = angles
                if project:
                    import json
                    db.update_project_field(project["id"], "camera_angles", json.dumps(angles))
                st.success(f"✅ Generated {len(angles)} shots.")
            except Exception as e:
                st.error(f"Generation failed: {e}")

    data = st.session_state.get("camera_angles_data")
    if not data and project and project["camera_angles"]:
        data = db.safe_json_loads(project["camera_angles"], default=[])

    if not data:
        return

    grouped = {}
    for shot in data:
        scene = shot.get("scene_number", "?")
        grouped.setdefault(scene, []).append(shot)

    for scene, shots in sorted(grouped.items(), key=lambda x: str(x[0])):
        st.subheader(f"🎬 Scene {scene}")
        for shot in shots:
            glass_open()
            st.markdown(f"**Shot {shot.get('shot_number', '?')} — {shot.get('camera_angle', '')}**")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.write(f"📷 Lens: {shot.get('lens_suggestion', '—')}")
                st.write(f"🎯 Shot Size: {shot.get('shot_size', '—')}")
                st.write(f"↕️ Camera Height: {shot.get('camera_height', '—')}")
            with c2:
                st.write(f"🎥 Movement: {shot.get('camera_movement', '—')}")
                st.write(f"🧍 Subject Position: {shot.get('subject_position', '—')}")
                st.write(f"💡 Lighting: {shot.get('lighting_direction', '—')}")
            with c3:
                st.write(f"🎭 Emotion: {shot.get('emotion', '—')}")
                st.write(f"🎬 Purpose: {shot.get('purpose', '—')}")
                st.write(f"⏱️ Duration: {shot.get('duration_seconds', '—')}s")
            chip(f"Transition: {shot.get('transition', '—')}", "blue")
            glass_close()

"""
pages_characters.py — Character Profile generator.
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
    page_header("🧑‍🎤 Character Profiles", "Deep character sheets for your cast")

    project, script_text = _get_active_script()
    if not script_text:
        empty_state("Generate a script first in the Script Generator, then come back here.")
        return

    glass_open()
    st.write("Generate full character profiles: appearance, personality, costume, "
             "voice, expression, body language and character arc.")
    generate = st.button("🧑‍🎤 Generate Character Profiles", use_container_width=True)
    glass_close()

    if generate:
        with st.spinner("Casting and building character profiles..."):
            try:
                characters = ai_engine.generate_characters(script_text)
                st.session_state["characters_data"] = characters
                if project:
                    db.update_project_field(project["id"], "characters", json.dumps(characters))
                st.success(f"✅ Built {len(characters)} character profiles.")
            except Exception as e:
                st.error(f"Generation failed: {e}")

    data = st.session_state.get("characters_data")
    if not data and project and project["characters"]:
        data = db.safe_json_loads(project["characters"], default=[])

    if not data:
        return

    cols = st.columns(2)
    for i, ch in enumerate(data):
        with cols[i % 2]:
            glass_open()
            st.markdown(f"### 🎭 {ch.get('name', 'Unnamed')}")
            st.caption(f"Age: {ch.get('age', '—')}")
            st.write(f"**Appearance:** {ch.get('appearance', '—')}")
            st.write(f"**Personality:** {ch.get('personality', '—')}")
            st.write(f"**Costume:** {ch.get('costume', '—')}")
            st.write(f"**Voice:** {ch.get('voice', '—')}")
            st.write(f"**Expression:** {ch.get('expression', '—')}")
            st.write(f"**Body Language:** {ch.get('body_language', '—')}")
            st.write(f"**Character Arc:** {ch.get('character_arc', '—')}")
            glass_close()

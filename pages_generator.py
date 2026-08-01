"""
pages_generator.py — Script Generator page.

Organizes inputs into sections (Story Idea, Genre, Duration, Target Audience,
Mood, Language, Video Style, Output Type) and supports Generate / Improve /
Regenerate / Save / Export actions, preserving the original Gemini-based
generation logic.
"""

import streamlit as st
import db
import ai_engine
from styles import glass_open, glass_close, divider
from components import page_header, empty_state


GENRES = ["Drama", "Comedy", "Thriller", "Horror", "Romance", "Sci-Fi", "Action", "Documentary", "Fantasy"]
DURATIONS = ["Under 1 min", "1-3 min", "3-10 min", "10-20 min", "Feature Length"]
AUDIENCES = ["General", "Kids", "Teens", "Young Adult", "Mature", "Family"]
MOODS = ["Uplifting", "Dark", "Suspenseful", "Whimsical", "Romantic", "Gritty", "Inspirational"]
LANGUAGES = ["English", "Hindi", "Telugu"]
VIDEO_STYLES = ["Short Film", "YouTube Short", "Instagram Reel", "TikTok Video", "Advertisement", "Trailer", "Documentary"]
OUTPUT_TYPES = ["Full Package", "Script Only", "Treatment"]


def _load_active_project():
    pid = st.session_state.get("active_project_id")
    if pid:
        return db.get_project(pid)
    return None


def render():
    page_header("📝 Script Generator", "Turn your story idea into a full cinematic pre-production package")

    project = _load_active_project()

    glass_open()
    st.markdown("#### 🎯 Story Basics")
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("Project Title", value=(project["title"] if project else ""))
        genre = st.selectbox("Genre", GENRES, index=GENRES.index(project["genre"]) if project and project["genre"] in GENRES else 0)
        duration = st.selectbox("Duration", DURATIONS, index=DURATIONS.index(project["duration"]) if project and project["duration"] in DURATIONS else 0)
        audience = st.selectbox("Target Audience", AUDIENCES, index=AUDIENCES.index(project["audience"]) if project and project["audience"] in AUDIENCES else 0)
    with col2:
        mood = st.selectbox("Mood", MOODS, index=MOODS.index(project["mood"]) if project and project["mood"] in MOODS else 0)
        language = st.selectbox("Language", LANGUAGES, index=LANGUAGES.index(project["language"]) if project and project["language"] in LANGUAGES else 0)
        video_style = st.selectbox("Video Style", VIDEO_STYLES, index=VIDEO_STYLES.index(project["video_style"]) if project and project["video_style"] in VIDEO_STYLES else 0)
        output_type = st.selectbox("Output Type", OUTPUT_TYPES, index=OUTPUT_TYPES.index(project["output_type"]) if project and project["output_type"] in OUTPUT_TYPES else 0)

    idea = st.text_area("Story Idea", value=(project["idea"] if project else ""), height=140,
                         placeholder="Describe your story idea, premise, or logline...")
    glass_close()

    meta = {
        "title": title, "idea": idea, "genre": genre, "duration": duration,
        "audience": audience, "mood": mood, "language": language,
        "video_style": video_style, "output_type": output_type,
    }

    b1, b2, b3, b4 = st.columns(4)
    generate_clicked = b1.button("🎬 Generate Script", use_container_width=True)
    improve_clicked = b2.button("✨ Improve Script", use_container_width=True)
    regenerate_clicked = b3.button("🔄 Regenerate", use_container_width=True)
    save_clicked = b4.button("💾 Save", use_container_width=True)

    script_key = "current_script_text"

    if generate_clicked or regenerate_clicked:
        if not title or not idea:
            st.error("Please provide both a Project Title and a Story Idea.")
        else:
            with st.spinner("🎥 Generating your cinematic package..."):
                try:
                    script_text = ai_engine.generate_script(meta)
                    st.session_state[script_key] = script_text
                    project_id = db.create_project(st.session_state.user, meta, script_text)
                    st.session_state.active_project_id = project_id
                    st.success("✅ Script package generated successfully.")
                except Exception as e:
                    st.error(f"Generation failed: {e}")

    if improve_clicked:
        existing = st.session_state.get(script_key) or (project["script"] if project else "")
        if not existing:
            st.warning("Generate a script first before improving it.")
        else:
            notes = st.session_state.get("improve_notes", "Make it more cinematic and emotionally resonant.")
            with st.spinner("Refining your script..."):
                try:
                    improved = ai_engine.improve_script(existing, notes)
                    st.session_state[script_key] = improved
                    if st.session_state.get("active_project_id"):
                        db.update_project_field(st.session_state.active_project_id, "script", improved)
                    st.success("✅ Script improved.")
                except Exception as e:
                    st.error(f"Improvement failed: {e}")

    st.text_input("Improvement notes (used by ✨ Improve Script)", key="improve_notes",
                   value="Make it more cinematic and emotionally resonant.")

    if save_clicked and st.session_state.get("active_project_id"):
        db.update_project_field(st.session_state.active_project_id, "title", title)
        st.success("💾 Project saved.")

    divider()

    output = st.session_state.get(script_key) or (project["script"] if project else None)

    if output:
        st.subheader(f"🎬 {title or 'Untitled Project'}")
        glass_open()
        st.markdown(output)
        glass_close()

        st.caption("Next steps: use the sidebar to generate Camera Angles, Scene Breakdown, "
                   "Storyboard or Characters from this script, or head to Export.")
    else:
        empty_state("Fill in your story basics above and click 🎬 Generate Script to begin.")

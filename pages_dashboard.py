"""
pages_dashboard.py — Premium dashboard: welcome banner, stats, recent
projects (with cover thumbnails), and quick actions — matching the
Scriptoria mockup layout.
"""

import streamlit as st
import db
from styles import glass_open, glass_close, divider
from components import page_header, stat_card, project_card, quick_action_card

VISIBLE_PROJECTS_DEFAULT = 3


def _go_to(page_name, project_id=None):
    if project_id is not None:
        st.session_state.active_project_id = project_id
    st.session_state.page = page_name
    st.rerun()


def render():
    page_header("Dashboard")

    # --------------------------------------------------------------- HERO
    glass_open()
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            f"""
            <p style="color:rgba(245,230,200,0.65);margin-bottom:2px;">Welcome back,</p>
            <h2 style="color:#D4AF37;margin:0 0 8px 0;font-weight:800;">{st.session_state.user}</h2>
            <p style="color:rgba(245,230,200,0.8);">Let's create something amazing today! 🚀</p>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div style="height:120px;border-radius:14px;display:flex;align-items:center;
                        justify-content:center;font-size:3rem;
                        background:radial-gradient(circle,rgba(212,175,55,0.22),rgba(212,175,55,0) 70%);">
                🎥
            </div>
            """,
            unsafe_allow_html=True,
        )
    glass_close()

    # ---------------------------------------------------------- OVERVIEW
    st.markdown("#### Overview")
    stats = db.get_stats_for_user(st.session_state.user)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        stat_card("Scripts Generated", stats.get("scripts") or 0, "📄", "violet")
    with c2:
        stat_card("Scenes Generated", stats.get("scenes") or 0, "🎬", "green")
    with c3:
        stat_card("Characters Created", stats.get("characters") or 0, "👥", "amber")
    with c4:
        stat_card("Exports Completed", stats.get("exports") or 0, "⬆️", "blue")

    divider()

    # ---------------------------------------------------- RECENT PROJECTS
    header_col, link_col = st.columns([4, 1])
    with header_col:
        st.markdown("#### Recent Projects")
    with link_col:
        show_all = st.session_state.get("dashboard_show_all_projects", False)
        if st.button("View all →" if not show_all else "Show less", key="view_all_projects"):
            st.session_state.dashboard_show_all_projects = not show_all
            st.rerun()

    limit = 50 if show_all else VISIBLE_PROJECTS_DEFAULT
    projects = db.get_projects_for_user(st.session_state.user, limit=limit)

    if not projects:
        glass_open()
        st.markdown(
            "<div style='text-align:center;padding:20px;'>"
            "<div style='font-size:2.4rem;'>🎬</div>"
            "<p style='color:rgba(245,230,200,0.7);'>No projects yet — head to Script Generator "
            "to create your first one.</p></div>",
            unsafe_allow_html=True,
        )
        glass_close()
    else:
        cols = st.columns(3)
        for i, p in enumerate(projects):
            scene_data = db.safe_json_loads(p["scene_breakdown"], default=[])
            subtitle = f"{len(scene_data)} scenes" if scene_data else "Not yet broken down"
            with cols[i % 3]:
                project_card(p["title"] or "Untitled Project", subtitle, seed=f"scriptoria-{p['id']}")
                if st.button("Open", key=f"open_project_{p['id']}", use_container_width=True):
                    _go_to("Script Generator", project_id=p["id"])

    divider()

    # ------------------------------------------------------- QUICK ACTIONS
    st.markdown("#### Quick Actions")
    qc1, qc2, qc3, qc4 = st.columns(4)
    with qc1:
        quick_action_card("✨", "New Script", "Generate a new script")
        if st.button("Go", key="qa_new_script", use_container_width=True):
            st.session_state.active_project_id = None
            _go_to("Script Generator")
    with qc2:
        quick_action_card("📷", "Camera Angles", "Plan cinematic shots")
        if st.button("Go", key="qa_camera", use_container_width=True):
            _go_to("Camera Angles")
    with qc3:
        quick_action_card("📋", "Scene Breakdown", "Break down your scenes")
        if st.button("Go", key="qa_scene", use_container_width=True):
            _go_to("Scene Breakdown")
    with qc4:
        quick_action_card("⬆️", "Export Project", "Export your project")
        if st.button("Go", key="qa_export", use_container_width=True):
            _go_to("Export")

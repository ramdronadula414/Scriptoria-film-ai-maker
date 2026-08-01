"""
components.py — Reusable, small UI pieces shared across pages.
"""

import streamlit as st
from streamlit_option_menu import option_menu
from styles import glass_open, glass_close

# (page name, bootstrap-icon name)
NAV_ITEMS = [
    ("Dashboard", "grid-1x2-fill"),
    ("Script Generator", "pencil-square"),
    ("Camera Angles", "camera-fill"),
    ("Scene Breakdown", "list-ul"),
    ("Storyboard", "images"),
    ("Characters", "people-fill"),
    ("Export", "upload"),
    ("Settings", "gear-fill"),
    ("Profile", "person-circle"),
    ("About", "info-circle"),
]


def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align:center;padding:6px 0 18px 0;">
                <div style="font-size:2.6rem;line-height:1;">🎬</div>
                <div style="font-size:2rem;font-weight:800;margin-top:6px;
                            background:linear-gradient(90deg,#D4AF37,#F5E6C8 60%,#D4AF37);
                            -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
                    Scriptoria
                </div>
                <div style="color:rgba(245,230,200,0.55);font-size:0.8rem;
                            letter-spacing:2px;text-transform:uppercase;margin-top:-4px;">
                    AI Film Studio
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        labels = [name for name, _ in NAV_ITEMS]
        icons = [icon for _, icon in NAV_ITEMS]
        current = st.session_state.get("page", "Dashboard")
        default_index = labels.index(current) if current in labels else 0

        choice = option_menu(
            menu_title=None,
            options=labels,
            icons=icons,
            default_index=default_index,
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#D4AF37", "font-size": "16px"},
                "nav-link": {
                    "font-size": "15px",
                    "color": "#F5E6C8",
                    "text-align": "left",
                    "margin": "4px 0",
                    "padding": "12px 14px",
                    "border-radius": "10px",
                    "border": "1px solid transparent",
                    "--hover-color": "rgba(212,175,55,0.10)",
                },
                "nav-link-selected": {
                    "background-color": "rgba(212,175,55,0.14)",
                    "color": "#D4AF37",
                    "border": "1px solid rgba(212,175,55,0.55)",
                    "font-weight": "600",
                },
            },
        )
        st.session_state.page = choice

        st.markdown("<div style='margin-top:18px;'></div>", unsafe_allow_html=True)
        if st.button("🚪  Logout", use_container_width=True, key="sidebar_logout"):
            for key in ("user", "is_guest", "active_project_id", "page"):
                st.session_state.pop(key, None)
            st.rerun()


STAT_COLORS = {
    "violet": "#8B7CF6",
    "green": "#3FBF7F",
    "amber": "#D98A3D",
    "blue": "#4C9BE8",
}


def stat_card(label, value, icon, color="violet"):
    hex_color = STAT_COLORS.get(color, color)
    st.markdown(
        f"""
        <div class="glass-card fade-in stat-card">
            <div class="stat-icon" style="background:{hex_color}26;color:{hex_color};">{icon}</div>
            <div class="stat-text">
                <div class="stat-value">{value}</div>
                <div class="stat-label">{label}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def project_thumbnail(seed, height=140):
    """Deterministic decorative placeholder image for a project card."""
    return f"https://picsum.photos/seed/{seed}/500/{height * 2}"


def project_card(title, subtitle, seed):
    st.markdown(
        f"""
        <div class="glass-card fade-in project-card">
            <div class="project-thumb" style="background-image:url('{project_thumbnail(seed)}');"></div>
            <div class="project-info">
                <div class="project-title-row">
                    <span class="project-title">🎬 {title}</span>
                    <span class="project-kebab">⋮</span>
                </div>
                <div class="project-subtitle">{subtitle}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def quick_action_card(icon, title, subtitle):
    st.markdown(
        f"""
        <div class="glass-card fade-in quick-action-card">
            <div class="quick-action-icon">{icon}</div>
            <div class="quick-action-title">{title}</div>
            <div class="quick-action-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_header(title, subtitle=""):
    st.markdown(
        f"""
        <div class="page-header-row">
            <span class="page-header-hamburger">☰</span>
            <div>
                <h1 style="background:linear-gradient(90deg,#D4AF37,#F5E6C8);
                           -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                           font-weight:800;margin-bottom:0;display:inline-block;">{title}</h1>
                <p style="color:rgba(245,230,200,0.7);margin-top:2px;">{subtitle}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def empty_state(message, icon="🎬"):
    glass_open()
    st.markdown(
        f"<div style='text-align:center;padding:20px;'>"
        f"<div style='font-size:2.4rem;'>{icon}</div>"
        f"<p style='color:rgba(245,230,200,0.7);'>{message}</p></div>",
        unsafe_allow_html=True,
    )
    glass_close()

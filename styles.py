"""
styles.py — Premium cinematic dark/navy/gold theme for Scriptoria AI.

All styling is plain CSS injected through st.markdown(unsafe_allow_html=True).
No external HTML/CSS/JS files are used, per project constraints.
"""

import streamlit as st

GOLD = "#D4AF37"
CREAM = "#F5E6C8"


def inject_global_css(animations_enabled: bool = True, font_scale: float = 1.0):
    anim = "1" if animations_enabled else "0"
    st.markdown(
        f"""
        <style>
        :root {{
            --gold: {GOLD};
            --cream: {CREAM};
            --font-scale: {font_scale};
        }}

        html, body, [class*="css"] {{
            font-family: 'Segoe UI', 'Inter', sans-serif !important;
            font-size: calc(1rem * var(--font-scale));
        }}

        .stApp {{
            background: radial-gradient(circle at 15% 10%, #16324a 0%, #0b1622 45%, #05080d 100%);
            color: var(--cream);
        }}

        /* subtle animated glow blobs behind everything */
        .stApp::before {{
            content: "";
            position: fixed;
            top: -20%; left: -10%;
            width: 60vw; height: 60vw;
            background: radial-gradient(circle, rgba(212,175,55,0.10) 0%, rgba(212,175,55,0) 70%);
            z-index: 0;
            animation: {"floatGlow 14s ease-in-out infinite" if anim == "1" else "none"};
        }}

        @keyframes floatGlow {{
            0%,100% {{ transform: translate(0,0); }}
            50% {{ transform: translate(4%, 6%); }}
        }}

        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(14px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .fade-in {{
            animation: {"fadeInUp 0.55s ease-out" if anim == "1" else "none"};
        }}

        /* Glassmorphism card */
        .glass-card {{
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(212,175,55,0.25);
            border-radius: 18px;
            padding: 26px 28px;
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            box-shadow: 0 10px 35px rgba(0,0,0,0.45);
            margin-bottom: 20px;
            transition: transform 0.25s ease, box-shadow 0.25s ease;
        }}
        .glass-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 14px 45px rgba(212,175,55,0.15);
        }}

        /* Hero */
        .hero {{
            text-align: center;
            padding: 46px 20px 30px 20px;
        }}
        .hero h1 {{
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(90deg, var(--gold), var(--cream) 60%, var(--gold));
            background-size: 200% auto;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: {"shine 5s linear infinite" if anim == "1" else "none"};
            margin-bottom: 6px;
        }}
        @keyframes shine {{
            to {{ background-position: 200% center; }}
        }}
        .hero p {{
            color: rgba(245,230,200,0.75);
            font-size: 1.05rem;
            letter-spacing: 0.5px;
        }}

        .gradient-divider {{
            height: 2px;
            border: none;
            margin: 18px 0 26px 0;
            background: linear-gradient(90deg, transparent, var(--gold), transparent);
            background-size: 200% auto;
            animation: {"shine 4s linear infinite" if anim == "1" else "none"};
        }}

        /* Buttons */
        .stButton>button, .stDownloadButton>button {{
            border-radius: 10px !important;
            border: 1px solid var(--gold) !important;
            background: linear-gradient(135deg, rgba(212,175,55,0.18), rgba(212,175,55,0.05)) !important;
            color: var(--cream) !important;
            font-weight: 600 !important;
            padding: 0.55em 1.3em !important;
            transition: all 0.2s ease-in-out !important;
        }}
        .stButton>button:hover, .stDownloadButton>button:hover {{
            background: linear-gradient(135deg, var(--gold), #b8912c) !important;
            color: #0b1622 !important;
            box-shadow: 0 0 18px rgba(212,175,55,0.55);
            transform: translateY(-1px);
        }}

        /* Status chips */
        .chip {{
            display: inline-block;
            padding: 4px 14px;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 600;
            margin-right: 6px;
            border: 1px solid rgba(212,175,55,0.4);
            background: rgba(212,175,55,0.10);
            color: var(--gold);
        }}
        .chip.green {{ border-color: rgba(90,200,140,0.5); color: #7BE0A6; background: rgba(90,200,140,0.08); }}
        .chip.blue {{ border-color: rgba(100,170,240,0.5); color: #8FC4FA; background: rgba(100,170,240,0.08); }}

        /* Inputs */
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {{
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(212,175,55,0.3) !important;
            border-radius: 10px !important;
            color: var(--cream) !important;
        }}

        /* Sidebar */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #0c1a26, #060d14);
            border-right: 1px solid rgba(212,175,55,0.15);
        }}
        section[data-testid="stSidebar"] .stRadio label {{
            font-size: 1rem;
        }}

        /* Expander / storyboard cards */
        .stExpander {{
            border: 1px solid rgba(212,175,55,0.2) !important;
            border-radius: 14px !important;
            background: rgba(255,255,255,0.03) !important;
        }}

        hr {{ border-color: rgba(212,175,55,0.2); }}

        ::-webkit-scrollbar {{ width: 10px; }}
        ::-webkit-scrollbar-thumb {{ background: rgba(212,175,55,0.35); border-radius: 10px; }}
        ::-webkit-scrollbar-track {{ background: transparent; }}

        /* Page header row (hamburger + gradient title) */
        .page-header-row {{
            display: flex;
            align-items: flex-start;
            gap: 14px;
            margin-bottom: 6px;
        }}
        .page-header-hamburger {{
            font-size: 1.4rem;
            color: var(--gold);
            margin-top: 4px;
        }}

        /* Stat cards */
        .stat-card {{
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 20px 22px;
        }}
        .stat-icon {{
            width: 52px;
            height: 52px;
            min-width: 52px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
        }}
        .stat-value {{
            font-size: 1.9rem;
            font-weight: 800;
            color: var(--cream);
            line-height: 1.1;
        }}
        .stat-label {{
            color: rgba(245,230,200,0.65);
            font-size: 0.88rem;
        }}

        /* Project cards */
        .project-card {{
            padding: 0;
            overflow: hidden;
        }}
        .project-thumb {{
            width: 100%;
            height: 150px;
            background-size: cover;
            background-position: center;
        }}
        .project-info {{
            padding: 14px 18px 18px 18px;
        }}
        .project-title-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .project-title {{
            font-weight: 700;
            color: var(--cream);
        }}
        .project-kebab {{
            color: rgba(245,230,200,0.5);
            font-weight: 800;
            cursor: default;
        }}
        .project-subtitle {{
            color: rgba(245,230,200,0.6);
            font-size: 0.85rem;
            margin-top: 4px;
        }}

        /* Quick action cards */
        .quick-action-card {{
            text-align: center;
            padding: 22px 16px;
        }}
        .quick-action-icon {{
            font-size: 1.6rem;
            margin-bottom: 8px;
        }}
        .quick-action-title {{
            font-weight: 700;
            color: var(--cream);
            margin-bottom: 4px;
        }}
        .quick-action-subtitle {{
            color: rgba(245,230,200,0.6);
            font-size: 0.82rem;
        }}

        /* streamlit-option-menu container tweaks */
        section[data-testid="stSidebar"] .nav {{
            gap: 2px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def glass_open():
    st.markdown('<div class="glass-card fade-in">', unsafe_allow_html=True)


def glass_close():
    st.markdown("</div>", unsafe_allow_html=True)


def divider():
    st.markdown('<hr class="gradient-divider" />', unsafe_allow_html=True)


def chip(label, kind=""):
    st.markdown(f'<span class="chip {kind}">{label}</span>', unsafe_allow_html=True)

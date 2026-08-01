"""
auth.py — Premium authentication screen: login, signup and guest mode.
Uses the same hashing / validation logic as the original app for
database compatibility, wrapped in the new cinematic UI.
"""

import re
import hashlib
import streamlit as st
import db
from styles import glass_open, glass_close, divider


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*]", password):
        return False
    return True


def password_strength(password):
    score = sum([
        len(password) >= 8,
        bool(re.search(r"[A-Z]", password)),
        bool(re.search(r"[a-z]", password)),
        bool(re.search(r"\d", password)),
        bool(re.search(r"[!@#$%^&*]", password)),
    ])
    labels = ["Very Weak", "Weak", "Fair", "Good", "Strong", "Excellent"]
    colors = ["#8a2c2c", "#a5432c", "#c99a2c", "#8fae3c", "#3ca85a", "#2c9e6a"]
    return labels[score], colors[score], score / 5


def _hero():
    st.markdown(
        """
        <div class="hero">
            <div style="font-size:3.2rem;">🎬</div>
            <h1>Scriptoria AI</h1>
            <p>The Premium AI Film Pre-Production Studio</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def login_page():
    _hero()

    _, center, _ = st.columns([1, 1.3, 1])
    with center:
        glass_open()
        tab_login, tab_signup = st.tabs(["🔐 Login", "✨ Sign Up"])

        # ------------------------------------------------------------ LOGIN
        with tab_login:
            email = st.text_input("Email", key="login_email", placeholder="you@example.com")
            password = st.text_input("Password", type="password", key="login_password")
            remember = st.checkbox("Remember me", value=True, key="remember_me")
            c1, c2 = st.columns(2)
            login_clicked = c1.button("Login", use_container_width=True, key="login_btn")
            c2.button("Forgot Password?", use_container_width=True, key="forgot_pw_btn")

            if st.session_state.get("forgot_pw_btn"):
                st.info("Password reset isn't wired up yet — this is a placeholder for a future release.")

            if login_clicked:
                if not email or not password:
                    st.error("Please enter both email and password.")
                else:
                    with st.spinner("Verifying credentials..."):
                        user = db.get_user_by_credentials(email, hash_password(password))
                    if user:
                        st.session_state.user = email
                        st.session_state.remember_me = remember
                        st.success("✅ Login successful — welcome back!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials. Please try again.")

            divider()
            if st.button("Continue as Guest", use_container_width=True, key="guest_btn"):
                st.session_state.user = "guest@scriptoria.ai"
                st.session_state.is_guest = True
                st.success("Continuing as guest — your work won't be saved permanently.")
                st.rerun()

        # ----------------------------------------------------------- SIGNUP
        with tab_signup:
            name = st.text_input("Full Name", key="signup_name")
            username = st.text_input("Username", key="signup_username")
            email_s = st.text_input("Email", key="signup_email")
            pw = st.text_input("Create Password", type="password", key="signup_password")
            confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")

            if pw:
                label, color, frac = password_strength(pw)
                st.markdown(
                    f"""
                    <div style="height:8px;background:rgba(255,255,255,0.08);border-radius:6px;overflow:hidden;margin:4px 0;">
                        <div style="width:{frac*100:.0f}%;height:100%;background:{color};"></div>
                    </div>
                    <span style="font-size:0.8rem;color:{color};">{label}</span>
                    """,
                    unsafe_allow_html=True,
                )

            terms = st.checkbox("I agree to the Terms & Conditions", key="terms_checkbox")

            if st.button("Create Account", use_container_width=True, key="signup_btn"):
                if not all([name, username, email_s, pw, confirm]):
                    st.error("Please fill in every field.")
                elif pw != confirm:
                    st.error("Passwords do not match.")
                elif not valid_password(pw):
                    st.error("Password must be 8+ characters with uppercase, lowercase, number & symbol.")
                elif not terms:
                    st.error("Please accept the Terms & Conditions to continue.")
                else:
                    try:
                        db.create_user(username, email_s, hash_password(pw))
                        st.success("🎉 Account created! Please log in from the Login tab.")
                    except Exception:
                        st.error("That email is already registered.")

        glass_close()

        st.markdown(
            "<p style='text-align:center;color:rgba(245,230,200,0.5);font-size:0.8rem;'>"
            "🎬 Scriptoria AI · Premium Cinematic Pre-Production Suite</p>",
            unsafe_allow_html=True,
        )

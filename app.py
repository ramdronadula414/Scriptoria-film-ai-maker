import streamlit as st
import sqlite3
import re
import hashlib
from datetime import datetime
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from docx import Document
import google.generativeai as genai

# -------------------------
# CONFIG
# -------------------------
st.set_page_config(page_title="Scriptoria AI", page_icon="🎬", layout="wide")

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# -------------------------
# DATABASE SETUP
# -------------------------
conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS outputs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT,
    content TEXT,
    created_at TEXT
)
""")

conn.commit()

# -------------------------
# PASSWORD HASH
# -------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -------------------------
# PASSWORD POLICY
# -------------------------
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

# -------------------------
# SESSION STATE
# -------------------------
if "user" not in st.session_state:
    st.session_state.user = None

# -------------------------
# STYLING
# -------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(120deg,#0f2027,#203a43,#2c5364);
    color:white;
}

.glass {
    background: rgba(255,255,255,0.08);
    padding:25px;
    border-radius:15px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
}

.center-box {
    max-width: 420px;
    margin: auto;
    margin-top: 80px;
}

button {
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# AUTH UI
# -------------------------
def login_page():
    st.markdown('<div class="glass center-box">', unsafe_allow_html=True)
    st.title("🎬 Scriptoria AI")
    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            c.execute("SELECT * FROM users WHERE email=? AND password=?",
                      (email, hash_password(password)))
            user = c.fetchone()
            if user:
                st.session_state.user = email
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        username = st.text_input("Username")
        email = st.text_input("Email ", key="signup_email")
        password = st.text_input("Create Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")

        if st.button("Create Account"):
            if password != confirm:
                st.error("Passwords do not match")
            elif not valid_password(password):
                st.error("Password must contain uppercase, lowercase, number & symbol")
            else:
                try:
                    c.execute("INSERT INTO users(username,email,password) VALUES(?,?,?)",
                              (username, email, hash_password(password)))
                    conn.commit()
                    st.success("Account created! Please login.")
                except:
                    st.error("Email already registered")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# MAIN APP
# -------------------------
def app_page():

    st.sidebar.success(f"Logged in as {st.session_state.user}")
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    st.title("🎬 Scriptoria AI")
    st.caption("AI Powered Film Pre-Production System")

    st.markdown('<div class="glass">', unsafe_allow_html=True)

    title = st.text_input("Enter Project Title")

    idea = st.text_area("Enter your story idea")

    language = st.selectbox("Select Language",
                            ["English", "Hindi", "Telugu"])

    generate = st.button("Generate Pre-Production Pack")

    st.markdown('</div>', unsafe_allow_html=True)

    def build_prompt(title, idea, language):
        return f"""
You are a professional screenwriter.

Project Title:
{title}

Story Idea:
{idea}

Generate in {language}.

Include:
SCREENPLAY
CHARACTERS
SOUND DESIGN
PRODUCTION PLAN
"""

    if generate and title and idea:
        with st.spinner("Generating cinematic package..."):
            response = model.generate_content(build_prompt(title, idea, language))
            output = response.text

        st.success("Generated Successfully")
        st.subheader(f"🎬 {title}") 
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown(output)
        st.markdown('</div>', unsafe_allow_html=True)

        # SAVE TO DATABASE
        c.execute("INSERT INTO outputs VALUES(NULL,?,?,?)",
                  (st.session_state.user, output, datetime.now()))
        conn.commit()

        # DOWNLOAD OPTIONS
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")

        st.download_button("Download TXT", output,
                           file_name="script.txt")

        # PDF
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer)
        styles = getSampleStyleSheet()

        elements = []
        for line in output.split("\n"):
            elements.append(Paragraph(line, styles["Normal"]))
            elements.append(Spacer(1,6))
        doc.build(elements)
        pdf_buffer.seek(0)

        st.download_button("Download PDF", pdf_buffer,
                           file_name="script.pdf")

        # DOCX
        docx_buffer = BytesIO()
        document = Document()
        for line in output.split("\n"):
            document.add_paragraph(line)
        document.save(docx_buffer)
        docx_buffer.seek(0)

        st.download_button("Download DOCX", docx_buffer,
                           file_name="script.docx")

    # SHOW HISTORY
    st.subheader("📜 Your Previous Generations")

    rows = c.execute(
        "SELECT content, created_at FROM outputs WHERE user_email=? ORDER BY id DESC",
        (st.session_state.user,)
    ).fetchall()

    for r in rows[:5]:
        with st.expander(f"Generated on {r[1]}"):
            st.write(r[0])


# -------------------------
# ROUTING
# -------------------------
if st.session_state.user:
    app_page()
else:
    login_page()
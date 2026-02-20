import streamlit as st
from google import genai
from datetime import datetime
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from docx import Document
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Scriptoria AI",
    page_icon="🎬",
    layout="wide"
)

# -----------------------------
# GEMINI CONFIG
# -----------------------------
# Set your API key as environment variable before running
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# -----------------------------
# UI STYLING
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(120deg,#0f2027,#203a43,#2c5364);
    color:white;
}
.glass {
    background: rgba(255,255,255,0.08);
    padding:20px;
    border-radius:15px;
    backdrop-filter: blur(10px);
}
</style>
""", unsafe_allow_html=True)

st.title("🎬 Scriptoria AI")
st.caption("Generative AI–Powered Film Pre-Production System")

# -----------------------------
# INPUT PANEL
# -----------------------------
with st.container():
    st.markdown('<div class="glass">', unsafe_allow_html=True)

    title = st.text_input("Project Title")

    idea = st.text_area("Enter your story idea")

    language = st.selectbox(
        "Select Language",
        ["English", "Hindi", "Telugu"]
    )

    generate = st.button("Generate Pre-Production Pack")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# PROMPT TEMPLATE
# -----------------------------
def build_prompt(title, idea, language):

    lang_rules = {
        "English": "Generate entirely in English.",
        "Hindi": "Generate entirely in Hindi (Devanagari script).",
        "Telugu": "Generate entirely in Telugu script."
    }

    return f"""
You are a professional screenwriter and film production planner.

Project Title:
{title}

Story Idea:
{idea}

Language Rules:
{lang_rules[language]}

Maintain narrative consistency.

OUTPUT STRUCTURE:

SCREENPLAY
(minimum 5 scenes, proper INT/EXT formatting)

CHARACTER PROFILES
(Name, age, background, motivation, conflict, arc)

SOUND DESIGN PLAN
(scene wise)

PRODUCTION PLAN
(location, props, costumes, shoot grouping)
"""

# -----------------------------
# GENERATION
# -----------------------------
if generate and idea and title:

    with st.spinner("Generating cinematic pre-production package..."):

        prompt = build_prompt(title, idea, language)
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt,
        )

        output = response.text
    st.success("Generation Complete")

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown(output)
    st.markdown('</div>', unsafe_allow_html=True)

    # -----------------------------
    # EXPORT FUNCTIONS
    # -----------------------------
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")

    # TXT
    st.download_button(
        "Download TXT",
        output,
        file_name=f"scriptoria_{timestamp}.txt"
    )

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

    st.download_button(
        "Download PDF",
        pdf_buffer,
        file_name=f"scriptoria_{timestamp}.pdf",
        mime="application/pdf"
    )

    # DOCX
    docx_buffer = BytesIO()
    document = Document()

    for line in output.split("\n"):
        document.add_paragraph(line)

    document.save(docx_buffer)
    docx_buffer.seek(0)

    st.download_button(
        "Download DOCX",
        docx_buffer,
        file_name=f"scriptoria_{timestamp}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
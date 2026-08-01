# 🎬 Scriptoria AI

**Premium AI-Powered Film Pre-Production Studio**

A cinematic, glassmorphic Streamlit application that takes a story idea from
concept to a full pre-production package — screenplay, camera angles, scene
breakdown, storyboard and character profiles — powered by Google Gemini.

## 🚀 Features

- **Premium Cinematic UI** — deep navy/gold glassmorphism theme, animated hero
  section, glowing dividers, status chips, hover animations — all built with
  pure Streamlit + injected CSS (no external HTML/CSS/JS files).
- **Redesigned Authentication** — animated login/signup with password
  strength meter, "Continue as Guest" mode, and validation, backed by the
  same SQLite schema as before.
- **Dashboard** — project stats, recent projects, quick actions, latest
  activity.
- **Script Generator** — sectioned inputs (idea, genre, duration, audience,
  mood, language, video style, output type) with Generate / Improve /
  Regenerate / Save actions.
- **🎥 Camera Angle Generator (NEW)** — automatically produces a full
  professional shot list per scene: camera angle, lens, movement, shot size,
  height, subject position, lighting, emotion, purpose, transition & duration.
  Supports Short Films, YouTube Shorts, Reels, TikTok, Ads, Trailers &
  Documentaries.
- **Scene Breakdown** — location, time, characters, action, dialogue, sound,
  music, lighting, props, costume, weather, camera & editing notes per scene.
- **Storyboard Planner** — visual storyboard cards with color palette,
  lighting and composition notes.
- **Character Profiles** — appearance, personality, costume, voice,
  expression, body language and character arc for every major character.
- **Export Center** — TXT, Markdown, JSON, PDF and DOCX, with premium
  formatted headers.
- **Settings** — theme animation toggle, font size, AI model selection,
  default language, default export format, default camera style.
- **Multilingual Output** — English, Hindi, Telugu.

## 🛠 Tech Stack

- Streamlit
- Python
- Google Gemini AI (`google-generativeai`)
- ReportLab (PDF export)
- python-docx (DOCX export)
- SQLite (local persistence)

## 📁 Project Structure

```
app.py                 # Entry point & page routing
db.py                  # SQLite schema & queries (users, projects)
styles.py              # Premium cinematic CSS theme
ai_engine.py           # Gemini prompt builders & generation calls
auth.py                # Login / Signup / Guest screen
components.py          # Sidebar nav & shared UI widgets
pages_dashboard.py      # Dashboard
pages_generator.py      # Script Generator
pages_camera.py          # Camera Angle Generator
pages_scene.py           # Scene Breakdown
pages_storyboard.py     # Storyboard Planner
pages_characters.py     # Character Profiles
pages_export.py          # Export Center
pages_settings.py        # Settings
pages_misc.py            # Profile & About
```

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Add your Gemini API key to `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "your-key-here"
```

## 👨‍💻 Author

Ramanjaneyulu Dronadula

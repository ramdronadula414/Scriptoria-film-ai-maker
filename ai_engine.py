"""
ai_engine.py — All Gemini prompt construction + generation calls live here,
kept separate from UI code for maintainability.
"""

import json
import re
import streamlit as st
import google.generativeai as genai

_MODEL_CACHE = {}


def get_model(model_name="gemini-2.5-flash"):
    """Cache GenerativeModel instances so we don't recreate them every rerun."""
    if model_name not in _MODEL_CACHE:
        _MODEL_CACHE[model_name] = genai.GenerativeModel(model_name)
    return _MODEL_CACHE[model_name]


def configure(api_key):
    genai.configure(api_key=api_key)


def _extract_json(text):
    """Gemini sometimes wraps JSON in ```json fences — strip and parse safely."""
    cleaned = re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Try to locate the first [...] or {...} block
        match = re.search(r"(\[.*\]|\{.*\})", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                return None
        return None


# ---------------------------------------------------------------------------
# SCRIPT GENERATION
# ---------------------------------------------------------------------------

def build_script_prompt(meta):
    return f"""
You are an award-winning professional screenwriter and film pre-production consultant.

Project Title: {meta.get('title')}
Story Idea: {meta.get('idea')}
Genre: {meta.get('genre')}
Target Duration: {meta.get('duration')}
Target Audience: {meta.get('audience')}
Mood/Tone: {meta.get('mood')}
Output Format: {meta.get('output_type')}
Visual Style: {meta.get('video_style')}
Language: {meta.get('language')}

Write the complete output in {meta.get('language')}.

Structure the response with these clearly labeled sections, in this order:

SCREENPLAY
(Full scene-by-scene screenplay in standard screenplay formatting, numbered scenes.)

CHARACTERS
(Brief profile for each major character.)

SOUND DESIGN
(Music mood, key sound effects, ambience per act.)

PRODUCTION PLAN
(Suggested shoot days, locations, budget tier, crew roles.)
"""


def generate_script(meta, model_name="gemini-2.5-flash"):
    model = get_model(model_name)
    response = model.generate_content(build_script_prompt(meta))
    return response.text


def improve_script(existing_script, instructions, model_name="gemini-2.5-flash"):
    model = get_model(model_name)
    prompt = f"""
You are revising an existing screenplay package. Keep the same overall structure
(SCREENPLAY, CHARACTERS, SOUND DESIGN, PRODUCTION PLAN) but improve it based on
these notes: {instructions}

EXISTING CONTENT:
{existing_script}

Return the full improved package with the same section headers.
"""
    response = model.generate_content(prompt)
    return response.text


# ---------------------------------------------------------------------------
# CAMERA ANGLE GENERATOR
# ---------------------------------------------------------------------------

def build_camera_angle_prompt(script_text, video_style):
    return f"""
You are a professional cinematographer. Based on the screenplay below, generate a
detailed shot list for every scene, tailored for: {video_style}.

Return ONLY valid JSON (no markdown fences, no commentary) as a list of objects,
one per shot, each with exactly these keys:
"scene_number", "shot_number", "camera_angle", "lens_suggestion",
"camera_movement", "shot_size", "camera_height", "subject_position",
"lighting_direction", "emotion", "purpose", "transition", "duration_seconds"

SCREENPLAY:
{script_text}
"""


def generate_camera_angles(script_text, video_style, model_name="gemini-2.5-flash"):
    model = get_model(model_name)
    response = model.generate_content(build_camera_angle_prompt(script_text, video_style))
    data = _extract_json(response.text)
    return data if data is not None else []


# ---------------------------------------------------------------------------
# SCENE BREAKDOWN
# ---------------------------------------------------------------------------

def build_scene_breakdown_prompt(script_text):
    return f"""
You are an assistant director producing a scene breakdown sheet. Based on the
screenplay below, return ONLY valid JSON (no markdown fences) as a list of
objects, one per scene, each with exactly these keys:
"scene_number", "location", "time_of_day", "characters", "action", "emotion",
"dialogue_summary", "sound_effects", "background_music", "lighting", "props",
"costume", "weather", "camera_notes", "editing_notes"

SCREENPLAY:
{script_text}
"""


def generate_scene_breakdown(script_text, model_name="gemini-2.5-flash"):
    model = get_model(model_name)
    response = model.generate_content(build_scene_breakdown_prompt(script_text))
    data = _extract_json(response.text)
    return data if data is not None else []


# ---------------------------------------------------------------------------
# STORYBOARD
# ---------------------------------------------------------------------------

def build_storyboard_prompt(script_text):
    return f"""
You are a storyboard artist. Based on the screenplay below, return ONLY valid
JSON (no markdown fences) as a list of objects, one card per key scene, each
with exactly these keys:
"scene_title", "scene_summary", "visual_description", "camera_angle",
"color_palette", "lighting", "composition", "notes"

SCREENPLAY:
{script_text}
"""


def generate_storyboard(script_text, model_name="gemini-2.5-flash"):
    model = get_model(model_name)
    response = model.generate_content(build_storyboard_prompt(script_text))
    data = _extract_json(response.text)
    return data if data is not None else []


# ---------------------------------------------------------------------------
# CHARACTER PROFILES
# ---------------------------------------------------------------------------

def build_character_prompt(script_text):
    return f"""
You are a casting director and character designer. Based on the screenplay
below, return ONLY valid JSON (no markdown fences) as a list of objects, one
per major character, each with exactly these keys:
"name", "age", "appearance", "personality", "costume", "voice", "expression",
"body_language", "character_arc"

SCREENPLAY:
{script_text}
"""


def generate_characters(script_text, model_name="gemini-2.5-flash"):
    model = get_model(model_name)
    response = model.generate_content(build_character_prompt(script_text))
    data = _extract_json(response.text)
    return data if data is not None else []

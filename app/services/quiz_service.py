import json
import os
import uuid
from typing import Dict, Tuple

from dotenv import load_dotenv
import google.genai as genai

from app.schemas.quiz import QuizQuestion, QuizSession

load_dotenv()

_sessions: Dict[str, QuizSession] = {}

_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

LIFE_STAGES = [
    (13, 17,  "Teen (under 18)",   "first jobs, saving, budgeting pocket money"),
    (18, 24,  "Early 20s",         "student loans, first salary, renting, starting to save"),
    (25, 34,  "Late 20s-30s",      "career growth, investing, buying a home, emergency funds"),
    (35, 49,  "40s",               "wealth building, children's education, insurance, retirement planning"),
    (50, 64,  "50s-early 60s",     "pre-retirement, super/pension strategy, downsizing, health costs"),
    (65, 120, "Retirement age",    "drawing down savings, aged care, estate planning, fixed income"),
]


def get_life_stage(age: int) -> Tuple[str, str]:
    for min_age, max_age, stage, desc in LIFE_STAGES:
        if min_age <= age <= max_age:
            return stage, desc
    return "Adult", "general financial management"


def _generate_questions(age: int, stage: str, desc: str) -> list:
    prompt = f"""You are a financial literacy quiz engine. Generate exactly 5 multiple-choice questions for a {age}-year-old Australian. Their life stage: "{stage}" ({desc}).

Rules:
- Questions must be realistic and specific to their age/stage
- 4 answer choices each (A, B, C, D)
- Only ONE correct answer per question
- Include a short explanation (2-3 sentences) and a pro tip per question

Respond ONLY with valid JSON, no markdown, no preamble. Format:
{{
  "questions": [
    {{
      "question": "...",
      "choices": ["A. ...", "B. ...", "C. ...", "D. ..."],
      "correct_index": 0,
      "explanation": "...",
      "tip": "..."
    }}
  ]
}}"""

    response = _client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )
    raw = response.text
    clean = raw.replace("```json", "").replace("```", "").strip()
    data = json.loads(clean)
    return [QuizQuestion(**q) for q in data["questions"]]


def create_session(age: int) -> Tuple[str, QuizSession]:
    stage, desc = get_life_stage(age)
    questions = _generate_questions(age, stage, desc)
    session_id = str(uuid.uuid4())
    session = QuizSession(age=age, life_stage=stage, questions=questions)
    _sessions[session_id] = session
    return session_id, session


def get_session(session_id: str) -> QuizSession:
    session = _sessions.get(session_id)
    if not session:
        raise KeyError(f"Session '{session_id}' not found or expired.")
    return session


def submit_answer(session_id: str, chosen_index: int) -> dict:
    session = get_session(session_id)
    if session.completed:
        raise ValueError("This quiz session is already completed.")

    q = session.questions[session.current_index]
    is_correct = chosen_index == q.correct_index
    if is_correct:
        session.score += 1

    session.current_index += 1
    questions_remaining = len(session.questions) - session.current_index
    is_final = questions_remaining == 0
    if is_final:
        session.completed = True

    return {
        "is_correct": is_correct,
        "correct_index": q.correct_index,
        "explanation": q.explanation,
        "tip": q.tip,
        "score": session.score,
        "questions_remaining": questions_remaining,
        "is_final": is_final,
        "final_message": _get_final_message(session.score, len(session.questions)) if is_final else None,
    }


def get_next_question(session_id: str) -> QuizQuestion:
    session = get_session(session_id)
    if session.completed or session.current_index >= len(session.questions):
        raise ValueError("No more questions in this session.")
    return session.questions[session.current_index]


def get_results(session_id: str) -> dict:
    session = get_session(session_id)
    total = len(session.questions)
    return {
        "session_id": session_id,
        "age": session.age,
        "life_stage": session.life_stage,
        "score": session.score,
        "total": total,
        "percentage": round((session.score / total) * 100, 1),
        "message": _get_final_message(session.score, total),
    }


def _get_final_message(score: int, total: int) -> str:
    pct = score / total
    if pct == 1.0:
        return "Outstanding! You clearly think critically about money. Keep building on this."
    elif pct >= 0.7:
        return "Solid work! You have a good foundation. Review the ones you missed to sharpen your edge."
    elif pct >= 0.4:
        return "Good effort. Financial literacy is a skill — the more you practise, the sharper you get."
    return "Everyone starts somewhere. Re-read the explanations, then try again — you will improve fast."
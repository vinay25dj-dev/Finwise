import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from app.schemas.quiz import (
    AnswerFeedback, AnswerRequest, QuizQuestion,
    QuizResultResponse, StartQuizRequest, StartQuizResponse,
)
from app.services.quiz_service import (
    create_session, get_life_stage, get_next_question, get_results, submit_answer, _client,
)

router = APIRouter()


class RawQuizRequest(BaseModel):
    age: int
    stage: str
    desc: str
    avoid: Optional[List[str]] = []
    prompt: str


@router.post("/raw")
async def raw_quiz(request: RawQuizRequest):
    """Frontend sends a complete Gemini prompt; we return the parsed questions JSON."""
    try:
        response = _client.models.generate_content(
            model="gemini-1.5-flash",
            contents=request.prompt
        )
        raw = response.text
        clean = raw.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini generation failed: {e}")


@router.post("/start", response_model=StartQuizResponse)
async def start_quiz(request: StartQuizRequest):
    if not (13 <= request.age <= 100):
        raise HTTPException(status_code=422, detail="Age must be between 13 and 100.")
    try:
        session_id, session = create_session(request.age)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate questions: {e}")
    stage, desc = get_life_stage(request.age)
    return StartQuizResponse(
        session_id=session_id, life_stage=stage, stage_description=desc,
        total_questions=len(session.questions), first_question=session.questions[0],
    )


@router.post("/answer", response_model=AnswerFeedback)
async def answer_question(request: AnswerRequest):
    try:
        return AnswerFeedback(**submit_answer(request.session_id, request.chosen_index))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/next/{session_id}", response_model=QuizQuestion)
async def next_question(session_id: str):
    try:
        return get_next_question(session_id)
    except (KeyError, ValueError) as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/results/{session_id}", response_model=QuizResultResponse)
async def quiz_results(session_id: str):
    try:
        return get_results(session_id)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))
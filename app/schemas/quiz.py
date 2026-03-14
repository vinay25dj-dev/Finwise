from pydantic import BaseModel
from typing import List, Optional


class QuizChoice(BaseModel):
    text: str
    index: int


class QuizQuestion(BaseModel):
    question: str
    choices: List[str]
    correct_index: int
    explanation: str
    tip: str


class QuizSession(BaseModel):
    age: int
    life_stage: str
    questions: List[QuizQuestion]
    current_index: int = 0
    score: int = 0
    completed: bool = False


class StartQuizRequest(BaseModel):
    age: int


class StartQuizResponse(BaseModel):
    session_id: str
    life_stage: str
    stage_description: str
    total_questions: int
    first_question: QuizQuestion


class AnswerRequest(BaseModel):
    session_id: str
    chosen_index: int


class AnswerFeedback(BaseModel):
    is_correct: bool
    correct_index: int
    explanation: str
    tip: str
    score: int
    questions_remaining: int
    is_final: bool
    final_message: Optional[str] = None


class QuizResultResponse(BaseModel):
    session_id: str
    age: int
    life_stage: str
    score: int
    total: int
    percentage: float
    message: str
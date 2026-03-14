from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from app.schemas.game import GameState, GameChoice, TurnResponse
from app.services.game_engine import get_scenario_for_age, process_choice

router = APIRouter()

class ProcessTurnRequest(BaseModel):
    state: GameState
    choice: GameChoice

@router.get("/start", response_model=TurnResponse)
async def start_game():
    # Provide a starter state and scenario
    initial_state = GameState(
        balance=1000.0,
        monthly_income=4000.0,
        monthly_expenses=3000.0,
        turn_number=1,
        score=22,
        title="Getting By",
        age=22,
        life_stage="Foundation (20s)"
    )
    first_scenario = get_scenario_for_age(initial_state.age)
    
    return TurnResponse(
        state=initial_state,
        message="Welcome to the Finwise Game! Here is your first scenario.",
        next_scenario=first_scenario
    )

@router.post("/turn", response_model=TurnResponse)
async def play_turn(request: ProcessTurnRequest):
    try:
        new_state = process_choice(request.state, request.choice)
        next_scenario = get_scenario_for_age(new_state.age)
        
        message = f"You selected: {request.choice.text}. Results have been applied to your balance."
        
        return TurnResponse(
            state=new_state,
            message=message,
            next_scenario=next_scenario
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

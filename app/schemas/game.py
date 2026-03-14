from pydantic import BaseModel, Field
from typing import List, Optional

class GameState(BaseModel):
    player_name: str = Field("Guest", description="Name of the player")
    balance: float = Field(..., description="Current cash balance in the game")
    monthly_income: float = Field(..., description="Monthly income in the game")
    monthly_expenses: float = Field(..., description="Monthly expenses in the game")
    credit_score: Optional[int] = Field(None, description="Game credit score")
    turn_number: int = Field(1, description="Current turn number")
    score: int = Field(0, description="Financial score")
    title: str = Field("Novice", description="Player Title based on wealth")
    age: int = Field(22, description="The player's current chronological age in game")
    life_stage: str = Field("Foundation (20s)", description="The player's current life stage category")

class GameChoice(BaseModel):
    id: str = Field(..., description="Unique ID for the choice")
    text: str = Field(..., description="The text of the choice displayed to the user")
    impact_description: str = Field(..., description="Short explanation of consequence")
    cost: Optional[float] = Field(0.0, description="Immediate cash cost or gain (negative=cost, positive=gain)")
    income_change: Optional[float] = Field(0.0, description="Change to monthly income")
    expense_change: Optional[float] = Field(0.0, description="Change to monthly expenses")

class GameScenario(BaseModel):
    id: str = Field(..., description="Unique ID for the scenario")
    title: str = Field(..., description="Title of the scenario")
    description: str = Field(..., description="Detailed description of the life event")
    choices: List[GameChoice] = Field(..., description="Available choices for the player")

class TurnResponse(BaseModel):
    state: GameState = Field(..., description="The player's new game state")
    message: str = Field(..., description="Feedback from the last choice made")
    next_scenario: Optional[GameScenario] = Field(None, description="The next scenario to face, if any")

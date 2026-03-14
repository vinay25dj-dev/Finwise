from pydantic import BaseModel, Field
from typing import Optional, List

class FinancialProfile(BaseModel):
    monthly_income: float = Field(..., description="User's monthly income", gt=0)
    monthly_expenses: float = Field(..., description="User's monthly expenses", ge=0)
    current_savings: float = Field(..., description="Current total savings", ge=0)
    loan_amount: Optional[float] = Field(0.0, description="Total amount of outstanding loans", ge=0)
    number_of_loans: Optional[int] = Field(0, description="Number of active loans", ge=0)
    credit_score: Optional[int] = Field(None, description="Credit score between 300 and 850", ge=300, le=850)
    financial_goals: Optional[str] = Field(None, description="Short term or long term financial goals")

class FinancialStrategy(BaseModel):
    title: str = Field(..., description="Strategy title")
    description: str = Field(..., description="Detailed description of the strategy")
    action_items: List[str] = Field(default_factory=list, description="Specific action items for the user")

class FinancialPlanResponse(BaseModel):
    score: int = Field(..., description="Overall financial health score out of 100")
    badges: List[str] = Field(default_factory=list, description="Badges earned (e.g. 'Debt Free')")
    profile_summary: str = Field(..., description="A brief summary of the user's situation")
    strategies: List[FinancialStrategy] = Field(..., description="List of generated strategies")
    emergency_fund_advice: str = Field(..., description="Advice covering unexpected expenses")

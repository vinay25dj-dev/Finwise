from fastapi import APIRouter, HTTPException
from app.schemas.financial import FinancialProfile, FinancialPlanResponse
from app.services.planner import generate_financial_plan

router = APIRouter()

@router.post("/plan", response_model=FinancialPlanResponse)
async def get_financial_plan(profile: FinancialProfile):
    try:
        plan = generate_financial_plan(profile)
        return plan
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

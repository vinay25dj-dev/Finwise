from app.schemas.financial import FinancialProfile
from app.services.planner import generate_financial_plan

def test_generate_financial_plan_emergency():
    profile = FinancialProfile(
        monthly_income=5000,
        monthly_expenses=4000,
        current_savings=5000,  # 1.25 months
        loan_amount=0,
        number_of_loans=0,
        credit_score=700,
        financial_goals="Buy a house"
    )
    plan = generate_financial_plan(profile)
    assert plan is not None
    assert any("Emergency Fund" in strat.title for strat in plan.strategies)

def test_generate_financial_plan_surplus():
    profile = FinancialProfile(
        monthly_income=10000,
        monthly_expenses=3000,
        current_savings=50000,  # > 6 months
        loan_amount=0,
        number_of_loans=0,
        credit_score=800,
        financial_goals="Retire early"
    )
    plan = generate_financial_plan(profile)
    assert any("Optimize Cash and Invest" in strat.title for strat in plan.strategies)
    assert "surplus" in plan.profile_summary.lower()

def test_generate_financial_plan_debt():
    profile = FinancialProfile(
        monthly_income=6000,
        monthly_expenses=3000,
        current_savings=20000,
        loan_amount=15000,
        number_of_loans=2,
        credit_score=650,
        financial_goals="Clear debt"
    )
    plan = generate_financial_plan(profile)
    assert any("Debt" in strat.title for strat in plan.strategies)

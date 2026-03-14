from app.schemas.financial import FinancialProfile, FinancialPlanResponse, FinancialStrategy

def generate_financial_plan(profile: FinancialProfile) -> FinancialPlanResponse:
    strategies = []
    badges = []
    score = 50  # Base Score
    
    # Analyze emergency fund (Current Savings vs Monthly Expenses)
    emergency_months = profile.current_savings / profile.monthly_expenses if profile.monthly_expenses > 0 else float('inf')
    
    if emergency_months < 3:
        score -= 15
        emergency_advice = f"Your current savings of ${profile.current_savings} covers about {emergency_months:.1f} months of expenses. Aim to save at least 3-6 months (${profile.monthly_expenses * 3} - ${profile.monthly_expenses * 6}) for unexpected life events."
        strategies.append(FinancialStrategy(
            title="Build an Emergency Fund",
            description="You need a safety net for unexpected expenses like medical bills or car repairs.",
            action_items=[
                "Set up an automatic transfer of 10% of your income into a high-yield savings account.",
                "Cut down on non-essential dining out next month to boost initial emergency savings."
            ]
        ))
    elif emergency_months < 6:
        score += 10
        emergency_advice = f"Good job! You have about {emergency_months:.1f} months of emergency savings. Consider pushing it to 6 months for better security."
        badges.append("Saver")
    else:
         score += 25
         badges.append("Emergency Ready")
         emergency_advice = "Excellent! You have a robust emergency fund. Focus your surplus cash on investments or paying down debt."
         strategies.append(FinancialStrategy(
             title="Optimize Cash and Invest",
             description="Your emergency fund is fully funded. Time to make your money work harder.",
             action_items=[
                 "Open a brokerage account and invest in low-cost index funds.",
                 "Maximize contributions to tax-advantaged retirement accounts."
             ]
         ))

    # Analyze debt
    if profile.loan_amount > 0:
        score -= min(20, int((profile.loan_amount / max(1, profile.monthly_income)) * 5))
        strategies.append(FinancialStrategy(
            title="Accelerate Debt Paydown",
            description=f"You have ${profile.loan_amount} in loans. Paying this down reduces interest burden and increases your cash flow.",
            action_items=[
                "List your debts from highest interest rate to lowest.",
                "Pay minimums on all, and put all extra cash toward the highest interest debt (Avalanche method)."
            ]
        ))
    else:
        score += 15
        badges.append("Debt Free")

    # Surplus analysis
    surplus = profile.monthly_income - profile.monthly_expenses
    if surplus < profile.monthly_income * 0.1:
        score -= min(20, int(((profile.monthly_income * 0.1 - surplus) / max(1, profile.monthly_income)) * 100))
        strategies.append(FinancialStrategy(
            title="Increase Monthly Cash Flow",
            description="Your expenses are consuming a large portion of your income, leaving little room to save.",
            action_items=[
                "Review subscriptions and cancel unused services.",
                "Negotiate lower rates on insurance and internet bills.",
                "Look for opportunities to increase income via a side hustle or asking for a raise."
            ]
        ))
    elif surplus > profile.monthly_income * 0.3:
        score += 10
        badges.append("High Earner")
    
    # Cap score between 0 and 100
    score = max(0, min(100, score))
    
    summary = f"With a monthly surplus of ${surplus:.2f} and a credit score of {profile.credit_score or 'Unknown'}, you are in a position to take control of your finances. "
    if profile.financial_goals:
        summary += f"These strategies are tailored to help you reach your goal: '{profile.financial_goals}'."

    return FinancialPlanResponse(
        score=score,
        badges=badges,
        profile_summary=summary.strip(),
        strategies=strategies,
        emergency_fund_advice=emergency_advice
    )

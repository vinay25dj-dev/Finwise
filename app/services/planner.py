from app.schemas.financial import FinancialProfile, FinancialPlanResponse, FinancialStrategy


def generate_financial_plan(profile: FinancialProfile) -> FinancialPlanResponse:
    strategies = []
    badges = []
    score = 50  # Base score

    # --- Emergency fund analysis ---
    emergency_months = (
        profile.current_savings / profile.monthly_expenses
        if profile.monthly_expenses > 0
        else float("inf")
    )

    if emergency_months < 3:
        score -= 15
        emergency_advice = (
            f"Your current savings of ${profile.current_savings:.2f} covers about "
            f"{emergency_months:.1f} months of expenses. Aim for at least 3–6 months "
            f"(${profile.monthly_expenses * 3:.2f}–${profile.monthly_expenses * 6:.2f}) "
            f"for unexpected life events."
        )
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
        badges.append("Saver")
        emergency_advice = (
            f"Good job! You have about {emergency_months:.1f} months of emergency savings. "
            f"Consider pushing it to 6 months for better security."
        )
    else:
        score += 25
        badges.append("Emergency Ready")
        emergency_advice = (
            "Excellent! You have a robust emergency fund. "
            "Focus your surplus cash on investments or paying down debt."
        )
        strategies.append(FinancialStrategy(
            title="Optimize Cash and Invest",
            description="Your emergency fund is fully funded. Time to make your money work harder.",
            action_items=[
                "Open a brokerage account and invest in low-cost index funds.",
                "Maximize contributions to tax-advantaged retirement accounts."
            ]
        ))

    # --- Debt analysis ---
    loan_amount = profile.loan_amount or 0.0
    if loan_amount > 0:
        score -= min(20, int((loan_amount / max(1, profile.monthly_income)) * 5))
        strategies.append(FinancialStrategy(
            title="Accelerate Debt Paydown",
            description=(
                f"You have ${loan_amount:.2f} in loans. Paying this down reduces "
                f"interest burden and increases your monthly cash flow."
            ),
            action_items=[
                "List your debts from highest interest rate to lowest.",
                "Pay minimums on all debts, then put all extra cash toward the highest-interest one (Avalanche method)."
            ]
        ))
    else:
        score += 15
        badges.append("Debt Free")

    # --- Surplus / cash-flow analysis ---
    surplus = profile.monthly_income - profile.monthly_expenses
    if surplus < profile.monthly_income * 0.1:
        score -= min(20, int(((profile.monthly_income * 0.1 - surplus) / max(1, profile.monthly_income)) * 100))
        strategies.append(FinancialStrategy(
            title="Increase Monthly Cash Flow",
            description="Your expenses are consuming a large portion of your income, leaving little room to save.",
            action_items=[
                "Review subscriptions and cancel unused services.",
                "Negotiate lower rates on insurance and internet bills.",
                "Look for opportunities to increase income via a side hustle or by asking for a raise."
            ]
        ))
    elif surplus > profile.monthly_income * 0.3:
        score += 10
        badges.append("High Earner")

    # Cap score 0–100
    score = max(0, min(100, score))

    summary = (
        f"With a monthly surplus of ${surplus:.2f} and a credit score of "
        f"{profile.credit_score or 'Unknown'}, you are in a position to take control of your finances."
    )
    if profile.financial_goals:
        summary += f" These strategies are tailored to help you reach your goal: '{profile.financial_goals}'."

    return FinancialPlanResponse(
        score=score,
        badges=badges,
        profile_summary=summary.strip(),
        strategies=strategies,
        emergency_fund_advice=emergency_advice
    )
from app.schemas.game import GameState, GameChoice
from app.services.game_engine import get_scenario_for_age, process_choice

def test_get_scenario_for_age():
    scenario = get_scenario_for_age(25)
    assert scenario.title is not None
    assert len(scenario.choices) > 0

def test_process_choice():
    initial_state = GameState(
        balance=1000,
        monthly_income=5000,
        monthly_expenses=4000,
        turn_number=1,
        age=22
    )
    
    # Simulate a choice that costs 500 now, and adds 200 to expenses
    choice = GameChoice(
        id="test_choice",
        text="Test",
        impact_description="Impact test",
        cost=-500,
        income_change=0,
        expense_change=200
    )
    
    new_state = process_choice(initial_state, choice)
    
    # new balance = current (1000) + surplus (1000) + cost (-500) = 1500
    assert new_state.balance == 1500
    assert new_state.monthly_expenses == 4200
    assert new_state.turn_number == 2
    assert new_state.age == 23

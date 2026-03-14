import random
import uuid
from app.schemas.game import GameScenario, GameChoice, GameState

SCENARIO_TEMPLATES = [
    # ---- 20s: Early Career & Foundations ----
    {
        "category": "Education & Career",
        "min_age": 20, "max_age": 29,
        "title_templates": ["Student Loan Repayment", "First Apartment", "Entry-level Grind", "Certification"],
        "desc_templates": [
            "You are facing the realities of a '{event}'.",
            "A '{event}' challenge has appeared.",
            "You need to handle a '{event}' to move forward in your 20s."
        ],
        "events": ["student debt milestone", "lease renewal", "low-paying internship", "skill bootcamp"],
        "base_cost": (500, 3000),
        "choices_templates": [
            {"type": "pay", "text": "Pay aggressively from savings", "impact": "Drains cash now but saves on interest.", "cost_mult": 1.0, "exp": -50},
            {"type": "finance", "text": "Take on reasonable debt", "impact": "Leaves cash reserves but adds a monthly payment.", "cost_mult": 0.1, "exp": 150},
            {"type": "ignore", "text": "Defer or delay", "impact": "Temporary relief but costs more long-term.", "cost_mult": 0, "exp": 0, "risk_mult": 1.5}
        ]
    },
    {
        "category": "Lifestyle (20s)",
        "min_age": 20, "max_age": 29,
        "title_templates": ["Friend's Destination Wedding", "Moving to a New City", "Music Festival"],
        "desc_templates": [
            "Your friends are planning a '{event}'.",
            "You have the urge for a '{event}'.",
            "An opportunity for a '{event}' comes up."
        ],
        "events": ["trip to Bali", "cross-country move", "VIP concert experience"],
        "base_cost": (800, 2500),
        "choices_templates": [
            {"type": "go", "text": "Go and enjoy your youth!", "impact": "Great memories, big hit to savings.", "cost_mult": 1.0, "exp": 0},
            {"type": "budget", "text": "Go but on a strict budget", "impact": "Moderate fun, moderate cost.", "cost_mult": 0.5, "exp": 0},
            {"type": "skip", "text": "Stay home and save", "impact": "FOMO, but your wallet is safe.", "cost_mult": 0, "exp": 0}
        ]
    },

    # ---- 30s: Growth & Establishment ----
    {
        "category": "Home & Family",
        "min_age": 30, "max_age": 39,
        "title_templates": ["First Home Purchase", "Childcare Costs", "Home Upgrade"],
        "desc_templates": [
            "It's time to consider a '{event}'.",
            "You're facing expenses from a '{event}'.",
            "A '{event}' is becoming a priority."
        ],
        "events": ["down payment on a house", "daycare enrollment", "kitchen remodel"],
        "base_cost": (5000, 20000),
        "choices_templates": [
            {"type": "cash", "text": "Use your savings", "impact": "Massive upfront cost, but builds equity or handles the need securely.", "cost_mult": 1.0, "exp": 0},
            {"type": "loan", "text": "Take out a loan", "impact": "Keeps cash safe but adds a massive monthly expense.", "cost_mult": 0.1, "exp": 500},
            {"type": "delay", "text": "Keep renting / Delay plans", "impact": "Safe play, but delays life goals.", "cost_mult": 0, "exp": 0}
        ]
    },
    {
        "category": "Career (30s)",
        "min_age": 30, "max_age": 39,
        "title_templates": ["Mid-Career Shift", "Management Role", "Starting a Business"],
        "desc_templates": [
            "You have an opportunity for a '{event}'.",
            "You're conceptualizing a '{event}'.",
            "A recruiter reached out about a '{event}'."
        ],
        "events": ["career pivot", "promotion to director", "side hustle launch"],
        "base_cost": (2000, 10000),
        "choices_templates": [
            {"type": "invest", "text": "Take the leap and invest", "impact": "High cost now, but huge potential income boost.", "cost_mult": 1.0, "inc_boost": (1000, 3000), "exp": 0},
            {"type": "safe", "text": "Stay in current comfortable job", "impact": "No risk, small predictable raise.", "cost_mult": 0, "inc_boost": (100, 300), "exp": 0}
        ]
    },

    # ---- 40s-50s: Wealth Building & Realities ----
    {
        "category": "Health & Parents",
        "min_age": 40, "max_age": 59,
        "title_templates": ["Medical Emergency", "Aging Parents Care", "Health Scare"],
        "desc_templates": [
            "You encounter a sudden '{event}'.",
            "You need to handle a '{event}' for a family member.",
            "A '{event}' requires immediate financial attention."
        ],
        "events": ["surgery deductible", "assisted living deposit", "major dental work"],
        "base_cost": (3000, 15000),
        "choices_templates": [
            {"type": "savings", "text": "Pay from emergency fund", "impact": "Drains liquidity suddenly.", "cost_mult": 1.0, "exp": 0},
            {"type": "finance", "text": "Finance the medical debt", "impact": "Adds significant monthly burden.", "cost_mult": 0, "exp": 400}
        ]
    },
    {
        "category": "Investments",
        "min_age": 40, "max_age": 59,
        "title_templates": ["Market Crash", "Investment Opportunity", "College Fund"],
        "desc_templates": [
            "You face a major decision regarding a '{event}'.",
            "The reality of a '{event}' hits you.",
            "An advisor calls you about a '{event}'."
        ],
        "events": ["stock market dip", "real estate deal", "kids tuition bill"],
        "base_cost": (5000, 25000),
        "choices_templates": [
            {"type": "aggressive", "text": "Buy the dip / Pay the tuition", "impact": "Huge upfront cost but secures the future.", "cost_mult": 1.0, "exp": 0},
            {"type": "conservative", "text": "Pull back to cash / Take student loans", "impact": "Saves cash, but loses potential growth.", "cost_mult": 0, "exp": 300}
        ]
    },

    # ---- 60s+: Pre-Retirement & Legacy ----
    {
        "category": "Retirement",
        "min_age": 60, "max_age": 100,
        "title_templates": ["Downsizing", "Pension Decision", "Health Insurance Shift"],
        "desc_templates": [
            "You are navigating a '{event}'.",
            "It's time for a '{event}'.",
            "A '{event}' approaches as retirement nears."
        ],
        "events": ["selling the family home", "lump sum vs annuity", "Medicare enrollment"],
        "base_cost": (0, 5000),
        "choices_templates": [
            {"type": "safe", "text": "Prioritize security", "impact": "Lowers expenses massively, moderate cost.", "cost_mult": 1.0, "exp": -1000},
            {"type": "risk", "text": "Keep current lifestyle", "impact": "No upfront cost, but expenses stay dangerously high.", "cost_mult": 0, "exp": 0}
        ]
    }
]


def get_scenario_for_age(age: int) -> GameScenario:
    valid_templates = [t for t in SCENARIO_TEMPLATES if t["min_age"] <= age <= t["max_age"]]
    if not valid_templates:
        valid_templates = SCENARIO_TEMPLATES

    template = random.choice(valid_templates)

    title = random.choice(template["title_templates"])
    event = random.choice(template["events"])
    description = random.choice(template["desc_templates"]).format(event=event)

    base_cost_range = template["base_cost"]
    base_cost = random.randint(base_cost_range[0], base_cost_range[1])

    choices_list = template["choices_templates"]
    chosen_templates = random.sample(choices_list, min(3, len(choices_list)))

    choices = []
    for c in chosen_templates:
        actual_cost = -int(base_cost * c.get("cost_mult", 1.0))

        exp_change = c.get("exp", 0)
        if isinstance(exp_change, float) and 0 < exp_change < 1:
            exp_change = int(abs(base_cost) * exp_change)
            actual_cost = 0

        inc_boost = 0
        if "inc_boost" in c:
            inc_boost = random.randint(c["inc_boost"][0], c["inc_boost"][1])

        choices.append(GameChoice(
            id=str(uuid.uuid4()),
            text=c["text"],
            impact_description=c["impact"],
            cost=actual_cost,
            income_change=inc_boost,
            expense_change=exp_change
        ))

    return GameScenario(
        id=str(uuid.uuid4()),
        title=f"[{template['category']}] {title}",
        description=description,
        choices=choices
    )


def process_choice(current_state: GameState, choice: GameChoice) -> GameState:
    new_state = current_state.model_copy()

    # Apply monthly surplus
    surplus = new_state.monthly_income - new_state.monthly_expenses
    new_state.balance += surplus

    # Apply one-time cost/gain from choice
    new_state.balance += choice.cost

    # Apply ongoing changes
    new_state.monthly_income += choice.income_change
    new_state.monthly_expenses += choice.expense_change

    new_state.turn_number += 1
    new_state.age += 1

    # Update life stage
    if new_state.age < 30:
        new_state.life_stage = "Foundation (20s)"
    elif new_state.age < 40:
        new_state.life_stage = "Growth (30s)"
    elif new_state.age < 50:
        new_state.life_stage = "Mid-Life (40s)"
    elif new_state.age < 60:
        new_state.life_stage = "Pre-Retirement (50s)"
    else:
        new_state.life_stage = "Legacy (60s+)"

    # Update score and title
    net_flow = new_state.monthly_income - new_state.monthly_expenses
    potential_health = new_state.balance + (net_flow * 12)
    new_state.score = int(max(0, min(10000, potential_health)) / 100)

    if new_state.balance < 0 and net_flow < 0:
        new_state.title = "Bankrupt Dangers"
    elif new_state.balance < 1000:
        new_state.title = "Survival Mode"
    elif new_state.balance < 5000:
        new_state.title = "Getting By"
    elif new_state.balance < 15000:
        new_state.title = "Comfortable"
    else:
        new_state.title = "Wealth Building"

    return new_state
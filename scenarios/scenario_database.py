"""
FinWise Scenario Database
Contains behavioral financial decision scenarios with bias tags
"""

SCENARIO_DATABASE = [
    {
        "id": "S001",
        "topic": "Spending vs Saving",
        "bias_tested": "Present Bias",
        "difficulty": 1,
        "scenario_text": """
You just received ₹5,000 as a birthday gift. You have two options:

A) Spend ₹3,000 now on something you want, save ₹2,000
B) Save all ₹5,000 and earn ₹500 interest in 6 months

There's a sale ending today on something you've wanted for a while.
        """,
        "decision_type": "slider",  # 0 = Option A, 100 = Option B
        "metrics_to_track": ["decision_value", "decision_time", "confidence"],
        "ideal_range": [40, 80],  # Balanced to slightly savings-focused
        "follow_up_question": "How confident are you about this decision?"
    },
    
    {
        "id": "S002",
        "topic": "Discount Trap",
        "bias_tested": "Anchoring Bias",
        "difficulty": 1,
        "scenario_text": """
You're buying a laptop. You see two options:

Laptop A: Originally ₹60,000, now ₹45,000 (25% off)
Laptop B: Priced at ₹42,000 (no discount mentioned)

Both have identical specifications and warranty. Which do you choose?
        """,
        "decision_type": "choice",
        "options": ["Laptop A (discounted)", "Laptop B (regular price)", "Need more time to decide"],
        "metrics_to_track": ["choice", "decision_time", "reasoning"],
        "ideal_choice": 1,  # Laptop B is objectively better
        "follow_up_question": "What influenced your decision the most?"
    },
    
    {
        "id": "S003",
        "topic": "Delayed Gratification",
        "bias_tested": "Hyperbolic Discounting",
        "difficulty": 2,
        "scenario_text": """
You're offered a choice for your internship stipend payment:

Option A: Receive ₹10,000 today
Option B: Receive ₹13,000 after 2 months
Option C: Receive ₹15,000 after 4 months

You have no urgent expenses. Your emergency fund can cover 2 months.
        """,
        "decision_type": "choice",
        "options": ["₹10,000 today", "₹13,000 in 2 months", "₹15,000 in 4 months"],
        "metrics_to_track": ["choice", "decision_time", "confidence", "revision_count"],
        "ideal_choice": 2,  # Best ROI
        "follow_up_question": "How comfortable are you waiting for larger rewards?"
    },
    
    {
        "id": "S004",
        "topic": "Credit Card EMI",
        "bias_tested": "Mental Accounting",
        "difficulty": 2,
        "scenario_text": """
You want to buy a phone worth ₹30,000. You have three payment options:

A) Pay ₹30,000 upfront (you have this amount saved)
B) Pay ₹6,000/month for 6 months (Total: ₹36,000, 20% interest)
C) Pay ₹3,200/month for 12 months (Total: ₹38,400, 28% interest)

Your monthly income is ₹25,000, expenses are ₹18,000.
        """,
        "decision_type": "choice",
        "options": ["Pay ₹30,000 now", "6-month EMI", "12-month EMI"],
        "metrics_to_track": ["choice", "decision_time", "confidence"],
        "ideal_choice": 0,  # Lowest cost
        "follow_up_question": "Did the monthly payment amount influence your choice?"
    },
    
    {
        "id": "S005",
        "topic": "Subscription Trap",
        "bias_tested": "Sunk Cost Fallacy",
        "difficulty": 2,
        "scenario_text": """
You subscribed to a streaming service 3 months ago (₹500/month).
You've only used it twice in the last 2 months.

The annual plan costs ₹4,800 (saves ₹1,200 vs monthly).

What do you do?
        """,
        "decision_type": "choice",
        "options": [
            "Cancel immediately",
            "Continue monthly plan",
            "Switch to annual plan to save money",
            "Cancel after this month"
        ],
        "metrics_to_track": ["choice", "decision_time", "reasoning"],
        "ideal_choice": 0,  # Cancel if not using
        "follow_up_question": "Did the money already spent affect your decision?"
    },
    
    {
        "id": "S006",
        "topic": "Emergency Fund",
        "bias_tested": "Optimism Bias",
        "difficulty": 1,
        "scenario_text": """
You just started earning ₹30,000/month. Your expenses are ₹20,000/month.

How much do you want to keep as an emergency fund before investing?
        """,
        "decision_type": "slider",  # 0 = 1 month, 100 = 12 months
        "slider_labels": ["1 month", "3 months", "6 months", "12 months"],
        "metrics_to_track": ["decision_value", "decision_time", "confidence"],
        "ideal_range": [40, 70],  # 3-6 months recommended
        "follow_up_question": "What emergencies did you consider?"
    },
    
    {
        "id": "S007",
        "topic": "Opportunity Cost",
        "bias_tested": "Loss Aversion",
        "difficulty": 3,
        "scenario_text": """
You have ₹50,000 saved. Two options:

A) Invest in a course (₹40,000) that could increase your salary by ₹10,000/month within 6 months (70% success rate)

B) Keep money in fixed deposit earning ₹3,000 over the next year (100% guaranteed)

Your current job is stable. You have 3 months' emergency fund separately.
        """,
        "decision_type": "slider",  # 0 = All FD, 100 = All course
        "metrics_to_track": ["decision_value", "decision_time", "confidence", "risk_perception"],
        "ideal_range": [60, 90],  # Should lean toward investment
        "follow_up_question": "What worried you most about the risky option?"
    },
    
    {
        "id": "S008",
        "topic": "Time Value of Money",
        "bias_tested": "Present Bias",
        "difficulty": 3,
        "scenario_text": """
You receive a ₹1,00,000 bonus. Choose one:

A) Spend ₹60,000 on a vacation now, invest ₹40,000
B) Spend ₹30,000 on a smaller trip now, invest ₹70,000
C) Invest all ₹1,00,000, plan a bigger vacation next year using returns

Your investments historically give 12% annual returns.
You haven't taken a vacation in 2 years.
        """,
        "decision_type": "choice",
        "options": [
            "₹60k vacation + ₹40k investment",
            "₹30k vacation + ₹70k investment",
            "₹100k investment, vacation later"
        ],
        "metrics_to_track": ["choice", "decision_time", "confidence", "reasoning"],
        "ideal_choice": 1,  # Balanced approach
        "follow_up_question": "How did you weigh present enjoyment vs future gains?"
    }
]

def get_scenario_by_id(scenario_id):
    """Retrieve scenario by ID"""
    for scenario in SCENARIO_DATABASE:
        if scenario["id"] == scenario_id:
            return scenario
    return None

def get_scenarios_by_difficulty(difficulty):
    """Get all scenarios of a specific difficulty"""
    return [s for s in SCENARIO_DATABASE if s["difficulty"] == difficulty]

def get_scenarios_by_bias(bias_type):
    """Get scenarios testing a specific bias"""
    return [s for s in SCENARIO_DATABASE if s["bias_tested"] == bias_type]

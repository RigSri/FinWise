import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import json
from scenarios.scenario_database import SCENARIO_DATABASE
from utils.behavioral_analysis import BehavioralAnalyzer
from utils.insight_generator import InsightGenerator
from utils.scenario_selector import AdaptiveScenarioSelector

# PDF Generation Function
def generate_pdf_report(persona, insights, progress):
    """Generate PDF report of behavioral profile"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.enums import TA_CENTER
        import io
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1E3A8A'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        story.append(Paragraph("FinWise Behavioral Profile Report", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Date
        date_text = f"Generated on: {datetime.now().strftime('%B %d, %Y')}"
        story.append(Paragraph(date_text, styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Profile metrics
        story.append(Paragraph("Behavioral Metrics", styles['Heading2']))
        
        metrics_data = [
            ['Metric', 'Score'],
            ['Risk Tolerance', f"{persona['risk_tolerance']:.0f}/100"],
            ['Impulsivity', f"{persona['impulsivity']:.0f}/100"],
            ['Loss Aversion', f"{persona['loss_aversion']:.0f}/100"],
            ['Planning Horizon', f"{persona['planning_horizon']:.0f}/100"]
        ]
        
        metrics_table = Table(metrics_data, colWidths=[3*inch, 2*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(metrics_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Strengths
        story.append(Paragraph("Strengths", styles['Heading2']))
        for strength in insights['strengths']:
            story.append(Paragraph(f"• {strength}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Growth Areas
        story.append(Paragraph("Growth Areas", styles['Heading2']))
        for growth in insights['growth_areas']:
            story.append(Paragraph(f"• {growth}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Progress
        story.append(Paragraph("Progress Summary", styles['Heading2']))
        story.append(Paragraph(f"Scenarios Completed: {progress['completed']}/{progress['total_scenarios']}", styles['Normal']))
        story.append(Paragraph(f"Completion Rate: {progress['completion_percentage']:.0f}%", styles['Normal']))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    except ImportError:
        return None
    

def create_scenario_visualization(scenario):
    """Create relevant visualization for scenario"""
    
    # S001: Delayed Gratification - Compound Interest Growth
    if scenario['id'] == 'S001':
        years = list(range(0, 11))
        immediate_value = [10000] * 11
        delayed_value = [10000 * (1.12 ** year) for year in years]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=years, y=immediate_value, name='Take ₹10k Now', 
                                line=dict(color='#EF4444', width=3)))
        fig.add_trace(go.Scatter(x=years, y=delayed_value, name='Wait & Invest at 12%',
                                line=dict(color='#10B981', width=3)))
        
        fig.update_layout(
            title='Money Growth Over Time',
            xaxis_title='Years',
            yaxis_title='Value (₹)',
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        return fig
    
    # S002: Anchoring - Price Comparison
    elif scenario['id'] == 'S002':
        items = ['Option A<br>(60% off)', 'Option B<br>(20% off)']
        original_prices = [5000, 1250]
        final_prices = [2000, 1000]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=items, y=original_prices, name='Original Price',
                            marker_color='#F87171'))
        fig.add_trace(go.Bar(x=items, y=final_prices, name='Final Price',
                            marker_color='#34D399'))
        
        fig.update_layout(
            title='Actual Prices: Look Beyond Discounts!',
            yaxis_title='Price (₹)',
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            barmode='group'
        )
        return fig
    
    # S003: Time Value - Investment Return
    elif scenario['id'] == 'S003':
        months = list(range(0, 13))
        option_a = [50000] * 13
        option_b = [50000 + (2500 * month) for month in months]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=option_a, name='Get ₹50k Now',
                                line=dict(color='#F59E0B', width=3)))
        fig.add_trace(go.Scatter(x=months, y=option_b, name='₹52.5k in 1 Year',
                                line=dict(color='#8B5CF6', width=3, dash='dash')))
        
        fig.update_layout(
            title='Effective Annual Return: 5% per year',
            xaxis_title='Months',
            yaxis_title='Value (₹)',
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        return fig
    
    # S004: Interest Cost - Loan Comparison
    elif scenario['id'] == 'S004':
        categories = ['15% Interest<br>12 months', '10% Interest<br>24 months']
        principal = [20000, 20000]
        interest = [1635, 2200]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=categories, y=principal, name='Principal',
                            marker_color='#60A5FA'))
        fig.add_trace(go.Bar(x=categories, y=interest, name='Interest Paid',
                            marker_color='#F87171'))
        
        fig.update_layout(
            title='Total Cost Comparison',
            yaxis_title='Amount (₹)',
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            barmode='stack'
        )
        return fig
    
    # S006: Emergency Fund - Savings Goal
    elif scenario['id'] == 'S006':
        categories = ['Current<br>₹10k', '3 Months<br>₹90k', '6 Months<br>₹180k']
        values = [10000, 90000, 180000]
        colors = ['#EF4444', '#F59E0B', '#10B981']
        
        fig = go.Figure(data=[go.Bar(x=categories, y=values, marker_color=colors)])
        
        fig.update_layout(
            title='Emergency Fund: Expert Recommendation',
            yaxis_title='Savings (₹)',
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        return fig
    
    # S008: Present vs Future - Trade-off
    elif scenario['id'] == 'S008':
        options = ['All Travel<br>₹2L Now', 'Balanced<br>₹1L + ₹1L Invest', 'All Invest<br>₹2L → ₹6.27L']
        immediate_joy = [100, 50, 0]
        future_wealth = [0, 100, 314]  # After 10 years at 12%
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=options, y=immediate_joy, name='Immediate Joy',
                            marker_color='#F472B6'))
        fig.add_trace(go.Bar(x=options, y=future_wealth, name='Future Wealth (10 yrs)',
                            marker_color='#34D399'))
        
        fig.update_layout(
            title='Present vs Future Trade-off',
            yaxis_title='Relative Value',
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            barmode='group'
        )
        return fig
    
    # S010: Budget Allocation - 50-30-20 Rule
    elif scenario['id'] == 'S010':
        labels = ['Needs (50%)', 'Wants (30%)', 'Savings (20%)']
        values = [50, 30, 20]
        colors = ['#60A5FA', '#F472B6', '#34D399']
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker_colors=colors,
                                     textinfo='label+percent', hole=0.3)])
        
        fig.update_layout(
            title='Recommended Budget: 50-30-20 Rule',
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        return fig
    
    # S012: Brand Premium - Value Comparison
    elif scenario['id'] == 'S012':
        items = ['No-Brand<br>₹35k', 'Brand<br>₹35.9k']
        values = [35000, 35900]
        colors = ['#10B981', '#F59E0B']
        
        fig = go.Figure(data=[go.Bar(x=items, y=values, marker_color=colors,
                                     text=[f'₹{v:,}' for v in values], textposition='outside')])
        
        fig.update_layout(
            title='Same Specs, Different Brand - Worth ₹900?',
            yaxis_title='Price (₹)',
            height=300,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        return fig
    
    # S015: Early Investment - Compound Magic
    elif scenario['id'] == 'S015':
        years = list(range(22, 61))
        start_22 = [5000 * 12 * ((1.12 ** (year - 22)) - 1) / 0.12 for year in years]
        start_30 = [0] * 8 + [5000 * 12 * ((1.12 ** (year - 30)) - 1) / 0.12 for year in years[8:]]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=years, y=start_22, name='Start at 22',
                                fill='tonexty', line=dict(color='#8B5CF6', width=3)))
        fig.add_trace(go.Scatter(x=years, y=start_30, name='Start at 30',
                                fill='tozeroy', line=dict(color='#F59E0B', width=3)))
        
        fig.update_layout(
            title='₹5k/month invested: Starting Early = Huge Difference',
            xaxis_title='Age',
            yaxis_title='Portfolio Value (₹ Lakhs)',
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        return fig
    
    return None

# Page config
st.set_page_config(
    page_title="FinWise - Behavioral Financial Learning",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# FIXED Custom CSS with better colors
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .scenario-card {
        background: #F1F5F9;
        padding: 2rem;
        border-radius: 15px;
        border-left: 5px solid #3B82F6;
        margin: 1rem 0;
        color: #1E293B;
        font-size: 1.1rem;
        line-height: 1.8;
    }
    .hero-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .hint-box {
        background: #FEF3C7;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #F59E0B;
        color: #92400E;
        margin: 1rem 0;
        font-weight: 500;
    }
    .badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.5rem;
        font-weight: bold;
    }
    .case-study-box {
        background: #FFF1F2;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #EF4444;
        margin: 1rem 0;
        color: #7F1D1D;
        font-weight: 500;
        line-height: 1.6;
    }
    .calculator-box {
        background: #E0E7FF;
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid #6366F1;
        margin: 1rem 0;
    }
    .strength-box {
        background: #D1FAE5;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #10B981;
        margin: 0.5rem 0;
        color: #065F46;
        font-weight: 500;
    }
    .growth-box {
        background: #DBEAFE;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #3B82F6;
        margin: 0.5rem 0;
        color: #1E3A8A;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Hints database
HINTS = {
    "S001": "Think about opportunity cost: what could that money grow into if you wait?",
    "S002": "Focus on the actual price, not the discount percentage. Which costs less?",
    "S003": "Calculate the percentage return: how much extra are you getting per month of waiting?",
    "S004": "Compare total amounts paid. Interest adds up over time.",
    "S005": "Consider future usage, not past spending. Past money is already gone.",
    "S006": "Financial experts typically recommend 3-6 months of expenses for emergencies.",
    "S007": "Compare expected returns: 70% chance of ₹10k/month vs guaranteed ₹3k/year.",
    "S008": "Consider: can you enjoy yourself AND secure your future?",
    "S009": "Ask yourself: do you understand the investment, or are you following the crowd?",
    "S010": "The 50-30-20 rule: 50% needs, 30% wants, 20% savings.",
    "S011": "Medical emergencies are unpredictable. Young doesn't mean invincible.",
    "S012": "Same specs, same warranty = same product. Is the brand worth ₹900 more?",
    "S013": "Kill the highest interest rate first. It's costing you the most money.",
    "S014": "Want vs Need test: Will you regret this in a week? Can you survive without it?",
    "S015": "Compound interest is magical when started early. Time is your biggest asset."
}

# Real-world case studies
CASE_STUDIES = {
    "Present Bias": "📉 In 2017, many people withdrew retirement savings early, paying 30% penalties, to buy items they no longer use today. Short-term thinking cost them lakhs in future wealth.",
    "Anchoring Bias": "💰 Black Friday shoppers spend 40% more than planned because 'original prices' anchor them to believe they're getting deals, even when prices are artificially inflated.",
    "Herd Behavior": "📊 The 2017 Bitcoin FOMO: People invested life savings at ₹15 lakh/coin because 'everyone was doing it.' Many lost 70% when it crashed to ₹4 lakh.",
    "Sunk Cost Fallacy": "🎓 38% of people continue paying for gym memberships they don't use 'because they already paid.' That's ₹6,000+/year wasted.",
    "Loss Aversion": "📈 Investors who check portfolios daily are 2x more likely to sell winners early and hold losers longer, losing 3-5% annual returns.",
    "Hyperbolic Discounting": "💳 Credit card users pay ₹2.5 lakh extra over a lifetime due to minimum payments, choosing small monthly payments over paying off high-interest debt.",
    "Mental Accounting": "🎰 People spend bonuses on luxuries but won't spend 'salary' the same way, even though it's all just money. This arbitrary division costs them.",
    "Optimism Bias": "🏥 70% of young adults skip health insurance thinking 'it won't happen to me.' One hospitalization can cost ₹5-10 lakhs, wiping out years of savings.",
    "Status Quo Bias": "💼 Employees who don't negotiate salary cost themselves ₹50 lakhs+ over a career. Inertia is expensive."
}

# Learning resources
LEARNING_RESOURCES = {
    "Present Bias": {
        "explanation": "Present bias makes us overvalue immediate rewards over larger future benefits.",
        "resources": [
            "📚 Read: 'Thinking, Fast and Slow' by Daniel Kahneman",
            "🎥 Watch: TED Talk - 'The puzzle of motivation' by Dan Pink",
            "📝 Practice: Set up automatic savings before you see your paycheck"
        ]
    },
    "Anchoring Bias": {
        "explanation": "Anchoring bias causes us to rely too heavily on the first piece of information (the 'anchor').",
        "resources": [
            "📚 Read: 'Predictably Irrational' by Dan Ariely",
            "💡 Tip: Always research the actual value before looking at discounts",
            "📝 Practice: Compare at least 3 options before making purchase decisions"
        ]
    },
    "Hyperbolic Discounting": {
        "explanation": "We value immediate rewards disproportionately over future ones, even when future is better.",
        "resources": [
            "📚 Read: 'The Marshmallow Test' by Walter Mischel",
            "💰 Tool: Use compound interest calculators to visualize long-term gains",
            "📝 Practice: Create a '30-day rule' for big purchases"
        ]
    },
    "Mental Accounting": {
        "explanation": "We treat money differently based on arbitrary categories rather than its actual value.",
        "resources": [
            "📚 Read: 'Nudge' by Richard Thaler",
            "💡 Tip: Money is money - focus on total cost, not payment structure",
            "📝 Practice: Track all expenses in one place to see the full picture"
        ]
    },
    "Sunk Cost Fallacy": {
        "explanation": "We continue investing in something because we've already spent money, time, or effort on it.",
        "resources": [
            "📚 Read: 'The Art of Thinking Clearly' by Rolf Dobelli",
            "💡 Tip: Past costs are irrelevant. Only consider future value.",
            "📝 Practice: Ask 'Would I start this today?' for ongoing commitments"
        ]
    },
    "Optimism Bias": {
        "explanation": "We underestimate the likelihood of negative events happening to us.",
        "resources": [
            "📚 Read: 'The Black Swan' by Nassim Taleb",
            "💡 Tip: Plan for worst-case scenarios, hope for the best",
            "📝 Practice: Build emergency funds and insurance coverage"
        ]
    },
    "Loss Aversion": {
        "explanation": "We feel the pain of losses more intensely than the pleasure of equivalent gains.",
        "resources": [
            "📚 Read: 'Fooled by Randomness' by Nassim Taleb",
            "💡 Tip: Focus on long-term expected value, not short-term losses",
            "📝 Practice: Review investment performance yearly, not daily"
        ]
    },
    "Herd Behavior": {
        "explanation": "We follow what others are doing, assuming the crowd must know something we don't.",
        "resources": [
            "📚 Read: 'A Random Walk Down Wall Street' by Burton Malkiel",
            "💡 Tip: FOMO (Fear of Missing Out) is not an investment strategy",
            "📝 Practice: Research investments independently before following trends"
        ]
    },
    "Status Quo Bias": {
        "explanation": "We prefer to keep things the same rather than change, even when change is beneficial.",
        "resources": [
            "📚 Read: 'Switch: How to Change Things When Change Is Hard' by Chip Heath",
            "💡 Tip: Automate good financial habits to overcome inertia",
            "📝 Practice: Review and adjust your financial plan quarterly"
        ]
    }
}

# Archetype profiles for comparison
ARCHETYPE_PROFILES = {
    "Impulsive Spender": {
        "risk_tolerance": 45,
        "impulsivity": 85,
        "loss_aversion": 30,
        "planning_horizon": 25
    },
    "Cautious Planner": {
        "risk_tolerance": 25,
        "impulsivity": 20,
        "loss_aversion": 80,
        "planning_horizon": 85
    },
    "Balanced Investor": {
        "risk_tolerance": 60,
        "impulsivity": 40,
        "loss_aversion": 45,
        "planning_horizon": 70
    },
    "Risk-Taker": {
        "risk_tolerance": 90,
        "impulsivity": 65,
        "loss_aversion": 20,
        "planning_horizon": 55
    }
}

# Achievement system
def check_achievements(persona, progress):
    badges = []
    
    if progress['completed'] >= 15:
        badges.append("🎓 Master Learner")
    if progress['completed'] >= 5:
        badges.append("🌟 Quick Starter")
    if persona['risk_tolerance'] > 70:
        badges.append("🚀 Risk Taker")
    if persona['planning_horizon'] > 70:
        badges.append("📅 Future Focused")
    if persona['impulsivity'] < 30:
        badges.append("🧘 Zen Master")
    if persona['loss_aversion'] < 30:
        badges.append("💎 Fearless")
    
    return badges

# Initialize session state
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = BehavioralAnalyzer()
    st.session_state.selector = AdaptiveScenarioSelector(SCENARIO_DATABASE)
    st.session_state.insight_gen = InsightGenerator()
    st.session_state.current_scenario = None
    st.session_state.started = False
    st.session_state.show_feedback = False
    st.session_state.feedback_text = ""
    st.session_state.hint_shown = False
    st.session_state.page = "home"

# Sidebar with navigation
with st.sidebar:
    st.markdown("### Navigation")
    
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()
    
    if st.button("🎯 Scenarios", use_container_width=True):
        st.session_state.page = "scenarios"
        if not st.session_state.started:
            st.session_state.started = True
            first_scenario = st.session_state.selector.select_next_scenario(
                {'decisions_made': 0}, 
                strategy='adaptive'
            )
            st.session_state.current_scenario = first_scenario
        st.rerun()
    
    if st.button("🧮 Financial Calculators", use_container_width=True):
        st.session_state.page = "calculators"
        st.rerun()

    st.markdown("---")
    st.markdown("### Progress Dashboard")
    progress = st.session_state.selector.get_progress_stats()
    
    st.metric("Scenarios Completed", f"{progress['completed']}/{progress['total_scenarios']}")
    st.progress(progress['completion_percentage'] / 100)
    
    if progress['completed'] >= 3:
        st.markdown("---")
        st.markdown("### Behavioral Profile")
        persona = st.session_state.analyzer.generate_persona()
        
        categories = ['Risk', 'Impulsivity', 'Loss Aversion', 'Planning']
        values = [
            persona['risk_tolerance'],
            persona['impulsivity'],
            persona['loss_aversion'],
            persona['planning_horizon']
        ]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            fillcolor='rgba(99, 102, 241, 0.3)',
            line=dict(color='rgb(99, 102, 241)', width=2)
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            height=300,
            margin=dict(l=50, r=50, t=30, b=30)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.info(f"**Archetype:** {st.session_state.analyzer.get_persona_archetype(persona)}")
        
# =============================================================================
# FINWISE BUDDY - FLOATING CHAT WIDGET 🤖💰
# =============================================================================

# Initialize coach
if 'coach' not in st.session_state:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
        if api_key:
            from utils.finwise_coach import FinWiseCoach
            st.session_state.coach = FinWiseCoach(api_key)
            if 'chat_messages' not in st.session_state:
                st.session_state.chat_messages = []
            if 'show_chat_popup' not in st.session_state:
                st.session_state.show_chat_popup = False
            if 'last_request_time' not in st.session_state:
                st.session_state.last_request_time = 0
        else:
            st.session_state.coach = None
    except Exception as e:
        st.session_state.coach = None

# Floating chat button CSS
if st.session_state.get('coach'):
    st.markdown("""
        <style>
        .floating-chat-btn {
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 1000;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            font-size: 28px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            transition: transform 0.2s;
        }
        .floating-chat-btn:hover {
            transform: scale(1.1);
        }
        </style>
    """, unsafe_allow_html=True)

# Process chat function with rate limiting
def process_chat_message(prompt):
    """Process user message and get AI response"""
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    
    # Check last request time to avoid rate limits
    import time
    current_time = time.time()
    
    if 'last_request_time' not in st.session_state:
        st.session_state.last_request_time = 0
    
    # Enforce 5 second delay between requests
    time_since_last = current_time - st.session_state.last_request_time
    if time_since_last < 5:
        wait_time = int(5 - time_since_last) + 1
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": f"⏱️ Please wait {wait_time} more seconds before asking another question to avoid rate limits!"
        })
        st.rerun()
        return
    
    try:
        persona = st.session_state.analyzer.generate_persona()
        
        # Get decisions safely
        decisions = []
        if hasattr(st.session_state.analyzer, 'decisions'):
            if isinstance(st.session_state.analyzer.decisions, list):
                decisions = st.session_state.analyzer.decisions
        
        progress = st.session_state.selector.get_progress_stats()
        
        # Call coach
        answer = st.session_state.coach.ask(prompt, persona, decisions, progress)
        
        # Update last request time
        st.session_state.last_request_time = time.time()
        
        st.session_state.chat_messages.append({"role": "assistant", "content": answer})
    except Exception as e:
        st.session_state.chat_messages.append({
            "role": "assistant",
            "content": f"❌ Oops! Error: {str(e)}\n\nTry asking differently!"
        })
    
    st.rerun()

# Chat popup modal
@st.dialog("💰 FinWise Buddy Chat", width="large")
def show_chat_popup():
    """Show chat interface in popup"""
    
    # Welcome or chat history
    if not st.session_state.chat_messages:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1.5rem; border-radius: 12px; text-align: center; margin-bottom: 1rem;'>
                <h2 style='margin: 0; color: white;'>👋 Hey! I'm FinWise Buddy!</h2>
                <p style='margin-top: 0.5rem; color: #f0f0f0;'>
                    Your AI financial coach ready to help! 💪
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**💡 I can help you with:**")
        st.markdown("""
        - 📊 Understanding your financial behavior
        - 🎯 Recommending scenarios to try next
        - 💰 Giving personalized money tips
        - 🤔 Explaining why your scores are high/low
        - 📈 Tracking your progress
        """)
        
        # Quick question buttons
        st.markdown("---")
        st.markdown("**🚀 Quick Questions:**")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Explain My Profile", key="qb1", use_container_width=True):
                process_chat_message("Explain my behavioral profile in simple terms")
            if st.button("🎯 Next Scenario?", key="qb2", use_container_width=True):
                process_chat_message("Which scenario should I try next and why?")
        
        with col2:
            if st.button("💰 Money Tips", key="qb3", use_container_width=True):
                process_chat_message("Give me 3 financial tips based on my profile")
            if st.button("📈 My Progress", key="qb4", use_container_width=True):
                process_chat_message("How am I doing? Show my progress")
    else:
        # Display chat messages
        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(f"""
                    <div style='background-color: #1e3a5f; padding: 1rem; 
                                border-radius: 10px; margin: 0.5rem 0;'>
                        <strong>🧑 You:</strong><br>{msg['content']}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style='background-color: #0f5132; padding: 1rem; 
                                border-radius: 10px; margin: 0.5rem 0;'>
                        <strong>🤖 FinWise Buddy:</strong><br>{msg['content']}
                    </div>
                """, unsafe_allow_html=True)
    
    # Input section
    st.markdown("---")
    st.markdown("**💬 Ask me anything:**")
    
    user_input = st.text_area(
        "Your question:",
        key="chat_popup_input",
        height=100,
        placeholder="e.g., Why is my impulsivity score high?",
        label_visibility="collapsed"
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("🚀 Send", type="primary", use_container_width=True, key="send_popup_btn"):
            if user_input and user_input.strip():
                process_chat_message(user_input)
            else:
                st.warning("Please type a question first!")
    
    with col2:
        if st.button("🗑️ Clear", use_container_width=True, key="clear_popup_btn"):
            st.session_state.chat_messages = []
            st.rerun()
    
    # Chat stats
    if st.session_state.chat_messages:
        msg_count = len([m for m in st.session_state.chat_messages if m['role'] == 'user'])
        st.caption(f"💬 {msg_count} questions asked")

# Main area - Floating button trigger
if st.session_state.get('coach'):
    # Add some space at bottom for button
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Floating chat button
    col1, col2, col3 = st.columns([4, 1, 1])
    with col3:
        if st.button("💬", key="floating_chat_btn", help="Chat with FinWise Buddy"):
            show_chat_popup()
else:
    st.info("💡 Add GEMINI_API_KEY to activate FinWise Buddy")




    persona = st.session_state.analyzer.generate_persona()
    progress = st.session_state.selector.get_progress_stats()
        # Achievement badges
    badges = check_achievements(persona, progress)
    if badges:
            st.markdown("**🏆 Achievements:**")
            for badge in badges:
                st.markdown(f"<span class='badge'>{badge}</span>", unsafe_allow_html=True)

# Main content routing
if st.session_state.page == "home":
    # HOME PAGE
    st.markdown('<h1 class="main-header">FinWise</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Behavioral Financial Learning Platform</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hero-banner">
        <h2 style="margin: 0; font-size: 2rem;">Understand Your Financial Decision-Making</h2>
        <p style="margin-top: 1rem; font-size: 1.2rem;">Powered by Behavioral AI & Cognitive Science</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 10px; text-align: center;'>
            <h3 style='color: white; margin: 0; font-size: 2rem;'>15</h3>
            <p style='color: white; margin: 0.5rem 0 0 0;'>Scenarios</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1.5rem; border-radius: 10px; text-align: center;'>
            <h3 style='color: white; margin: 0; font-size: 2rem;'>9</h3>
            <p style='color: white; margin: 0.5rem 0 0 0;'>Biases Tested</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 1.5rem; border-radius: 10px; text-align: center;'>
            <h3 style='color: white; margin: 0; font-size: 2rem;'>AI</h3>
            <p style='color: white; margin: 0.5rem 0 0 0;'>Adaptive</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 1.5rem; border-radius: 10px; text-align: center;'>
            <h3 style='color: white; margin: 0; font-size: 2rem;'>Real-time</h3>
            <p style='color: white; margin: 0.5rem 0 0 0;'>Insights</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 How FinWise Works")
        st.markdown("""
        1. **Face Realistic Scenarios** - Financial decisions you'll actually encounter
        2. **Make Your Choice** - No right or wrong answers
        3. **AI Analyzes Patterns** - Detects biases and decision styles
        4. **Get Personalized Insights** - Understand your financial psychology
        5. **Learn & Improve** - Access resources for your weak areas
        """)
    
    with col2:
        st.markdown("### ✨ What Makes It Different")
        st.markdown("""
        - **Behavioral Focus** - Analyzes how you think, not what you answer
        - **Bias Detection** - Identifies 9 cognitive biases
        - **Adaptive AI** - Scenarios personalize to your profile
        - **Learning Resources** - Get hints and educational materials
        - **Financial Tools** - Built-in calculators for real decisions
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🚀 Start Your Journey", type="primary", use_container_width=True):
            st.session_state.page = "scenarios"
            st.session_state.started = True
            first_scenario = st.session_state.selector.select_next_scenario(
                {'decisions_made': 0}, 
                strategy='adaptive'
            )
            st.session_state.current_scenario = first_scenario
            st.rerun()
    # =============================================================================
    # INTERACTIVE BIAS EXPLAINERS 🧠
    # =============================================================================
    st.markdown("---")
    st.markdown("### 🧠 Understanding Cognitive Biases")
    st.markdown("*Learn about the psychological patterns that influence your financial decisions*")

    # Bias explainer data
    bias_explainers = {
        "⚓ Anchoring Bias": {
            "definition": "The tendency to rely too heavily on the first piece of information you encounter (the 'anchor') when making decisions.",
            "example": "A shirt originally priced at ₹5,000 is on 'sale' for ₹3,000. You feel like you're getting a great deal because of the anchor (₹5,000), even though ₹3,000 might still be overpriced for that shirt!",
            "impact": "Retailers use this constantly! They show inflated 'original prices' to make discounts seem bigger. You end up spending more than you would have without seeing that first number.",
            "how_to_avoid": "Always research actual market prices before buying. Ask yourself: 'Would I pay this much if I hadn't seen the original price?' Ignore the anchor and focus on real value.",
        },
        "⏰ Present Bias": {
            "definition": "The tendency to prioritize immediate rewards over future benefits, even when the future benefit is objectively better.",
            "example": "Choosing ₹100 today instead of ₹150 next month. Or spending ₹150 daily on coffee instead of saving it (₹54,750/year!).",
            "impact": "Makes saving nearly impossible! Your brain values 'now' so much more than 'later' that long-term goals feel abstract and unimportant. This is why retirement savings are so hard.",
            "how_to_avoid": "Automate savings FIRST before you see the money. Visualize your future self - imagine how grateful they'll be. Use the '10-10-10 rule': How will I feel about this in 10 minutes? 10 months? 10 years?",
        },
        "😰 Loss Aversion": {
            "definition": "The pain of losing something is psychologically twice as powerful as the pleasure of gaining something equivalent.",
            "example": "Losing ₹1,000 feels much worse than the joy of winning ₹1,000. This makes you avoid reasonable risks or hold onto losing investments hoping to 'break even'.",
            "impact": "You become too risk-averse, missing growth opportunities. Or worse, you hold losing stocks/investments because selling would 'lock in' the loss, leading to even bigger losses!",
            "how_to_avoid": "Focus on long-term probabilities, not emotions. Past losses are already gone - make decisions based on future potential. Use stop-loss limits to force rational exit points.",
        },
        "🔍 Confirmation Bias": {
            "definition": "The tendency to search for, interpret, and remember information in a way that confirms your existing beliefs, while ignoring contradicting evidence.",
            "example": "You want to buy a new phone, so you only read positive reviews and ignore negative ones. Or you believe crypto is great, so you only follow crypto bulls on Twitter.",
            "impact": "You make decisions based on incomplete information, leading to costly mistakes. You become trapped in echo chambers where bad ideas never get challenged.",
            "how_to_avoid": "Actively seek opposing viewpoints. Before any big decision, deliberately search for reasons NOT to do it. Ask: 'What would prove me wrong?' Play devil's advocate with yourself.",
        },
        "💸 Sunk Cost Fallacy": {
            "definition": "Continuing something because you've already invested time, money, or effort, even when it's clearly not working and continuing makes no rational sense.",
            "example": "Staying in a bad stock because 'I've already lost so much, I can't quit now!' Or finishing a terrible movie because you paid for the ticket. Or keeping a gym membership you never use.",
            "impact": "You throw good money after bad, escalating losses instead of cutting them. Past investments cloud your judgment about future decisions. You waste resources on losing propositions.",
            "how_to_avoid": "Remember: Sunk costs are GONE. They're history. Make decisions based only on future costs and benefits. Ask: 'If I were starting fresh today, would I make this same choice?'",
        },
        "😎 Overconfidence Bias": {
            "definition": "Overestimating your knowledge, abilities, and the precision of your predictions. Believing you're better at decisions than you actually are.",
            "example": "Day trading stocks because you 'figured out the pattern' after 3 winning trades. Or thinking you can time the market. Or not doing research because 'I know enough already'.",
            "impact": "You take excessive risks without proper research. You ignore expert advice. You lose money on speculative bets. Studies show overconfident investors earn lower returns!",
            "how_to_avoid": "Track your predictions and decisions - you'll see you're wrong often! Always do proper research. Seek expert opinions. Remember: Even pros get it wrong regularly. Stay humble!",
        },
        "🐑 Herd Mentality": {
            "definition": "Following what everyone else is doing, assuming the crowd knows better, without doing your own research or thinking independently.",
            "example": "Buying crypto in 2021 because 'everyone's talking about it!' Or investing in a stock because it's trending on social media. Or rushing to buy toilet paper during COVID panic.",
            "impact": "You buy high when everyone's excited (market top) and sell low when everyone's panicking (market bottom). The crowd is often wrong at extremes! This destroys wealth systematically.",
            "how_to_avoid": "Do your own research always. Be skeptical of trends and hype. Remember Warren Buffett: 'Be fearful when others are greedy, greedy when others are fearful.' Think independently!",
        },
        "🧠 Mental Accounting": {
            "definition": "Treating money differently based on its source or intended purpose, even though money is fungible (all money is the same).",
            "example": "Spending gift money more freely than salary. Saving in a 3% savings account while carrying 18% credit card debt. Having separate 'vacation fund' and 'emergency fund' instead of optimizing total returns.",
            "impact": "You make irrational decisions that cost you money. You don't optimize across all your finances. You might save while in debt, effectively losing 15% on that money!",
            "how_to_avoid": "Treat all money the same - it's all YOUR money! Optimize across your entire financial life. Pay high-interest debt before saving. View finances holistically, not in separate 'buckets'.",
        },
    }

    # Display biases in expandable sections
    for bias_name, bias_info in bias_explainers.items():
        with st.expander(f"{bias_name}", expanded=False):
            # Definition
            st.markdown(f"**📖 What is it?**")
            st.info(bias_info["definition"])
            
            # Real-world example
            st.markdown(f"**💡 Real-World Example:**")
            st.success(bias_info["example"])
            
            # Impact on finances
            st.markdown(f"**💰 Impact on Your Money:**")
            st.warning(bias_info["impact"])
            
            # How to avoid
            st.markdown(f"**🛡️ How to Avoid This Bias:**")
            st.success(bias_info["how_to_avoid"])

    # =============================================================================
    # VIDEO EXPLAINERS - QUICK LEARNING 🎥
    # =============================================================================
    st.markdown("---")
    st.markdown("### 🎥 Video Explainers - Master Money Skills Fast!")
    st.markdown("*Watch curated videos to understand key concepts in minutes*")

    # Video library with thumbnails - ALL VERIFIED WORKING VIDEOS!
    video_library = {
        "🧠 Cognitive Biases": [
            {
                "title": "Anchoring Bias Explained",
                "video_id": "JLeyIdWv2Q8",
                "description": "How the first number you see controls your decisions",
                "duration": "3:45",
                "channel": "Sprouts"
            },
            {
                "title": "Present Bias - Why We Choose Now Over Later",
                "video_id": "49UlfbT1JTY",
                "description": "Understanding why immediate rewards feel so tempting",
                "duration": "8:11",
                "channel": "Behavioral Economics"
            },
            {
                "title": "Loss Aversion Explained",
                "video_id": "Igr-avFbfb8",
                "description": "Why losing ₹100 hurts more than winning ₹100 feels good",
                "duration": "3:56",
                "channel": "Marketing Business Network"
            },
            {
                "title": "Sunk Cost Fallacy",
                "video_id": "q4ZOY5fI-e8",
                "description": "Why we throw good money after bad decisions",
                "duration": "3:26",
                "channel": "Marketing Business Network"
            },
            {
                "title": "Confirmation Bias in Investing",
                "video_id": "5lIkLg1F7eM",
                "description": "How to overcome this costly mental trap",
                "duration": "6:45",
                "channel": "Financial Education"
            },
            {
                "title": "Mental Accounting & Money Mistakes",
                "video_id": "N2GLiZPJp-s",
                "description": "Why we treat salary and gift money differently",
                "duration": "5:17",
                "channel": "Finance Unlocked"
            },
        ],
        "💰 Money Skills": [
            {
                "title": "Emergency Fund - What & How Much",
                "video_id": "R2OvsQCubGw",
                "description": "3-6 months expenses explained simply",
                "duration": "7:26",
                "channel": "Financial Bunny"
            },
            {
                "title": "50/30/20 Budget Rule",
                "video_id": "LKxOamnP8J4",
                "description": "The simplest budgeting method that works",
                "duration": "6:02",
                "channel": "Khan Academy"
            },
            {
                "title": "How to Start SIP in India",
                "video_id": "ZXLATRO3Ifw",
                "description": "Mutual funds investing for beginners",
                "duration": "8:45",
                "channel": "Sanjay Kathuria"
            },
            {
                "title": "Credit Card Management",
                "video_id": "IWsKUCr-tdk",
                "description": "Avoid the debt trap, use cards smartly",
                "duration": "9:12",
                "channel": "Meghala"
            },
        ],
        "📈 Investing & Finance": [
            {
                "title": "Herd Mentality in Stock Market",
                "video_id": "XloSxBEUCNA",
                "description": "Why following the crowd loses money",
                "duration": "12:00",
                "channel": "Financial Education"
            },
            {
                "title": "Compound Interest Explained",
                "video_id": "TM2yIF0bASM",
                "description": "The magic of money growth over time",
                "duration": "31:45",
                "channel": "The Organic Chemistry Tutor"
            },
            {
                "title": "Behavioral Finance Basics",
                "video_id": "YUedGJ9KPTg",
                "description": "Prospect theory and mental accounting",
                "duration": "13:13",
                "channel": "Corporate Finance Institute"
            },
        ],
        "💡 Student Money Hacks": [
            {
                "title": "Personal Finance Tips for Students",
                "video_id": "eOmTJDMhkXw",
                "description": "How to manage money as a student",
                "duration": "3:47",
                "channel": "Unacademy"
            },
            {
                "title": "5 Simple Hacks to Save Big",
                "video_id": "J_cuCDyQc7g",
                "description": "Practical saving tips for Indian students",
                "duration": "3:36",
                "channel": "Finance with Sharan"
            },
            {
                "title": "Money Mistakes Indians Must Avoid",
                "video_id": "O8UwkDsVAX8",
                "description": "UPI habits, subscriptions, and common pitfalls",
                "duration": "13:45",
                "channel": "Sanjay Kathuria"
            },
            {
                "title": "Complete Financial Planning for 20s",
                "video_id": "BChDsJdOOrQ",
                "description": "Step-by-step money guide for young adults",
                "duration": "38:00",
                "channel": "Ankur Warikoo"
            },
        ],
    }

    # Display videos in tabs
    video_tabs = st.tabs(list(video_library.keys()))

    for tab, category in zip(video_tabs, video_library.keys()):
        with tab:
            videos = video_library[category]
            
            # Display videos in 2-column grid
            for i in range(0, len(videos), 2):
                cols = st.columns(2)
                
                for j, col in enumerate(cols):
                    if i + j < len(videos):
                        video = videos[i + j]
                        video_url = f"https://www.youtube.com/watch?v={video['video_id']}"
                        thumbnail_url = f"https://img.youtube.com/vi/{video['video_id']}/hqdefault.jpg"
                        
                        with col:
                            # Video thumbnail
                            st.image(thumbnail_url, use_container_width=True)
                            
                            # Video info
                            st.markdown(f"**{video['title']}** ⏱️ {video['duration']}")
                            st.caption(f"{video['description']}")
                            st.caption(f"📺 {video['channel']}")
                            
                            # Watch button
                            st.link_button("▶️ Watch on YouTube", video_url, use_container_width=True)
                            
                            st.markdown("")  # Spacing



elif st.session_state.page == "calculators":
    # FINANCIAL CALCULATORS PAGE
    st.markdown("## 🧮 Financial Calculators")
    st.markdown("Use these tools to make informed financial decisions")
    
    tab1, tab2, tab3 = st.tabs(["💰 Compound Interest", "🏦 EMI Calculator", "🚨 Emergency Fund"])
    
    with tab1:
        st.markdown("### Compound Interest Calculator")
        st.markdown("See how your money grows over time")
        
        col1, col2 = st.columns(2)
        
        with col1:
            principal = st.number_input("Initial Amount (₹)", min_value=1000, value=10000, step=1000)
            monthly = st.number_input("Monthly Contribution (₹)", min_value=0, value=5000, step=500)
            rate = st.slider("Annual Interest Rate (%)", min_value=1.0, max_value=20.0, value=12.0, step=0.5)
            years = st.slider("Time Period (years)", min_value=1, max_value=40, value=10)
        
        with col2:
            monthly_rate = rate / 12 / 100
            months = years * 12
            
            fv = principal * ((1 + monthly_rate) ** months)
            fv += monthly * (((1 + monthly_rate) ** months - 1) / monthly_rate)
            
            total_invested = principal + (monthly * months)
            gains = fv - total_invested
            
            st.metric("Total Invested", f"₹{total_invested:,.0f}")
            st.metric("Future Value", f"₹{fv:,.0f}", delta=f"₹{gains:,.0f} gains")
            st.metric("ROI", f"{(gains/total_invested)*100:.1f}%")
            
            st.success(f"💡 You'll earn ₹{gains:,.0f} just by investing consistently!")
    
    with tab2:
        st.markdown("### EMI Calculator")
        st.markdown("Calculate your monthly loan payments")
        
        col1, col2 = st.columns(2)
        
        with col1:
            loan_amount = st.number_input("Loan Amount (₹)", min_value=10000, value=500000, step=10000)
            loan_rate = st.slider("Interest Rate (% per annum)", min_value=5.0, max_value=25.0, value=12.0, step=0.5)
            loan_tenure = st.slider("Tenure (months)", min_value=6, max_value=360, value=60)
        
        with col2:
            r = loan_rate / 12 / 100
            emi = (loan_amount * r * ((1 + r) ** loan_tenure)) / (((1 + r) ** loan_tenure) - 1)
            total_payment = emi * loan_tenure
            interest_paid = total_payment - loan_amount
            
            st.metric("Monthly EMI", f"₹{emi:,.0f}")
            st.metric("Total Payment", f"₹{total_payment:,.0f}")
            st.metric("Interest Paid", f"₹{interest_paid:,.0f}", delta=f"-{(interest_paid/loan_amount)*100:.1f}%")
            
            if interest_paid > loan_amount * 0.5:
                st.warning(f"⚠️ You'll pay ₹{interest_paid:,.0f} in interest - consider a shorter tenure!")
    
    with tab3:
        st.markdown("### Emergency Fund Calculator")
        st.markdown("How much should you save for emergencies?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            monthly_expenses = st.number_input("Monthly Expenses (₹)", min_value=5000, value=30000, step=1000)
            months_coverage = st.slider("Months of Coverage", min_value=3, max_value=12, value=6)
            current_savings = st.number_input("Current Emergency Fund (₹)", min_value=0, value=50000, step=5000)
        
        with col2:
            target = monthly_expenses * months_coverage
            remaining = max(0, target - current_savings)
            progress_pct = min(100, (current_savings / target) * 100)
            
            st.metric("Target Emergency Fund", f"₹{target:,.0f}")
            st.metric("Current Progress", f"{progress_pct:.0f}%")
            st.metric("Still Need", f"₹{remaining:,.0f}")
            
            st.progress(progress_pct / 100)
            
            if remaining > 0:
                for months in [3, 6, 12]:
                    monthly_save = remaining / months
                    st.info(f"Save ₹{monthly_save:,.0f}/month → Reach goal in {months} months")



elif st.session_state.page == "scenarios":
    
    if st.session_state.current_scenario is None:
        progress = st.session_state.selector.get_progress_stats()
        
        if progress['completed'] >= 3:
            persona = st.session_state.analyzer.generate_persona()
        else:
            persona = {'decisions_made': progress['completed']}
        
        next_scenario = st.session_state.selector.select_next_scenario(persona, strategy='adaptive')
        
        if next_scenario is None:
            # FINAL RESULTS
            st.balloons()
            st.success("🎉 Congratulations! You've completed all scenarios!")
            
            persona = st.session_state.analyzer.generate_persona()
            insights = st.session_state.insight_gen.generate_persona_insights(persona)
            
            # Achievement badges
            badges = check_achievements(persona, progress)
            if badges:
                st.markdown("### 🏆 Achievements Unlocked!")
                for badge in badges:
                    st.markdown(f"<span class='badge'>{badge}</span>", unsafe_allow_html=True)
                st.markdown("---")
            
            st.markdown("### Your Final Behavioral Profile")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Risk Tolerance", f"{persona['risk_tolerance']:.0f}/100")
            col2.metric("Impulsivity", f"{persona['impulsivity']:.0f}/100")
            col3.metric("Loss Aversion", f"{persona['loss_aversion']:.0f}/100")
            col4.metric("Planning Horizon", f"{persona['planning_horizon']:.0f}/100")
            
            # COMPARE WITH ARCHETYPES
            st.markdown("---")
            st.markdown("### 📊 Compare with Financial Archetypes")
            
            categories = ['Risk Tolerance', 'Impulsivity', 'Loss Aversion', 'Planning Horizon']
            
            fig = go.Figure()
            
            your_values = [
                persona['risk_tolerance'],
                persona['impulsivity'],
                persona['loss_aversion'],
                persona['planning_horizon']
            ]
            
            fig.add_trace(go.Scatterpolar(
                r=your_values,
                theta=categories,
                fill='toself',
                name='You',
                fillcolor='rgba(99, 102, 241, 0.3)',
                line=dict(color='rgb(99, 102, 241)', width=3)
            ))
            
            archetype_select = st.selectbox(
                "Compare with:",
                list(ARCHETYPE_PROFILES.keys())
            )
            
            archetype = ARCHETYPE_PROFILES[archetype_select]
            archetype_values = [
                archetype['risk_tolerance'],
                archetype['impulsivity'],
                archetype['loss_aversion'],
                archetype['planning_horizon']
            ]
            
            fig.add_trace(go.Scatterpolar(
                r=archetype_values,
                theta=categories,
                fill='toself',
                name=archetype_select,
                fillcolor='rgba(239, 68, 68, 0.2)',
                line=dict(color='rgb(239, 68, 68)', width=2, dash='dash')
            ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=True,
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.markdown("### 💪 Strengths")
                for strength in insights['strengths']:
                    st.markdown(f'<div class="strength-box">✓ {strength}</div>', unsafe_allow_html=True)
            
            with col_right:
                st.markdown("### 📈 Growth Areas")
                for growth in insights['growth_areas']:
                    st.markdown(f'<div class="growth-box">→ {growth}</div>', unsafe_allow_html=True)
            
            # Personalized learning path
            st.markdown("---")
            st.markdown("### 📚 Your Personalized Learning Path")
            
            weak_biases = []
            if persona['impulsivity'] > 70:
                weak_biases.append("Present Bias")
            if persona['loss_aversion'] > 70:
                weak_biases.append("Loss Aversion")
            if persona['planning_horizon'] < 40:
                weak_biases.append("Hyperbolic Discounting")
            if persona['risk_tolerance'] < 30:
                weak_biases.append("Loss Aversion")
            
            if weak_biases:
                st.info("Based on your profile, we recommend focusing on these areas:")
                for bias in set(weak_biases):
                    with st.expander(f"📖 Learn about {bias}"):
                        resources = LEARNING_RESOURCES.get(bias, {})
                        st.markdown(f"**{resources.get('explanation', '')}**")
                        st.markdown("")
                        for resource in resources.get('resources', []):
                            st.markdown(f"- {resource}")
            else:
                st.success("🌟 Excellent! Your decision-making is well-balanced across all areas!")
            
            # WORKING PDF DOWNLOAD
            st.markdown("---")
            pdf_buffer = generate_pdf_report(persona, insights, progress)
            
            if pdf_buffer:
                st.download_button(
                    label="📄 Download Full Report (PDF)",
                    data=pdf_buffer,
                    file_name=f"FinWise_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf",
                    type="primary"
                )
            else:
                if st.button("📄 Download Full Report (PDF)", type="primary"):
                    st.warning("⚠️ Install reportlab to enable PDF downloads: pip install reportlab")
        
        else:
            st.session_state.current_scenario = next_scenario
            st.session_state.hint_shown = False
            st.rerun()
    
    else:
        # SHOW SCENARIO
        current_scenario_id = st.session_state.current_scenario
        progress = st.session_state.selector.get_progress_stats()
        scenario = st.session_state.current_scenario

        st.markdown(f"### Scenario {progress['completed'] + 1}: {scenario['topic']}")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"**Testing:** {scenario['bias_tested']}")
        with col2:
            difficulty_stars = "⭐" * scenario['difficulty'] + "☆" * (3 - scenario['difficulty'])
            st.info(f"**Difficulty:** {difficulty_stars}")
        
        with st.expander(f"ℹ️ What is {scenario['bias_tested']}?"):
            bias_info = LEARNING_RESOURCES.get(scenario['bias_tested'], {})
            st.markdown(bias_info.get('explanation', 'Information about this cognitive bias.'))
        
# Get current scenario data
scenario = st.session_state.current_scenario

# Only show scenario if one is selected
if scenario is not None:
    
    # Show scenario with visualization
    col_left, col_right = st.columns([1.5, 1])

    with col_left:
        st.markdown(f'<div class="scenario-card">{scenario["scenario_text"]}</div>', unsafe_allow_html=True)

    with col_right:
        # Add visualization if available
        viz = create_scenario_visualization(scenario)
        if viz:
            st.plotly_chart(viz, use_container_width=True)
        else:
            # Show helpful info box instead
            st.info("💡 **Think Carefully:**\n\nConsider both short-term and long-term impacts of your decision.")


        if not st.session_state.show_feedback:
            if not st.session_state.hint_shown:
                if st.button("💡 Need a hint?", type="secondary"):
                    st.session_state.hint_shown = True
                    st.rerun()
            
            if st.session_state.hint_shown:
                hint = HINTS.get(scenario['id'], "Think carefully about the long-term implications.")
                st.markdown(f'<div class="hint-box">💡 <strong>Hint:</strong> {hint}</div>', unsafe_allow_html=True)
            
            decision_value = None
            
            if scenario['decision_type'] == 'slider':
                st.markdown("#### Your Decision")
                decision_value = st.slider(
                    "Move the slider",
                    0, 100, 50,
                    label_visibility="collapsed"
                )
                if 'slider_labels' in scenario:
                    labels = scenario['slider_labels']
                    col1, col2 = st.columns(2)
                    col1.caption(f"← {labels[0]}")
                    col2.caption(f"{labels[-1]} →")
            
            elif scenario['decision_type'] == 'choice':
                st.markdown("#### Your Decision")
                options = scenario['options']
                selected = st.radio("Choose one:", options, index=None, label_visibility="collapsed")
                if selected:
                    decision_value = options.index(selected)
            
            st.markdown("#### Confidence Level")
            confidence = st.select_slider(
                "confidence",
                options=[1, 2, 3, 4, 5],
                value=3,
                format_func=lambda x: ["😟 Not sure", "🤔 Slightly", "😐 Moderate", "😊 Confident", "😎 Very confident"][x-1],
                label_visibility="collapsed"
            )
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("Submit Decision", type="primary", use_container_width=True, disabled=(decision_value is None)):
                    decision_time = 15.0
                    
                    decision_data = {
                        'decision_value': decision_value,
                        'decision_time': decision_time,
                        'confidence': confidence,
                        'revision_count': 0,
                        'timestamp': datetime.now()
                    }
                    
                    st.session_state.analyzer.log_decision(scenario['id'], decision_data)
                    st.session_state.selector.mark_scenario_completed(scenario['id'])
                    
                    feedback = st.session_state.insight_gen.generate_scenario_feedback(
                        scenario['id'], decision_data, scenario
                    )
                    
                    st.session_state.feedback_text = feedback
                    st.session_state.show_feedback = True
                    st.rerun()
        
        else:
            # FEEDBACK WITH FIXED CASE STUDY
            st.success("✅ Decision Recorded!")
            st.markdown(st.session_state.feedback_text)
            
            # FIXED Real-world case study with better visibility
            case_study = CASE_STUDIES.get(scenario['bias_tested'])
            if case_study:
                st.markdown("---")
                st.markdown("### 📰 Real-World Impact")
                st.markdown(f'<div class="case-study-box">💡 <strong>Case Study:</strong><br><br>{case_study}</div>', unsafe_allow_html=True)
            
            # Learning resources
            st.markdown("---")
            with st.expander(f"📚 Learn More About {scenario['bias_tested']}"):
                resources = LEARNING_RESOURCES.get(scenario['bias_tested'], {})
                st.markdown(f"**Understanding {scenario['bias_tested']}**")
                st.markdown(resources.get('explanation', ''))
                st.markdown("")
                st.markdown("**Recommended Resources:**")
                for resource in resources.get('resources', []):
                    st.markdown(f"- {resource}")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("Continue →", type="primary", use_container_width=True):
                    st.session_state.current_scenario = None
                    st.session_state.show_feedback = False
                    st.session_state.feedback_text = ""
                    st.session_state.hint_shown = False
                    st.rerun()

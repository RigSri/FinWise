"""
AI Insight Generator
Generates reflective, mentor-like insights from behavioral data
"""


import numpy as np
from datetime import datetime


class InsightGenerator:
    """Generates personalized insights based on behavioral persona"""
    
    def __init__(self):
        self.insight_templates = self._load_templates()
    
    def _load_templates(self):
        """Load insight templates for different behavioral patterns"""
        return {
            'high_present_bias': [
                "You often prioritize immediate certainty over long-term value, even when delayed gains are significantly higher. Consider: would waiting {time} really impact your current needs?",
                "Your decisions show a pattern of preferring 'now' over 'later'. This is natural, but {percentage}% of your choices favored short-term rewards despite better long-term options.",
                "Immediate gratification appears strongly in your decision pattern. You've chosen instant options {count} times when waiting could have increased value by {value}%."
            ],
            'high_loss_aversion': [
                "You seem quite cautious about potential losses, even when gains are likely. Your decisions avoid risk {percentage}% more than similar users.",
                "Loss aversion is evident—you're {ratio}x more sensitive to losses than gains. This protective instinct may be limiting growth opportunities.",
                "You consistently choose safer options even when expected value favors risk. In {count} scenarios, you avoided uncertainty despite favorable odds."
            ],
            'high_impulsivity': [
                "Your average decision time is {time} seconds—faster than {percentage}% of users. Quick thinking is valuable, but some decisions might benefit from reflection.",
                "You rarely revise your choices (only {count} times across {total} decisions). This confidence is good, but complex scenarios may need deeper analysis.",
                "You decide quickly and stick with it. While decisive, {percentage}% of your rapid choices were in scenarios designed for deliberation."
            ],
            'anchoring_bias': [
                "You were influenced by initial price points in {count} scenarios, even when actual value was clearly different. Try evaluating absolute value first.",
                "Discounts and reference prices seem to sway your decisions significantly. In scenario {scenario}, the 'original price' affected your choice despite identical products.",
                "Your decisions show susceptibility to anchoring—initial numbers shape your judgment by approximately {percentage}% more than expected."
            ],
            'sunk_cost_fallacy': [
                "You continued commitments based on past investments rather than future value {count} times. Past costs are gone—focus on what lies ahead.",
                "In scenario {scenario}, you let money already spent influence your decision. Economically, only future costs and benefits should matter.",
                "Your pattern suggests difficulty letting go of previous investments. This appears in {percentage}% of your continuation decisions."
            ],
            'good_planning': [
                "Strong long-term thinking! You consistently evaluate future implications, shown in {count} scenarios where you chose delayed but superior outcomes.",
                "Your planning horizon is longer than {percentage}% of users. You naturally balance present needs with future goals.",
                "Impressive patience in decision-making. You've demonstrated willingness to wait for {time} to gain {value}% more value."
            ],
            'balanced_approach': [
                "You show balanced decision-making across {count} scenarios. You weigh short and long-term factors without extreme bias.",
                "Your risk-taking is calibrated well—taking calculated risks in {count} scenarios while being appropriately cautious in {other_count} others.",
                "You adapt your strategy based on context. In high-stakes scenarios, you're careful; in lower-stakes ones, you're more exploratory."
            ]
        }
    
    def generate_scenario_feedback(self, scenario_id, decision_data, scenario_info):
        """
        Generate immediate feedback for a single scenario
        
        Parameters:
        - scenario_id: str
        - decision_data: dict with decision details
        - scenario_info: dict with scenario metadata
        
        Returns: str (feedback message)
        """
        bias_tested = scenario_info.get('bias_tested', '')
        decision_value = decision_data.get('decision_value', 0)
        decision_time = decision_data.get('decision_time', 30)
        ideal_range = scenario_info.get('ideal_range', [0, 100])
        
        feedback_parts = []
        
        # Decision acknowledgment
        feedback_parts.append(f"📊 **Decision Recorded**")
        
        # Time-based insight
        if decision_time < 10:
            feedback_parts.append(f"⚡ You decided in {decision_time:.1f} seconds—very quickly. Was this intuitive, or could more reflection help?")
        elif decision_time > 60:
            feedback_parts.append(f"🤔 You took {decision_time:.1f} seconds. Careful deliberation shows thoughtfulness.")
        
        # Value-based insight (for slider scenarios)
        if 'slider' in scenario_info.get('decision_type', ''):
            if decision_value < ideal_range[0]:
                feedback_parts.append(f"💭 Your choice leans toward {self._interpret_slider_low(scenario_id)}. Consider if this aligns with your long-term goals.")
            elif decision_value > ideal_range[1]:
                feedback_parts.append(f"💭 Your choice leans toward {self._interpret_slider_high(scenario_id)}. Balance is key—does this feel right?")
            else:
                feedback_parts.append(f"✅ Your choice falls in a balanced range. You're weighing multiple factors well.")
        
        # Bias-specific reflection
        if 'Present Bias' in bias_tested:
            feedback_parts.append("🔍 **Reflection**: Did immediate availability affect your choice more than future value?")
        elif 'Anchoring' in bias_tested:
            feedback_parts.append("🔍 **Reflection**: Were you influenced by the initial price, or did you focus on absolute value?")
        elif 'Sunk Cost' in bias_tested:
            feedback_parts.append("🔍 **Reflection**: Did money already spent influence this decision? Future value matters most.")
        
        return "\n\n".join(feedback_parts)
    
    def _interpret_slider_low(self, scenario_id):
        """Interpret what low slider values mean for each scenario"""
        interpretations = {
            'S001': "spending now over saving",
            'S006': "minimal emergency buffer",
            'S007': "guaranteed safety over growth"
        }
        return interpretations.get(scenario_id, "immediate options")
    
    def _interpret_slider_high(self, scenario_id):
        """Interpret what high slider values mean for each scenario"""
        interpretations = {
            'S001': "maximum saving over enjoyment",
            'S006': "very large emergency fund",
            'S007': "aggressive investment over stability"
        }
        return interpretations.get(scenario_id, "delayed options")
    
    def generate_persona_insights(self, persona):
        """
        Generate comprehensive insights from complete persona
        
        Parameters:
        - persona: dict from BehavioralAnalyzer.generate_persona()
        
        Returns: dict with insights by category
        """
        insights = {
            'strengths': [],
            'growth_areas': [],
            'bias_alerts': [],
            'archetype_description': ''
        }
        
        # Risk tolerance insights - LOWERED THRESHOLDS
        risk = persona['risk_tolerance']
        if risk > 50:  # Changed from 70
            insights['strengths'].append(f"You're comfortable with calculated risks (risk: {risk:.0f}/100) - essential for wealth building!")
        elif risk > 30 and risk <= 70:  # NEW: Balanced range
            insights['strengths'].append(f"You have a balanced approach to risk (risk: {risk:.0f}/100) - not too conservative, not too reckless!")
        elif risk < 25:  # Changed from 30
            insights['growth_areas'].append(f"You avoid risk even when odds are favorable. Your risk tolerance ({risk:.0f}/100) may limit growth opportunities.")
        
        # Impulsivity insights
        impulsivity = persona['impulsivity']
        if impulsivity > 70:
            insights['growth_areas'].append(f"You decide very quickly (impulsivity: {impulsivity:.0f}/100). Complex financial decisions often benefit from deliberation.")
        elif impulsivity < 50:  # Changed from 30
            insights['strengths'].append(f"You think carefully before deciding (impulsivity: {impulsivity:.0f}/100), weighing multiple factors systematically.")
        
        # Planning horizon insights - LOWERED THRESHOLDS
        planning = persona['planning_horizon']
        if planning > 55:  # Changed from 65
            insights['strengths'].append(f"Strong future orientation! You naturally consider long-term implications (planning: {planning:.0f}/100).")
        elif planning > 40:  # NEW: Moderate planning
            insights['strengths'].append(f"You balance present and future well (planning: {planning:.0f}/100) - you think ahead without ignoring today.")
        elif planning < 35:
            insights['growth_areas'].append(f"You focus heavily on the present (planning: {planning:.0f}/100). Try asking: 'How will this look in 6 months?'")
        
        # Loss aversion insights
        loss_aversion = persona['loss_aversion']
        if loss_aversion < 45:  # NEW: Low loss aversion is a strength
            insights['strengths'].append(f"You don't let fear of losses paralyze you (loss aversion: {loss_aversion:.0f}/100) - this helps you seize opportunities!")
        elif loss_aversion > 65:
            insights['bias_alerts'].append(f"⚠️ **Loss Aversion**: You're {loss_aversion:.0f}% more sensitive to losses than gains. This may cause you to miss opportunities.")
        
        # Bias pattern insights
        biases = persona.get('bias_patterns', {})
        for bias_name, severity in biases.items():
            if severity > 60:
                if bias_name == 'present_bias':
                    insights['bias_alerts'].append(f"⚠️ **Present Bias** ({severity:.0f}/100): You consistently favor immediate rewards over larger future gains.")
                elif bias_name == 'anchoring':
                    insights['bias_alerts'].append(f"⚠️ **Anchoring** ({severity:.0f}/100): Initial numbers (prices, discounts) disproportionately influence your decisions.")
                elif bias_name == 'sunk_cost':
                    insights['bias_alerts'].append(f"⚠️ **Sunk Cost Fallacy** ({severity:.0f}/100): Past investments are affecting future choices. Focus on what's ahead, not what's spent.")
        
        # FALLBACK: Ensure at least one strength always shows
        if len(insights['strengths']) == 0:
            insights['strengths'].append("🎉 You completed all scenarios - that shows commitment to learning and self-improvement!")
            insights['strengths'].append("💪 Your willingness to challenge your thinking is a huge strength in personal finance.")
        
        return insights
    
    def generate_session_summary(self, persona, decisions_count):
        """
        Generate end-of-session summary with actionable insights
        """
        summary = f"""
## 🎯 Session Summary

**Decisions Analyzed**: {decisions_count}
**Behavioral Archetype**: {self._get_archetype_name(persona)}

### 📈 Your Decision Profile

- **Risk Tolerance**: {persona['risk_tolerance']:.0f}/100 {self._risk_label(persona['risk_tolerance'])}
- **Impulsivity**: {persona['impulsivity']:.0f}/100 {self._impulsivity_label(persona['impulsivity'])}
- **Planning Horizon**: {persona['planning_horizon']:.0f}/100 {self._planning_label(persona['planning_horizon'])}
- **Loss Aversion**: {persona['loss_aversion']:.0f}/100 {self._loss_label(persona['loss_aversion'])}

### 💡 Key Pattern

{self._generate_key_pattern(persona)}

### 🎓 Growth Suggestion

{self._generate_growth_suggestion(persona)}
        """
        
        return summary.strip()
    
    def _get_archetype_name(self, persona):
        """Determine archetype name from persona metrics"""
        risk = persona['risk_tolerance']
        planning = persona['planning_horizon']
        impulsivity = persona['impulsivity']
        
        if risk > 60 and planning > 60:
            return "🧠 Strategic Investor"
        elif risk < 40 and impulsivity < 40:
            return "🛡️ Cautious Planner"
        elif impulsivity > 70:
            return "⚡ Impulsive Decider"
        elif planning < 30:
            return "🎯 Present-Focused"
        else:
            return "⚖️ Balanced Decision-Maker"
    
    def _risk_label(self, score):
        if score > 70: return "(High - Comfortable with uncertainty)"
        elif score > 40: return "(Moderate - Balanced approach)"
        else: return "(Low - Prefer safety)"
    
    def _impulsivity_label(self, score):
        if score > 70: return "(High - Quick decisions)"
        elif score > 40: return "(Moderate - Thoughtful pace)"
        else: return "(Low - Very deliberate)"
    
    def _planning_label(self, score):
        if score > 65: return "(Long-term thinker)"
        elif score > 35: return "(Balanced horizon)"
        else: return "(Short-term focused)"
    
    def _loss_label(self, score):
        if score > 65: return "(High - Very cautious about losses)"
        elif score > 35: return "(Moderate - Balanced)"
        else: return "(Low - Focus on gains)"
    
    def _generate_key_pattern(self, persona):
        """Generate the most important behavioral pattern observation"""
        risk = persona['risk_tolerance']
        planning = persona['planning_horizon']
        impulsivity = persona['impulsivity']
        biases = persona.get('bias_patterns', {})
        
        # Find dominant bias
        dominant_bias = max(biases.items(), key=lambda x: x[1]) if biases else (None, 0)
        
        if dominant_bias[1] > 60:
            return f"Your decisions show strong {dominant_bias[0].replace('_', ' ')} ({dominant_bias[1]:.0f}/100). This pattern appeared consistently across multiple scenarios."
        elif impulsivity > 70:
            return f"You decide very quickly (avg. decision time significantly below baseline). While decisive, some complex scenarios benefit from additional reflection."
        elif planning > 70:
            return f"You naturally think long-term, consistently favoring future value over immediate gratification. This serves you well in wealth-building scenarios."
        elif risk < 30:
            return f"You consistently choose safety over growth, even when expected returns favor calculated risks. Consider: what's the real downside?"
        else:
            return f"You show balanced decision-making, adapting your approach based on scenario context. This flexibility is valuable."
    
    def _generate_growth_suggestion(self, persona):
        """Generate personalized growth suggestion"""
        risk = persona['risk_tolerance']
        planning = persona['planning_horizon']
        impulsivity = persona['impulsivity']
        biases = persona.get('bias_patterns', {})
        
        suggestions = []
        
        if impulsivity > 70:
            suggestions.append("Try a 30-second pause before finalizing important decisions. Ask: 'What am I not considering?'")
        
        if planning < 35:
            suggestions.append("Before choosing, visualize yourself 6 months from now. Which option would 'future you' prefer?")
        
        if risk < 30:
            suggestions.append("Start with small, reversible risks to build comfort with uncertainty. Not all risks are equal.")
        
        if biases.get('present_bias', 0) > 60:
            suggestions.append("When comparing options, calculate the actual cost of immediacy. Is 'now' worth the premium?")
        
        if biases.get('sunk_cost', 0) > 60:
            suggestions.append("Practice asking: 'If I were starting fresh today, would I make this same choice?' Past costs shouldn't chain future decisions.")
        
        return suggestions[0] if suggestions else "Continue practicing with diverse scenarios to refine your decision patterns."

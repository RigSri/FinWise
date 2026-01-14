"""
Adaptive Scenario Selector
AI-driven system to choose optimal next scenario based on behavioral persona
"""

import numpy as np
import random
from sklearn.metrics.pairwise import cosine_similarity

class AdaptiveScenarioSelector:
    """
    Intelligently selects next scenario based on:
    - Current persona profile
    - Learning gaps (weak areas)
    - Progression difficulty
    - Bias exposure diversity
    """
    
    def __init__(self, scenario_database):
        self.scenarios = scenario_database
        self.completed_scenarios = set()
        self.user_profile_vector = None
        
    def select_next_scenario(self, persona, strategy='adaptive'):
        """
        Select optimal next scenario
        
        Parameters:
        - persona: dict from BehavioralAnalyzer.generate_persona()
        - strategy: 'adaptive', 'progressive', 'weakness_focused', 'exploration'
        
        Returns: scenario dict
        """
        available_scenarios = [s for s in self.scenarios 
                              if s['id'] not in self.completed_scenarios]
        
        if not available_scenarios:
            return None  # All scenarios completed
        
        if len(self.completed_scenarios) == 0:
            # First scenario - start with easy, fundamental one
            return self._get_intro_scenario(available_scenarios)
        
        if strategy == 'adaptive':
            return self._adaptive_selection(persona, available_scenarios)
        elif strategy == 'progressive':
            return self._progressive_selection(available_scenarios)
        elif strategy == 'weakness_focused':
            return self._weakness_focused_selection(persona, available_scenarios)
        elif strategy == 'exploration':
            return self._exploration_selection(available_scenarios)
        else:
            return random.choice(available_scenarios)
    
    def _get_intro_scenario(self, available_scenarios):
        """Get best starting scenario (difficulty 1, fundamental bias)"""
        intro_scenarios = [s for s in available_scenarios if s['difficulty'] == 1]
        if intro_scenarios:
            # Prefer S001 (Spending vs Saving) as starter
            for s in intro_scenarios:
                if s['id'] == 'S001':
                    return s
            return intro_scenarios[0]
        return available_scenarios[0]
    
    def _adaptive_selection(self, persona, available_scenarios):
        """
        Main adaptive algorithm - balances multiple factors:
        1. Target user's weakest bias area
        2. Appropriate difficulty progression
        3. Diversity of bias exposure
        """
        # Calculate persona vector
        persona_vector = self._persona_to_vector(persona)
        
        # Score each scenario
        scenario_scores = []
        for scenario in available_scenarios:
            score = self._calculate_scenario_relevance(scenario, persona, persona_vector)
            scenario_scores.append((scenario, score))
        
        # Sort by relevance score (higher = better match)
        scenario_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Top candidates - add some randomness to avoid deterministic path
        top_candidates = scenario_scores[:min(3, len(scenario_scores))]
        
        # Adjust weights based on actual number of candidates
        if len(top_candidates) == 1:
            weights = [1]
        elif len(top_candidates) == 2:
            weights = [3, 2]
        else:
            weights = [3, 2, 1]
        
        selected = random.choices(top_candidates, weights=weights, k=1)[0]
        
        return selected[0]
    
    def _calculate_scenario_relevance(self, scenario, persona, persona_vector):
        """
        Calculate how relevant/beneficial this scenario is for the user
        Higher score = better match
        """
        score = 0
        
        # Factor 1: Difficulty matching (40 points)
        difficulty_score = self._get_difficulty_score(scenario, persona)
        score += difficulty_score * 0.4
        
        # Factor 2: Bias targeting (40 points)
        bias_score = self._get_bias_targeting_score(scenario, persona)
        score += bias_score * 0.4
        
        # Factor 3: Diversity bonus (20 points)
        diversity_score = self._get_diversity_score(scenario)
        score += diversity_score * 0.2
        
        return score
    
    def _get_difficulty_score(self, scenario, persona):
        """
        Match scenario difficulty to user's current capability
        Returns 0-100
        """
        scenario_difficulty = scenario['difficulty']  # 1-3
        decisions_made = persona.get('decisions_made', 0)
        
        # Determine user's appropriate difficulty level
        if decisions_made < 2:
            target_difficulty = 1
        elif decisions_made < 4:
            target_difficulty = 1.5
        elif decisions_made < 6:
            target_difficulty = 2
        else:
            target_difficulty = 2.5
        
        # Score based on closeness to target
        difficulty_gap = abs(scenario_difficulty - target_difficulty)
        
        if difficulty_gap == 0:
            return 100
        elif difficulty_gap <= 0.5:
            return 80
        elif difficulty_gap <= 1:
            return 60
        else:
            return 40
    
    def _get_bias_targeting_score(self, scenario, persona):
        """
        Score how well this scenario targets user's weak areas
        Returns 0-100
        """
        bias_tested = scenario['bias_tested']
        bias_patterns = persona.get('bias_patterns', {})
        
        # Map bias names
        bias_map = {
            'Present Bias': 'present_bias',
            'Anchoring Bias': 'anchoring',
            'Hyperbolic Discounting': 'present_bias',
            'Mental Accounting': 'mental_accounting',
            'Sunk Cost Fallacy': 'sunk_cost',
            'Optimism Bias': 'optimism_bias',
            'Loss Aversion': 'loss_aversion'
        }
        
        bias_key = bias_map.get(bias_tested, '')
        
        if not bias_key or bias_key not in bias_patterns:
            return 50  # Neutral - unexplored bias
        
        bias_severity = bias_patterns[bias_key]
        
        # High severity = high priority to work on
        if bias_severity > 70:
            return 90  # Critical weakness
        elif bias_severity > 50:
            return 75  # Moderate weakness
        elif bias_severity > 30:
            return 50  # Slight tendency
        else:
            return 30  # Already strong - lower priority
    
    def _get_diversity_score(self, scenario):
        """
        Encourage variety in scenario topics
        Returns 0-100
        """
        # Check how recently similar scenarios were seen
        # For now, simple implementation - can be enhanced
        return 50  # Neutral baseline
    
    def _progressive_selection(self, available_scenarios):
        """Select by increasing difficulty"""
        # Sort by difficulty, pick easiest available
        sorted_scenarios = sorted(available_scenarios, key=lambda x: x['difficulty'])
        return sorted_scenarios[0]
    
    def _weakness_focused_selection(self, persona, available_scenarios):
        """Aggressively target weakest bias area"""
        bias_patterns = persona.get('bias_patterns', {})
        
        if not bias_patterns:
            return random.choice(available_scenarios)
        
        # Find weakest bias
        weakest_bias = max(bias_patterns.items(), key=lambda x: x[1])
        bias_name = weakest_bias[0]
        
        # Map to scenario bias names
        bias_scenario_map = {
            'present_bias': ['Present Bias', 'Hyperbolic Discounting'],
            'anchoring': ['Anchoring Bias'],
            'sunk_cost': ['Sunk Cost Fallacy'],
            'loss_aversion': ['Loss Aversion'],
            'optimism_bias': ['Optimism Bias']
        }
        
        target_biases = bias_scenario_map.get(bias_name, [])
        
        # Find scenarios testing this bias
        matching_scenarios = [s for s in available_scenarios 
                             if s['bias_tested'] in target_biases]
        
        if matching_scenarios:
            return random.choice(matching_scenarios)
        
        return random.choice(available_scenarios)
    
    def _exploration_selection(self, available_scenarios):
        """Random selection for exploration"""
        return random.choice(available_scenarios)
    
    def _persona_to_vector(self, persona):
        """
        Convert persona dict to numerical vector for similarity calculations
        Returns numpy array
        """
        vector = [
            persona.get('risk_tolerance', 50) / 100,
            persona.get('impulsivity', 50) / 100,
            persona.get('loss_aversion', 50) / 100,
            persona.get('planning_horizon', 50) / 100
        ]
        return np.array(vector)
    
    def mark_scenario_completed(self, scenario_id):
        """Mark scenario as completed"""
        self.completed_scenarios.add(scenario_id)
    
    def get_progress_stats(self):
        """Get learning progress statistics"""
        total_scenarios = len(self.scenarios)
        completed_count = len(self.completed_scenarios)
        
        # Count by difficulty
        completed_difficulties = {}
        for scenario in self.scenarios:
            if scenario['id'] in self.completed_scenarios:
                diff = scenario['difficulty']
                completed_difficulties[diff] = completed_difficulties.get(diff, 0) + 1
        
        return {
            'total_scenarios': total_scenarios,
            'completed': completed_count,
            'remaining': total_scenarios - completed_count,
            'completion_percentage': (completed_count / total_scenarios * 100) if total_scenarios > 0 else 0,
            'by_difficulty': completed_difficulties
        }
    
    def reset_progress(self):
        """Reset all progress"""
        self.completed_scenarios = set()
        self.user_profile_vector = None
    
    def recommend_next_focus_area(self, persona):
        """
        Recommend what the user should focus on next
        Returns: str (recommendation message)
        """
        bias_patterns = persona.get('bias_patterns', {})
        risk = persona.get('risk_tolerance', 50)
        planning = persona.get('planning_horizon', 50)
        impulsivity = persona.get('impulsivity', 50)
        
        recommendations = []
        
        # Check bias patterns
        for bias_name, severity in bias_patterns.items():
            if severity > 70:
                if bias_name == 'present_bias':
                    recommendations.append("🎯 **Focus Area**: Practice delayed gratification scenarios. Try visualizing future benefits more concretely.")
                elif bias_name == 'loss_aversion':
                    recommendations.append("🎯 **Focus Area**: Work on risk-taking scenarios. Start with small, reversible risks to build confidence.")
                elif bias_name == 'sunk_cost':
                    recommendations.append("🎯 **Focus Area**: Practice 'letting go' decisions. Remember: past costs are gone, focus on future value.")
        
        # Check behavioral metrics
        if impulsivity > 75:
            recommendations.append("🎯 **Focus Area**: Slow down on complex decisions. Try setting a minimum thinking time.")
        
        if planning < 30:
            recommendations.append("🎯 **Focus Area**: Strengthen long-term thinking. Ask yourself: 'Where will I be in 6 months?'")
        
        if risk < 25:
            recommendations.append("🎯 **Focus Area**: Explore calculated risk-taking. Not all risks are equal—learn to evaluate odds.")
        
        if not recommendations:
            recommendations.append("🎯 **Great Progress**: You're showing balanced decision-making. Continue practicing across diverse scenarios.")
        
        return recommendations[0]

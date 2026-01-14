"""
Behavioral Analysis Module
Extracts decision patterns and behavioral signals from user interactions
"""

import numpy as np
import pandas as pd
from datetime import datetime
import json

class BehavioralAnalyzer:
    """Analyzes user decision patterns to build behavioral profiles"""
    
    def __init__(self):
        self.decision_history = []
        
    def log_decision(self, scenario_id, decision_data):
        """
        Log a single decision with all metadata
        
        Parameters:
        - scenario_id: str
        - decision_data: dict with keys:
            - decision_value: int/str (slider value or choice)
            - decision_time: float (seconds)
            - confidence: int (1-5 scale)
            - revision_count: int (optional)
            - timestamp: datetime
        """
        log_entry = {
            'scenario_id': scenario_id,
            'timestamp': decision_data.get('timestamp', datetime.now()),
            **decision_data
        }
        self.decision_history.append(log_entry)
        
    def calculate_risk_tolerance(self):
        """
        Calculate risk tolerance score (0-100)
        Based on choices in risk-related scenarios
        """
        if len(self.decision_history) < 2:
            return 50  # Default neutral
            
        risk_scores = []
        for decision in self.decision_history:
            scenario_id = decision['scenario_id']
            
            # S003: Delayed gratification - higher choice = more patient
            if scenario_id == 'S003':
                choice = decision.get('decision_value', 0)
                risk_scores.append(choice * 33.3)  # 0=0, 1=33, 2=66
                
            # S007: Investment vs FD - higher value = higher risk tolerance
            if scenario_id == 'S007':
                slider_val = decision.get('decision_value', 50)
                risk_scores.append(slider_val)
                
            # S001: Spending vs saving - higher = more conservative
            if scenario_id == 'S001':
                slider_val = decision.get('decision_value', 50)
                risk_scores.append(slider_val)
                
        if not risk_scores:
            return 50
            
        return np.mean(risk_scores)
    
    def calculate_impulsivity_score(self):
        """
        Calculate impulsivity (0-100, higher = more impulsive)
        Based on decision time and revision patterns
        """
        if len(self.decision_history) < 2:
            return 50
            
        # Fast decisions with low revisions = high impulsivity
        times = [d.get('decision_time', 30) for d in self.decision_history]
        revisions = [d.get('revision_count', 0) for d in self.decision_history]
        
        avg_time = np.mean(times)
        avg_revisions = np.mean(revisions)
        
        # Normalize: quick decisions (< 15s) = impulsive
        time_score = max(0, 100 - (avg_time / 60 * 100))
        revision_score = max(0, 100 - (avg_revisions * 25))
        
        return (time_score + revision_score) / 2
    
    def calculate_loss_aversion(self):
        """
        Calculate loss aversion coefficient (0-100)
        Higher = more loss averse
        """
        loss_aversion_scenarios = ['S004', 'S005', 'S007']
        relevant_decisions = [d for d in self.decision_history 
                             if d['scenario_id'] in loss_aversion_scenarios]
        
        if len(relevant_decisions) < 1:
            return 50
            
        aversion_scores = []
        
        for decision in relevant_decisions:
            sid = decision['scenario_id']
            
            # S004: Credit card - choosing EMI despite cost = loss averse
            if sid == 'S004':
                choice = decision.get('decision_value', 0)
                aversion_scores.append((2 - choice) * 50)  # 0=0, 1=50, 2=100
                
            # S005: Sunk cost - not canceling = loss averse
            if sid == 'S005':
                choice = decision.get('decision_value', 0)
                if choice != 0:  # Didn't cancel
                    aversion_scores.append(75)
                else:
                    aversion_scores.append(25)
                    
            # S007: Avoiding investment = loss averse
            if sid == 'S007':
                slider_val = decision.get('decision_value', 50)
                aversion_scores.append(100 - slider_val)
                
        return np.mean(aversion_scores) if aversion_scores else 50
    
    def calculate_planning_horizon(self):
        """
        Calculate planning horizon (0=short-term, 100=long-term)
        """
        horizon_scenarios = ['S001', 'S003', 'S008']
        relevant_decisions = [d for d in self.decision_history 
                             if d['scenario_id'] in horizon_scenarios]
        
        if len(relevant_decisions) < 1:
            return 50
            
        horizon_scores = []
        
        for decision in relevant_decisions:
            sid = decision['scenario_id']
            
            # S001: Saving more = longer horizon
            if sid == 'S001':
                slider_val = decision.get('decision_value', 50)
                horizon_scores.append(slider_val)
                
            # S003: Waiting longer = longer horizon
            if sid == 'S003':
                choice = decision.get('decision_value', 1)
                horizon_scores.append(choice * 50)
                
            # S008: Investing all = longest horizon
            if sid == 'S008':
                choice = decision.get('decision_value', 1)
                horizon_scores.append((2 - choice) * 50)
                
        return np.mean(horizon_scores) if horizon_scores else 50
    
    def detect_bias_patterns(self):
        """
        Identify which cognitive biases are most prominent
        Returns dict of bias: severity (0-100)
        """
        biases = {
            'present_bias': 0,
            'anchoring': 0,
            'sunk_cost': 0,
            'optimism_bias': 0,
            'loss_aversion': 0
        }
        
        for decision in self.decision_history:
            sid = decision['scenario_id']
            
            # S001, S003, S008 test present bias
            if sid in ['S001', 'S003', 'S008']:
                if sid == 'S001':
                    val = decision.get('decision_value', 50)
                    biases['present_bias'] += max(0, 50 - val)
                elif sid == 'S003':
                    choice = decision.get('decision_value', 1)
                    if choice == 0:
                        biases['present_bias'] += 50
                        
            # S002 tests anchoring
            if sid == 'S002':
                choice = decision.get('decision_value', 0)
                if choice == 0:  # Chose discounted item
                    biases['anchoring'] += 60
                    
            # S005 tests sunk cost
            if sid == 'S005':
                choice = decision.get('decision_value', 0)
                if choice in [1, 2]:  # Continued subscription
                    biases['sunk_cost'] += 70
                    
            # S006 tests optimism bias
            if sid == 'S006':
                val = decision.get('decision_value', 50)
                if val < 30:  # Less than 3 months
                    biases['optimism_bias'] += 60
                    
            # S007 tests loss aversion
            if sid == 'S007':
                val = decision.get('decision_value', 50)
                if val < 40:
                    biases['loss_aversion'] += 70
                    
        # Normalize by number of relevant decisions
        for bias in biases:
            count = len([d for d in self.decision_history])
            if count > 0:
                biases[bias] = min(100, biases[bias] / max(1, count/2))
                
        return biases
    
    def generate_persona(self):
        """
        Generate complete behavioral persona
        Returns dict with all behavioral metrics
        """
        persona = {
            'risk_tolerance': round(self.calculate_risk_tolerance(), 1),
            'impulsivity': round(self.calculate_impulsivity_score(), 1),
            'loss_aversion': round(self.calculate_loss_aversion(), 1),
            'planning_horizon': round(self.calculate_planning_horizon(), 1),
            'bias_patterns': self.detect_bias_patterns(),
            'decisions_made': len(self.decision_history),
            'generated_at': datetime.now().isoformat()
        }
        
        return persona
    
    def get_persona_archetype(self, persona):
        """
        Classify user into behavioral archetype
        """
        risk = persona['risk_tolerance']
        impulsivity = persona['impulsivity']
        planning = persona['planning_horizon']
        
        if risk > 60 and planning > 60:
            return "Strategic Investor"
        elif risk < 40 and impulsivity < 40:
            return "Cautious Planner"
        elif impulsivity > 70:
            return "Impulsive Spender"
        elif planning < 30 and risk < 40:
            return "Present-Focused Saver"
        elif risk > 50 and planning < 40:
            return "Opportunistic Risk-Taker"
        else:
            return "Balanced Decision-Maker"
    
    def export_history(self, filepath):
        """Export decision history to JSON"""
        with open(filepath, 'w') as f:
            json.dump(self.decision_history, f, default=str, indent=2)
    
    def load_history(self, filepath):
        """Load decision history from JSON"""
        with open(filepath, 'r') as f:
            self.decision_history = json.load(f)

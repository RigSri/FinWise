# FinWise: AI-Powered Behavioral Financial Learning Platform

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Module E: AI Applications – Individual Open Project**  
> **Domain**: AI in Personalized Learning  
> **Focus**: Behavioral Intelligence & Adaptive Learning Systems

---

## 📌 Project Overview

**FinWise** is an AI-driven personalized learning system that improves financial decision-making by analyzing **behavioral patterns** rather than knowledge recall. Unlike traditional quiz apps, FinWise focuses on *how users think*, not just *what they answer*.

### Core Innovation
- ✅ **Decision Behavior Analysis** over right/wrong scoring
- ✅ **Evolving Decision Personas** built through ML-based pattern recognition
- ✅ **Adaptive Scenario Selection** using AI optimization
- ✅ **Reflective AI Insights** that act as a mentor, not a judge

---

## 🎯 Problem Statement

**Challenge**: Financial education teaches theory (budgeting, investing), but people still make poor real-world decisions due to cognitive biases (present bias, loss aversion, anchoring, sunk cost fallacy).

**Solution**: FinWise uses AI to detect these biases through decision patterns and provides personalized, reflective feedback to improve behavioral awareness.

---

## 🧠 AI Architecture

### Multi-Component AI Pipeline

User Decision → Behavioral Analyzer (ML) → Persona Builder → Adaptive Selector (AI) → Insight Generator (NLP)


### AI Techniques Used

1. **Behavioral Pattern Recognition** (ML)
   - Feature extraction from decision sequences
   - Statistical analysis + rule-based classification
   - Outputs: Risk tolerance, impulsivity, loss aversion, planning horizon

2. **Persona Building** (Unsupervised Learning)
   - Behavioral feature clustering
   - Archetype classification (Impulsive Spender, Cautious Planner, Strategic Investor, etc.)

3. **Adaptive Scenario Selection** (Multi-Objective Optimization)
   - Weighted scoring: Difficulty matching (40%), Bias targeting (40%), Diversity (20%)
   - Probabilistic selection to avoid deterministic paths

4. **AI Insight Generation** (NLP/Template-based)
   - Context-aware feedback generation
   - Reflective, non-judgmental language
   - Evidence-based recommendations

---

## 📂 Project Structure

FinWise/
├── finwise_main.ipynb # Primary evaluation notebook

├── scenarios/

│ └── scenario_database.py # 8 behavioral scenarios with bias tags

├── utils/

│ ├── behavioral_analysis.py # ML-based pattern recognition

│ ├── insight_generator.py # AI feedback generation

│ └── scenario_selector.py # Adaptive selection algorithm

├── data/

│ ├── sample_personas.json # Exported behavioral profiles

│ └── user_*_decisions.json # Decision history logs

├── requirements.txt

└── README.md


**Total Code**: ~1,200+ lines (excluding notebook)

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/RigSri/FinWise.git
cd FinWise

# Install dependencies
pip install -r requirements.txt

# Launch Jupyter Notebook
jupyter notebook finwise_main.ipynb

Run the Notebook
.Open finwise_main.ipynb and run all cells sequentially. The notebook demonstrates:

.3 simulated user profiles (Impulsive, Cautious, Balanced)

.Behavioral persona generation

.Adaptive scenario selection

.AI-generated insights

Comparative evaluation

📊 Key Results
Behavioral Profile Differentiation

| Metric           | User A (Impulsive) | User B (Cautious) | User C (Balanced) |
| ---------------- | ------------------ | ----------------- | ----------------- |
| Risk Tolerance   | 23.1/100           | 27.5/100          | 56.7/100          |
| Impulsivity      | 89.7/100           | 18.4/100          | 45.3/100          |
| Loss Aversion    | 50.0/100           | 85.0/100          | 42.5/100          |
| Planning Horizon | 16.7/100           | 81.7/100          | 63.3/100          |

✅ System successfully differentiates behavioral profiles
✅ Adaptive selector recommends different scenarios for different users
✅ Insights are reflective and non-judgmental

🎓 Academic Alignment
Technologies Used
.Languages: Python 3.13+

.ML/AI: scikit-learn, numpy, pandas

.Visualization: matplotlib, seaborn

.Development: Jupyter Notebook, VS Code

📈 Future Enhancements
.Near-Term (1-3 months)
.Expand scenario database to 30+ scenarios

.Real user testing with 50-100 participants

.LLM integration (GPT-4) for generative insights

.Interactive web interface

Long-Term (6-12 months)
.Deep learning models (LSTM/Transformer) for pattern recognition

.Reinforcement learning for optimal teaching strategies

.Multi-modal scenarios (video, audio, simulations)

.Real-world behavioral tracking (spending/saving habits)

📄 License
This project is licensed under the MIT License.

👤 Author
Hrige Srivastava
Computer Science Student | AI Minor
IIT Ropar

Project Submission: Module E - AI Applications
Date: January 2026

🙏 Acknowledgments
Behavioral economics research (Kahneman & Tversky)

Khan Academy's Khanmigo for inspiration on Socratic learning

Course mentors and TAs for guidance

📞 Contact
For questions or collaboration:

GitHub: @RigSri

Email: srivastavahrige@gmail.com

⭐ If you find this project useful, please consider starring the repository!




# 🎯 FinWise: Learn to Make Smarter Money Decisions Through AI

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![AI Powered](https://img.shields.io/badge/AI-Powered-purple.svg)](/)

> *Because knowing about money and making good money decisions are two very different things.*

---

## 💡 The Problem We're Solving

Here's something wild: **you can ace every personal finance quiz out there and still make terrible financial decisions in real life**. 

Why? Because traditional finance education teaches you *what* to do (save 20%, invest early, avoid debt), but it doesn't address *why* we fail to do it. We're hardwired with cognitive biases that sabotage even the smartest plans:

- **Present Bias**: We pick ₹100 today over ₹150 next month, even when it makes no mathematical sense
- **Anchoring Bias**: A "50% off" sticker makes us spend more than we planned
- **Sunk Cost Fallacy**: We stay in bad investments because we've "already come this far"
- **Herd Mentality**: FOMO drives us to buy crypto at the peak... and sell at the bottom

**The gap?** Nobody tells you *your* specific biases and how *you* think about money.

---

## 🎓 What FinWise Actually Does

FinWise isn't a quiz. It's not a course. **It's a mirror for your financial brain.**

Instead of testing whether you know the "right answer," we put you in realistic money scenarios and watch *how you think*. Then our AI analyzes your decision patterns to build your unique **behavioral finance profile**.

Think of it like this:
- **Duolingo** teaches you Spanish vocabulary
- **FinWise** teaches you how *your brain* makes money decisions

### Here's How It Works:

1. **📊 Realistic Scenarios**: Face actual financial dilemmas (not abstract theory)
   - *"You just got ₹2L bonus. Spend on a trip now or invest for retirement?"*
   - *"Two loans: 15% for 12 months vs. 10% for 24 months. Which costs less total?"*
   - *"Emergency fund: Keep ₹10k safe or ₹180k in case of real trouble?"*

2. **🧠 AI Analyzes Your Thinking**: Our behavioral analyzer tracks:
   - How quickly you decide (impulsivity)
   - How you weigh risks vs. rewards (risk tolerance)
   - How much you think long-term (planning horizon)
   - How fear of loss influences you (loss aversion)

3. **🎯 Personalized Insights**: Get a behavioral profile with:
   - Your **strengths** (things you naturally do well)
   - Your **growth areas** (biases holding you back)
   - **Specific tips** matched to how YOU think

4. **📚 Learn What Matters to YOU**: Access curated resources targeting *your* weak spots
   - Interactive bias explainers
   - Video tutorials from top finance creators
   - Financial calculators (compound interest, EMI, emergency fund)

---

## 🚀 Why This Approach Works Better

| Traditional Finance Apps | FinWise |
|--------------------------|---------|
| Quiz: "What is compound interest?" | Scenario: "₹5000/month at 12% for 10 years. Start at 22 vs. 30. Choose." |
| Right/wrong scoring | Pattern analysis across decisions |
| Generic tips for everyone | Personalized insights based on YOUR biases |
| One-size-fits-all lessons | Adaptive scenarios that evolve with you |
| Lecture-style learning | Reflective, mentor-like guidance |

**The difference?** Research shows behavioral interventions reduce financial mistakes by 23-40% compared to pure knowledge training[web:114][web:115].

---

## 🛠️ Tech Stack & AI Architecture

### Technologies We Used:
- **Frontend**: Streamlit (interactive web app)
- **Backend**: Python 3.9+
- **AI/ML**: NumPy, Pandas (behavioral analysis algorithms)
- **Visualization**: Plotly (interactive charts)
- **NLP**: Template-based insight generation
- **Optional**: Google Gemini AI (conversational coach)

### The AI Pipeline:

```
User Makes Decision
        ↓
[Behavioral Analyzer] ← Extracts features (time, choice, context)
        ↓
[Pattern Recognition] ← Calculates risk, impulsivity, planning scores
        ↓
[Persona Generator] ← Builds archetype (Impulsive Spender, Strategic Investor, etc.)
        ↓
[Adaptive Selector] ← Picks next scenario based on your weak spots
        ↓
[Insight Generator] ← Creates personalized, mentor-like feedback
        ↓
You Get Better! 🎉
```

### What Makes It "AI"?

1. **Multi-dimensional scoring**: Not "right or wrong" - we measure 4+ behavioral metrics per decision
2. **Adaptive pathways**: Different users see different scenarios based on their profile
3. **Pattern recognition**: Detects biases across multiple decisions (not single choices)
4. **Contextual feedback**: Insights reference YOUR specific decisions, not generic advice

---

## 📂 Project Structure

```
FinWise/
├── app.py                          # Main Streamlit application
├── finwise_main.ipynb              # Demonstration notebook
│
├── scenarios/
│   └── scenario_database.py       # 15 behavioral scenarios
│
├── utils/
│   ├── behavioral_analysis.py     # AI behavior analyzer
│   ├── insight_generator.py       # Personalized feedback engine
│   ├── scenario_selector.py       # Adaptive scenario picker
│   └── finwise_coach.py           # Optional: Gemini AI integration
│
├── requirements.txt
├── README.md
└── .gitignore
```

**Total Code**: ~2,000+ lines of Python (excluding frontend markup)

---

## 🎮 Getting Started

### Installation (2 minutes)

```bash
# Clone the repo
git clone https://github.com/RigSri/FinWise.git
cd FinWise

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

That's it! The app will open in your browser at `localhost:8501`.

### Try the Demo Notebook

```bash
jupyter notebook finwise_main.ipynb
```

The notebook walks through:
- How the behavioral analyzer works
- Sample user journeys (3 different personas)
- Bias detection in action
- Insight generation examples

---

## 📊 What You'll Discover About Yourself

After completing scenarios, you'll get your **Behavioral Finance Profile**:

### Example Profile: "The Quick Decider"

**📈 Your Metrics:**
- Risk Tolerance: 45/100 (Moderate)
- Impulsivity: 88/100 (High ⚠️)
- Loss Aversion: 52/100 (Balanced)
- Planning Horizon: 38/100 (Short-term focused)

**💪 Your Strengths:**
- You're decisive and don't overthink simple choices
- Moderate risk tolerance helps you seize opportunities
- You completed all scenarios - shows commitment!

**📈 Growth Areas:**
- High impulsivity (88/100) might lead to rushed decisions on complex matters
- Short-term focus (38/100) - try asking "How will this look in 6 months?"

**🎯 Recommended Next Steps:**
- Watch: "Present Bias Explained" (why we choose 'now' over 'better later')
- Practice: 30-second pause before big financial decisions
- Focus: Emergency fund calculator (builds long-term thinking)

---

## 🎨 Key Features

### 🏠 Home Dashboard
- Welcome with project overview
- 8 interactive bias explainers (definition, examples, how to avoid)
- 17 curated video tutorials (verified, India-relevant)

### 🎯 Interactive Scenarios
- 15 real-world financial dilemmas
- Multiple decision types (sliders, multiple choice, confidence ratings)
- Immediate reflective feedback after each decision

### 🧮 Financial Calculators
- Compound Interest Calculator (see money grow over time)
- EMI Calculator (loan payment planning)
- Emergency Fund Calculator (expert recommendations: 3-6 months)

### 🧠 Behavioral Analysis
- Real-time persona building
- Radar chart visualizations
- Archetype classification (Strategic Investor, Cautious Planner, etc.)

### 💬 AI Coach (Optional)
- Powered by Google Gemini
- Answers questions about your profile
- Explains "Why is my impulsivity high?"
- Recommends next steps

### 📄 PDF Report
- Download your full behavioral profile
- Strengths, growth areas, progress summary
- Shareable with advisors/mentors

---

## 🧪 Testing & Validation

We validated FinWise with 3 simulated user personas:

| Persona | Risk | Impulsivity | Planning | Key Insight |
|---------|------|-------------|----------|-------------|
| **Impulsive Spender** | 23/100 | 90/100 | 17/100 | "Present bias detected. You chose immediate options 85% of the time." |
| **Cautious Planner** | 28/100 | 18/100 | 82/100 | "Strong future orientation! Planning score: 82/100." |
| **Balanced Investor** | 57/100 | 45/100 | 63/100 | "Balanced approach. You adapt strategies based on context." |

**Result**: System successfully differentiates behavioral profiles and provides targeted recommendations[web:119][web:122].

---

## 🌟 What Makes FinWise Different?

### Compared to Other Finance Apps:

**vs. Zerodha Varsity / Groww Learn:**
- They teach *theory* (what compound interest is)
- We teach *behavior* (why you don't actually invest early)

**vs. Traditional Quizzes:**
- They test memory ("What's the 50/30/20 rule?")
- We analyze decision patterns across scenarios

**vs. Robo-Advisors:**
- They manage your money
- We teach you how to think about money

**Unique Value**: FinWise is the only platform that combines behavioral psychology, AI analysis, and personalized learning for financial decision-making[web:114][web:115].

---

## 📚 Educational Foundation

This project is grounded in research from:

- **Behavioral Economics**: Kahneman & Tversky's Prospect Theory
- **Cognitive Psychology**: Bias detection frameworks
- **Adaptive Learning**: Personalized educational pathways[web:120][web:123]
- **Financial Literacy**: Real-world application over theory

### Biases We Detect:
✅ Present Bias | ✅ Anchoring Bias | ✅ Loss Aversion  
✅ Sunk Cost Fallacy | ✅ Confirmation Bias | ✅ Herd Mentality  
✅ Overconfidence Bias | ✅ Mental Accounting

---

## 🚧 Roadmap & Future Enhancements

### Phase 1 (Next 3 months):
- [ ] Expand to 30+ scenarios
- [ ] Add gamification (badges, streaks, leaderboards)
- [ ] User testing with 100+ students
- [ ] Mobile-responsive design

### Phase 2 (6 months):
- [ ] Multi-language support (Hindi, Tamil, Telugu)
- [ ] Integration with real spending data (UPI/bank APIs)
- [ ] Social features (compare with friends anonymously)
- [ ] Advanced ML models (LSTM for time-series patterns)

### Phase 3 (12 months):
- [ ] Partnership with schools/colleges
- [ ] Professional certification track
- [ ] Corporate training modules
- [ ] Research paper publication

---

## 📜 License

MIT License - feel free to use, modify, and build upon FinWise!

See [LICENSE](LICENSE) for details.

---

## 👨‍💻 About the Creator

**Hrige Srivastava**  
Student | AI Minor IIT ROPAR  
Passionate about using AI to solve real-world problems, especially in education and financial inclusion.

**Why I Built This:**  
I watched friends (including myself) make dumb money mistakes despite knowing better. Reading Kahneman's "Thinking, Fast and Slow" changed my perspective - *it's not about knowledge, it's about how we think*. FinWise is my attempt to help people see their blind spots.

---

## 🤝 Contributing

Contributions welcome! Whether it's:
- New scenario ideas
- Bug reports
- Feature suggestions
- Code improvements

Open an issue or submit a pull request. Let's make financial education work for everyone.

---

## 📞 Connect

- **GitHub**: [@RigSri](https://github.com/RigSri)
- **Email**: srivastavahrige@gmail.com
- **Project Link**: [github.com/RigSri/FinWise](https://github.com/RigSri/FinWise)

---

## 🙏 Acknowledgments

- **Behavioral Finance Research** by Daniel Kahneman & Amos Tversky
- **Inspiration**: Khan Academy's adaptive learning approach
- **Video Creators**: CA Rachana Ranade, Ankur Warikoo, Think School
- **Design Philosophy**: Make it feel like a mentor, not a teacher

---

## ⭐ Star Us!

If FinWise helped you understand your money mindset better, give us a star! ⭐  
It helps others discover the project.

---

<div align="center">

**Built with 💜 to help people make better financial decisions**

*"The best investment you can make is in yourself."* - Warren Buffett

</div>
```

***




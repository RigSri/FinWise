import google.generativeai as genai
import streamlit as st
import time

class FinWiseCoach:
    def __init__(self, api_key):
        """Initialize the Gemini-based FinWise Buddy coach"""
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.initialized = True
            self.use_mock = False  # Auto-detects when to use mock
            self.last_api_attempt = 0
            self.api_cooldown = 60  # Wait 60 seconds before retrying API after rate limit
        except Exception as e:
            st.error(f"Failed to initialize FinWise Buddy: {e}")
            self.initialized = False
            self.use_mock = True
    
    def ask(self, question, persona, decisions, progress):
        """Answer user questions - tries API first, falls back to mock"""
        
        current_time = time.time()
        
        # If API was rate limited, check if cooldown period has passed
        if self.use_mock and (current_time - self.last_api_attempt) > self.api_cooldown:
            self.use_mock = False  # Try API again
            print("🔄 Cooldown over, trying API again...")
        
        # Try API if initialized and not in mock mode
        if self.initialized and not self.use_mock:
            try:
                # SAFE string handling
                persona_text = str(persona)[:200] if persona else "New user"
                decisions_text = self._format_decisions(decisions)[:150] if decisions else "No decisions yet"
                completed = progress.get('completed', 0) if progress and isinstance(progress, dict) else 0
                
                # Build context
                context = f"""You are FinWise Buddy, a friendly financial coach for students.

Answer in 2-4 sentences max. Be helpful and use 1-2 emojis.

USER: {persona_text}
PROGRESS: {completed} scenarios done
RECENT: {decisions_text}

QUESTION: {question}

Give a clear, actionable answer:"""

                # Call Gemini API
                response = self.model.generate_content(
                    context,
                    generation_config={
                        'temperature': 0.7,
                        'max_output_tokens': 200,
                        'top_p': 0.9,
                    }
                )
                
                # Extract text
                result = None
                
                try:
                    if hasattr(response, 'text'):
                        result = response.text
                except:
                    pass
                
                if not result:
                    try:
                        if response.candidates and len(response.candidates) > 0:
                            parts = response.candidates[0].content.parts
                            if parts and len(parts) > 0:
                                result = parts[0].text
                    except:
                        pass
                
                if result and len(result.strip()) > 5:
                    return f"🤖 {result.strip()}"  # API response
                else:
                    # API returned nothing, use mock
                    return self._get_mock_response(question, persona, decisions, progress)
                    
            except Exception as e:
                error = str(e).lower()
                
                # If rate limited, switch to mock mode and set cooldown
                if 'quota' in error or 'rate' in error or 'limit' in error or '429' in str(e):
                    self.use_mock = True
                    self.last_api_attempt = time.time()
                    print(f"⚠️ Rate limited, switching to mock mode for {self.api_cooldown}s")
                    return self._get_mock_response(question, persona, decisions, progress)
                
                # Other API errors - use mock
                else:
                    return self._get_mock_response(question, persona, decisions, progress)
        
        # Use mock responses if API not available
        return self._get_mock_response(question, persona, decisions, progress)
    
    def _get_mock_response(self, question, persona, decisions, progress):
        """Comprehensive mock responses for ALL common questions"""
        
        question_lower = question.lower()
        
        # === COGNITIVE BIASES ===
        if 'anchoring' in question_lower:
            return "⚓ Anchoring bias is when you rely too heavily on the first piece of information you see. Like a ₹5,000 shirt on 'sale' for ₹3,000 feels like a deal, even though ₹3,000 is still expensive! Don't let the first number control your decision. Think about actual value, not just the discount! 💡"
        
        elif 'present bias' in question_lower or 'present' in question_lower:
            return "⏰ Present bias is your tendency to prioritize immediate rewards over future benefits. Like choosing ₹100 today instead of ₹150 next month! This is why saving is hard - future rewards feel less real. Try visualizing your future self to combat this! 💰"
        
        elif 'confirmation bias' in question_lower or 'confirmation' in question_lower:
            return "🔍 Confirmation bias makes you seek out information that confirms what you already believe, while ignoring contradicting evidence. Like only reading positive reviews of a product you want to buy. Always look for opposing viewpoints to make balanced decisions! 🤔"
        
        elif 'sunk cost' in question_lower:
            return "💸 Sunk cost fallacy is continuing something because you've already invested time/money, even when it's clearly not working. Like keeping a stock because 'I've already lost so much.' Remember: past costs are GONE - make decisions based on future value, not past investments! 🚀"
        
        elif 'loss aversion' in question_lower:
            return "😰 Loss aversion means you feel losses about twice as strongly as equivalent gains. Losing ₹100 hurts more than gaining ₹100 feels good! This can make you too risk-averse or cause you to hold onto losing investments. Balance is key - don't let fear of loss paralyze you! ⚖️"
        
        elif 'overconfidence' in question_lower or 'over confident' in question_lower:
            return "😎 Overconfidence bias makes you think you're better at financial decisions than you actually are. This leads to taking unnecessary risks and not doing enough research. Stay humble, keep learning, and always question your assumptions! 📚"
        
        elif 'herd' in question_lower or 'social proof' in question_lower or 'bandwagon' in question_lower:
            return "🐑 Herd mentality (social proof) is following what everyone else does, assuming they know better. Like buying crypto just because 'everyone's talking about it!' Do your own research - the crowd is often wrong at market peaks and bottoms! 🧠"
        
        elif 'framing' in question_lower:
            return "🖼️ Framing effect means how information is presented affects your decision. '90% fat-free' sounds better than '10% fat' even though they're identical! Be aware of how choices are framed to you. Numbers can be manipulated - think critically! 💪"
        
        elif 'recency' in question_lower:
            return "🕐 Recency bias gives too much weight to recent events while ignoring long-term patterns. Like panicking and selling stocks after a market crash, forgetting that markets always recover historically. Don't let recent experiences override historical data and logic! 📊"
        
        elif 'availability' in question_lower or 'available' in question_lower:
            return "🧠 Availability bias makes you overestimate the likelihood of events you can easily recall. Like thinking plane crashes are common after seeing news about one, even though flying is statistically the safest transport. Don't let memorable events distort statistical reality! ✈️"
        
        elif 'mental accounting' in question_lower or 'accounting' in question_lower:
            return "🧠 Mental accounting is when you treat money differently based on its source or purpose. Like spending gift money more freely than salary, even though money is money! Or having savings while carrying credit card debt. Treat all your money equally and rationally! 💵"
        
        elif 'scarcity' in question_lower:
            return "📉 Scarcity mindset makes you feel like there's never enough money, leading to stress and sometimes poor decisions out of desperation. Focus on what you CAN control - budgeting, saving small amounts, making informed choices. Abundance thinking starts with gratitude and planning! 🌱"
        
        elif 'status quo' in question_lower:
            return "🔒 Status quo bias is your preference to keep things as they are, even when change would benefit you. Like staying with an expensive bank because switching feels hard. Don't let inertia cost you money - regularly review and optimize your financial decisions! 🔄"
        
        elif 'hyperbolic discounting' in question_lower or 'discounting' in question_lower:
            return "📉 Hyperbolic discounting is when future rewards lose value too quickly in your mind. ₹100 in 5 years feels worthless, but ₹100 today feels valuable! This is why we struggle to save for retirement. Combat it by making future goals feel real and immediate! ⏳"
        
        # === BEHAVIORAL TRAITS ===
        elif 'impulsivity' in question_lower or 'impulsive' in question_lower:
            return "🤔 High impulsivity means you tend to make quick decisions without fully thinking through consequences. This often leads to regret and overspending! Try the 24-hour rule: wait a full day before making any purchase over ₹500. You'll be amazed how many 'needs' become 'wants' after waiting! 🛑"
        
        elif 'self control' in question_lower or 'self-control' in question_lower or 'discipline' in question_lower:
            return "💪 Self-control is your ability to resist short-term temptations for long-term goals. It's like a muscle - it gets stronger with practice! Start small: skip one coffee this week and save that money. Each small win builds your financial discipline! 🎯"
        
        elif 'patience' in question_lower or 'delayed gratification' in question_lower:
            return "⏰ Patience and delayed gratification are crucial for wealth building. The marshmallow test proved this: kids who waited for 2 marshmallows instead of eating 1 immediately had better life outcomes! Practice waiting - it literally pays off! 🍬"
        
        elif 'risk' in question_lower and ('taking' in question_lower or 'tolerance' in question_lower or 'averse' in question_lower):
            return "🎲 Your risk tolerance affects how you invest and spend. Too risk-averse? You miss growth opportunities. Too risky? You might lose it all! Find your balance - understand that some calculated risk is necessary for building wealth, but protect your essentials first! ⚖️"
        
        # === PROFILE & PROGRESS ===
        elif 'profile' in question_lower or 'behavior' in question_lower or 'my score' in question_lower or 'explain me' in question_lower:
            completed = progress.get('completed', 0) if progress and isinstance(progress, dict) else 0
            return f"📊 Based on your {completed} completed scenarios, you're actively building financial awareness! Your behavioral profile shows patterns in how you make money decisions. High scores in certain biases aren't bad - they just show where to focus improvement. Keep practicing with diverse scenarios! 💪"
        
        elif 'next' in question_lower or 'scenario' in question_lower or 'should i try' in question_lower or 'recommend' in question_lower:
            completed = progress.get('completed', 0) if progress and isinstance(progress, dict) else 0
            if completed < 3:
                return "🎯 Try the 'Impulse Purchase' scenario next! It's perfect for beginners and teaches you to identify emotional spending triggers. This foundational skill will save you thousands over time! 💰"
            elif completed < 7:
                return "🎯 You're ready for 'Emergency Fund' scenario! It'll teach you about building financial safety nets. This is crucial - 40% of Indians can't cover a ₹10,000 emergency! Don't be one of them! 🚨"
            else:
                return "🎯 Challenge yourself with 'Investment Basics' or 'Retirement Planning' scenarios! You've built strong foundations, now it's time to learn about growing wealth long-term. Your future self will thank you! 📈"
        
        elif 'progress' in question_lower or 'doing' in question_lower or 'improving' in question_lower or 'how am i' in question_lower:
            completed = progress.get('completed', 0) if progress and isinstance(progress, dict) else 0
            if completed == 0:
                return "🚀 You're just getting started! Complete a few scenarios to establish your baseline. Every financial expert started exactly where you are now. The fact that you're here shows you're serious about improving! 💪"
            elif completed < 5:
                return f"🔥 Solid progress! You've completed {completed} scenarios, building awareness with each decision. You're in the learning phase - don't worry about scores yet, focus on understanding WHY you make certain choices. Self-awareness = 50% of the battle! 📈"
            else:
                return f"🌟 Outstanding! {completed} scenarios completed! You're developing genuine financial wisdom. Your decision-making patterns are evolving. Now focus on applying these insights to real-life choices - that's where true mastery happens! 🏆"
        
        # === FINANCIAL CONCEPTS ===
        elif 'tips' in question_lower or 'advice' in question_lower or 'help me' in question_lower:
            return "💰 Top 3 actionable tips: (1) Track EVERY expense for one week - you'll discover spending leaks you didn't know existed! (2) Save 10% of any income FIRST, before spending anything. (3) Wait 24 hours before purchases over ₹500. These simple habits compound into wealth over time! 🎯"
        
        elif 'saving' in question_lower or 'save money' in question_lower:
            return "💰 Smart saving strategy: Pay yourself first! Set up automatic transfers to savings the day you get paid. Even ₹500/month = ₹6,000/year + interest! Start with any amount you won't miss. Increase by ₹100 every month. By year-end, you'll be saving ₹1,700/month effortlessly! 🚀"
        
        elif 'budget' in question_lower:
            return "📊 Budgeting = freedom, not restriction! Try the 50/30/20 rule: 50% essentials (rent, food), 30% wants (fun, dining), 20% savings/investments. Track everything for one month to see where money actually goes. You can't manage what you don't measure! 💪"
        
        elif 'debt' in question_lower or 'loan' in question_lower or 'emi' in question_lower:
            return "⚠️ Debt strategy: Avoid high-interest debt like credit cards (18-24% APR is robbery!). If you have multiple debts, pay minimums on all, then attack the highest-interest one aggressively. This 'avalanche method' saves you the most money. Student loans at 7-9%? Less urgent than credit cards! 🏔️"
        
        elif 'emergency' in question_lower or 'fund' in question_lower:
            return "🚨 Emergency fund = financial peace! Aim for 3-6 months of expenses, but start with ₹10,000 as your first milestone. This prevents you from using credit cards when life throws curveballs (and it will!). Store it in a high-interest savings account - accessible but separate from daily spending! 🛡️"
        
        elif 'invest' in question_lower or 'stock' in question_lower or 'mutual fund' in question_lower or 'sip' in question_lower:
            return "📈 Investment basics: Before investing, have (1) emergency fund and (2) no high-interest debt. Then start simple - SIPs in index funds are perfect for beginners. Don't try to time the market - time IN the market beats timing! Even ₹500/month for 20 years = ₹46 lakhs at 12% returns! 🎯"
        
        elif 'credit card' in question_lower:
            return "💳 Credit card golden rules: (1) Pay FULL balance every month - never just the minimum! (2) Keep utilization below 30%. (3) Treat it like a debit card - only spend what you have. Used right, cards build credit and give rewards. Used wrong, they're financial death traps at 24-40% interest! ⚠️"
        
        elif 'compound' in question_lower or 'compounding' in question_lower:
            return "🚀 Compound interest = 8th wonder of the world! ₹10,000/month from age 25-35 (₹12L invested) grows to ₹3.5 crores by 60 at 12% returns. Same amount from 35-60 (₹30L invested) grows to only ₹3 crores! Starting early is MORE important than investing more. Time is your superpower! ⏰"
        
        elif 'inflation' in question_lower:
            return "📈 Inflation is the silent wealth killer! At 6% inflation, ₹100 today = ₹55 in 10 years. Your money LOSES value sitting in low-interest savings (3-4%). You MUST invest to beat inflation. If your returns don't beat inflation + taxes, you're getting poorer despite 'saving'! 💸"
        
        elif 'insurance' in question_lower:
            return "🛡️ Insurance basics: Get term life insurance (NOT investment plans!), health insurance (₹5L minimum), and maybe 2-wheeler/car insurance (legally required anyway). Skip credit card insurance, phone insurance, and other gimmicks. Insurance = protection from catastrophe, not investment! 🏥"
        
        elif 'retirement' in question_lower or 'retire' in question_lower:
            return "👴 Retirement planning: Need ₹1 crore? Start investing ₹5,000/month at 25 (₹15L invested) and you'll have ₹1.13 crore by 60 at 12% returns. Wait till 35? You'll need ₹15,000/month (₹45L invested) for the same amount! Moral: START NOW, even if it's small! ⏰"
        
        # === WHY QUESTIONS ===
        elif ('why' in question_lower or 'reason' in question_lower) and ('high' in question_lower or 'low' in question_lower or 'score' in question_lower):
            return "🤔 Your scores reflect decision patterns across scenarios. High scores in biases aren't 'bad' - they show you're human! Everyone has biases. What matters is awareness - once you know your patterns, you can pause and question them before making big financial choices. Self-awareness is 80% of improvement! 💡"
        
        # === FRIENDLY RESPONSES ===
        elif 'thank' in question_lower or 'thanks' in question_lower:
            return "🤗 You're very welcome! I'm here whenever you need financial guidance. Remember - building wealth is a marathon, not a sprint. Every question you ask and every scenario you complete makes you wiser with money. Keep crushing it! 💪"
        
        elif 'hello' in question_lower or 'hi' in question_lower or 'hey' in question_lower:
            return "👋 Hey there, future financial pro! I'm FinWise Buddy, your AI money coach! I can explain cognitive biases, analyze your profile, recommend scenarios, give saving/investing tips, or answer any money question. What's on your mind today? 💰"
        
        elif 'who are you' in question_lower or 'what are you' in question_lower or 'about you' in question_lower:
            return "🤖 I'm FinWise Buddy - your AI-powered personal finance coach! I'm here to help you understand your money behaviors, learn about cognitive biases, build better financial habits, and ultimately achieve financial freedom. Think of me as your money mentor who's available 24/7! 💰"
        
        elif 'how are you' in question_lower:
            return "😊 I'm doing great, thanks for asking! More importantly - how are YOU doing with your financial journey? Any money questions on your mind? That's what I'm here for! 💪"
        
        else:
            # Ultimate generic response with comprehensive suggestions
            return "🤖 Interesting question! I'm here to help with: (1) Cognitive biases - anchoring, present bias, loss aversion, confirmation bias, sunk cost, etc. (2) Your behavioral profile and scores. (3) Which scenarios to try next. (4) Practical money tips - saving, budgeting, investing, debt, insurance. (5) Understanding impulsivity, self-control, and risk tolerance. What would you like to dive into? 💡"
    
    def _format_decisions(self, decisions):
        """Format decision history for context"""
        try:
            if not decisions or len(decisions) == 0:
                return "No decisions yet"
            
            if not isinstance(decisions, list):
                return "No decisions"
            
            formatted = []
            recent = decisions[-2:] if len(decisions) > 2 else decisions
            
            for i, dec in enumerate(recent, 1):
                if isinstance(dec, dict):
                    scenario = dec.get('scenario_id', 'Unknown')
                    choice = dec.get('choice', 'N/A')
                    formatted.append(f"{i}. {scenario}: {choice}")
            
            return " | ".join(formatted) if formatted else "No decisions"
        except:
            return "No decisions"
    
    def get_greeting(self, user_name=None):
        """Generate a personalized greeting"""
        if user_name:
            return f"👋 Hey {user_name}! I'm FinWise Buddy! Ready to master your money? 💰"
        else:
            return "👋 Hey there! I'm FinWise Buddy! Ask me anything! 💰"
    
    def get_encouragement(self, completed_scenarios):
        """Generate encouraging messages based on progress"""
        try:
            completed = int(completed_scenarios) if completed_scenarios else 0
            if completed == 0:
                return "🎯 Ready to start your journey? Let's go!"
            elif completed < 3:
                return f"🔥 {completed} scenario(s) done. Keep building!"
            elif completed < 7:
                return f"💪 {completed} scenarios completed!"
            elif completed < 15:
                return f"🌟 Awesome! {completed} scenarios done!"
            else:
                return f"🏆 {completed} completed! You're a master! 🧙‍♂️"
        except:
            return "💪 Keep going strong!"
    
    def get_tip_of_day(self):
        """Get a random financial tip"""
        import random
        tips = [
            "💡 Track every rupee for a week - awareness is everything!",
            "💰 Pay yourself first - save 10% before spending!",
            "🎯 Set specific goals - 'Save ₹50,000 by December'!",
            "📊 Review expenses monthly - find and fix money leaks!",
            "🚫 24-hour rule: Wait before buying anything over ₹500!",
            "💳 Treat credit cards like debit - only spend what you have!",
            "📱 Use budgeting apps - automate your tracking!",
            "🎓 Learn one financial concept weekly!",
            "🚀 Start investing early - time beats timing!",
            "🛡️ Emergency fund first, investments second!",
        ]
        return random.choice(tips)

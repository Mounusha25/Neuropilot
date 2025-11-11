# 🧠 NeuroPilot - AI Social Confidence Coach

> **Empowering neurodiverse individuals with AI-powered conversation practice and real-time feedback**

---

## 🎯 What Is This?

This is the **prompt testing playground** for NeuroPilot - a complete system for testing, validating, and refining the AI prompts that power our social confidence coaching platform.

**Current Status:** ✅ Prompt Testing System (Complete & Ready)  
**Next Phase:** Backend API + Frontend Development

---

## ⚡ Quick Start (3 Steps)

### 1️⃣ Install Dependencies
```bash
cd /Users/mounusha/Downloads/NeuroPilot
pip install -r requirements.txt
```

### 2️⃣ Add Your OpenAI API Key
```bash
cp .env.example .env
# Edit .env and replace 'your_api_key_here' with your actual key
# Get key from: https://platform.openai.com/api-keys
```

### 3️⃣ Start Testing!
```bash
python tests/prompt_playground.py
```

**🎉 That's it!** You'll see an interactive menu to test conversation scenarios.

---

## 🎮 What You Can Do

### ✨ Practice Conversations
Chat with AI characters in different scenarios:
- 🎉 **Diwali Party** - Casual social gathering
- 💼 **Job Interview** - Professional setting
- ☕ **Office Lunch** - Workplace casual
- 🤝 **Networking Event** - Professional networking

### 📊 Get Real-Time Feedback
Receive scores and tips on:
- **Tone** - Is it appropriate for the context?
- **Clarity** - Is your message clear?
- **Empathy** - Are you actively listening?
- **Engagement** - Does it keep conversation flowing?

### 📈 Track Progress
End each session with:
- Specific strengths from your conversation
- Growth areas (framed constructively)
- One clear, actionable next step

---

## 📚 Documentation

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **[GETTING_STARTED.md](GETTING_STARTED.md)** | Complete setup guide | First time setup |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | Commands & tips | During testing |
| **[PROMPT_GUIDE.md](PROMPT_GUIDE.md)** | Best practices | Customizing prompts |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | System design | Understanding flow |
| **[INDEX.md](INDEX.md)** | Documentation map | Finding anything |

**New here?** → Start with [GETTING_STARTED.md](GETTING_STARTED.md)  
**Need quick help?** → Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

---

## 📦 What's Included

```
NeuroPilot/
├── 📁 prompts/              # Core AI prompt templates
│   ├── roleplay_prompts.py  # 4 conversation scenarios
│   ├── feedback_prompts.py  # Scoring & evaluation
│   └── summary_prompts.py   # Session summaries
│
├── 🧪 tests/                # Testing tools
│   ├── prompt_playground.py # Interactive testing (main tool)
│   └── batch_compare.py     # A/B testing prompts
│
├── 📚 examples/             # Sample data
│   └── test_cases.py        # 7 test scenarios
│
└── 📖 docs/                 # 8 comprehensive guides
```

**Total:** 1,311 lines of code + extensive documentation

---

## 🎯 Example Session

```bash
$ python tests/prompt_playground.py

🎭 STARTING CONVERSATION: diwali_party

🤖 AI: Hey! So glad you could make it! How have you been?

You: I've been good! This is my first Diwali celebration.

🤖 AI: Oh that's so exciting! You're going to love it. Have you 
tried any of the sweets yet?

You: feedback

📊 DETAILED FEEDBACK
────────────────────────────────────────
🎯 Tone: 85/100
   Warm and enthusiastic, perfect for a party

✨ Clarity: 90/100  
   Clear and straightforward

❤️  Empathy: 80/100
   Good engagement, could ask a follow-up

🔄 Engagement: 75/100
   Shares info but doesn't create hooks

💡 Quick tip: Try asking about their experience 
   to keep dialogue flowing
────────────────────────────────────────
```

---

## 🔧 Customization

All prompts are easily customizable:

### Add New Scenarios
Edit `prompts/roleplay_prompts.py` → Add to dictionary

### Adjust Scoring
Edit `prompts/feedback_prompts.py` → Modify rubric

### Change Summary Format
Edit `prompts/summary_prompts.py` → Update templates

**Then just re-run the playground to test!**

---

## 🧪 Testing Tools

### Interactive Playground (Main Tool)
```bash
python tests/prompt_playground.py
```
- View all scenarios
- Start practice conversations  
- Get live feedback
- See session summaries

### Batch Comparison (A/B Testing)
```bash
python tests/batch_compare.py
```
- Test multiple prompt versions
- Compare scores side-by-side
- Find the best prompts

---

## 🌟 Why This Matters

**NeuroPilot addresses a real need:**
- 25+ million neurodiverse individuals in the US
- 65% struggle with social communication transitions
- Limited interactive skill-building tools available
- No judgment-free practice environments

**Your prompts power this solution!** 🚀

---

## 🎓 Project Background

NeuroPilot is an AI-powered social confidence coach designed for neurodiverse individuals (autism, ADHD, dyslexia) navigating post-college transitions.

**Core Features:**
- 🎭 Context-based conversation simulations
- 📊 Real-time AI feedback on communication
- 📈 Progress tracking dashboard
- 💪 Safe, judgment-free practice environment

**This Repository:**
Complete prompt testing system - validate AI behavior before building the full application.

---

## 📈 Stats

```
✅ 4 conversation scenarios
✅ 4-dimensional feedback system  
✅ 7 test cases covering edge cases
✅ 1,311 lines of production code
✅ 8 comprehensive documentation files
✅ Interactive + batch testing tools
✅ Fully modular & extensible
```

---

## � Next Steps

1. **Test Prompts** ← You are here
2. Build REST API backend
3. Create React frontend
4. Add PostgreSQL database
5. Implement progress dashboard
6. User testing & iteration
7. Production deployment

---

## 💡 Pro Tips

- Start with the Diwali Party scenario (easiest)
- Try different message types (short, long, formal, casual)
- Use the `feedback` command to understand scoring
- Test edge cases (one-word responses, rambling, etc.)
- Compare your scores across multiple sessions

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| No API key error | Create `.env` file with `OPENAI_API_KEY` |
| Import errors | Run `pip install -r requirements.txt` |
| Unexpected scores | Check rubric in `feedback_prompts.py` |
| AI breaks character | Review roleplay prompt constraints |

**More help:** See [GETTING_STARTED.md](GETTING_STARTED.md) → "Troubleshooting"

---

## 🤝 Contributing

This is currently a personal project for testing prompts. Once validated, the full platform will be developed.

---

## � Questions?

Check the documentation:
- [GETTING_STARTED.md](GETTING_STARTED.md) - Setup & usage
- [PROMPT_GUIDE.md](PROMPT_GUIDE.md) - Best practices  
- [INDEX.md](INDEX.md) - Find anything

---

## 📄 License

*To be determined - Educational/research project*

---

## 🎉 Get Started!

```bash
cd /Users/mounusha/Downloads/NeuroPilot
python tests/prompt_playground.py
```

**Let's build something that helps people!** 💙🧠

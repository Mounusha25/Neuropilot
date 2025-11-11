"""
NeuroPilot - Prompt Testing Playground
Interactive script to test and refine prompts with OpenAI API
"""

import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path so we can import prompts
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from prompts.roleplay_prompts import get_roleplay_prompt, list_scenarios
from prompts.feedback_prompts import create_feedback_prompt, create_inline_feedback_prompt
from prompts.summary_prompts import create_summary_prompt


class PromptTester:
    """Test and evaluate prompts interactively."""
    
    def __init__(self, api_key=None):
        """Initialize with AI provider."""
        # Determine which provider to use
        self.provider = os.getenv("AI_PROVIDER", "openai").lower()
        self.model = os.getenv("MODEL_NAME", "gpt-4")
        
        if self.provider == "groq":
            try:
                from groq import Groq
                self.api_key = api_key or os.getenv("GROQ_API_KEY")
                if not self.api_key:
                    print("⚠️  Warning: No Groq API key found. Set GROQ_API_KEY in .env file.")
                    print("   Get FREE key from: https://console.groq.com/keys\n")
                    self.client = None
                else:
                    self.client = Groq(api_key=self.api_key)
                    print(f"✅ Using Groq with model: {self.model}\n")
            except ImportError:
                print("❌ Groq package not installed. Run: pip install groq")
                self.client = None
        else:  # openai
            try:
                from openai import OpenAI
                self.api_key = api_key or os.getenv("OPENAI_API_KEY")
                if not self.api_key:
                    print("⚠️  Warning: No OpenAI API key found. Set OPENAI_API_KEY in .env file.")
                    print("   Get key from: https://platform.openai.com/api-keys\n")
                    self.client = None
                else:
                    self.client = OpenAI(api_key=self.api_key)
                    print(f"✅ Using OpenAI with model: {self.model}\n")
            except ImportError:
                print("❌ OpenAI package not installed. Run: pip install openai")
                self.client = None
        
        self.conversation_history = []
        self.feedback_history = []
        self.current_scenario = None
    
    def list_available_scenarios(self):
        """Display all available roleplay scenarios."""
        print("\n" + "="*60)
        print("📋 AVAILABLE SCENARIOS")
        print("="*60)
        
        scenarios = list_scenarios()
        for key, info in scenarios.items():
            print(f"\n🎭 {key}")
            print(f"   Context: {info['context']}")
            print(f"   Character: {info['character']}")
            print(f"   Difficulty: {info['difficulty']}")
            print(f"   Tags: {', '.join(info['tags'])}")
        
        print("\n" + "="*60 + "\n")
    
    def view_roleplay_prompt(self, scenario_key):
        """View the full roleplay prompt for a scenario."""
        try:
            prompt = get_roleplay_prompt(scenario_key)
            print("\n" + "="*60)
            print(f"🎭 ROLEPLAY PROMPT: {scenario_key}")
            print("="*60)
            print(prompt)
            print("="*60 + "\n")
        except ValueError as e:
            print(f"❌ Error: {e}\n")
    
    def start_conversation(self, scenario_key):
        """Start a new conversation with a scenario."""
        if not self.client:
            print("❌ Cannot start conversation without OpenAI API key.\n")
            return
        
        try:
            self.current_scenario = scenario_key
            self.conversation_history = []
            self.feedback_history = []
            
            system_prompt = get_roleplay_prompt(scenario_key)
            
            print("\n" + "="*60)
            print(f"🎭 STARTING CONVERSATION: {scenario_key}")
            print("="*60)
            print("Type your messages to practice. Commands:")
            print("  'feedback' - Get detailed feedback on your last message")
            print("  'summary' - End session and get summary")
            print("  'quit' - Exit conversation")
            print("="*60 + "\n")
            
            # Get AI's opening message
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt}
                ],
                temperature=0.8,
                max_tokens=150
            )
            
            ai_message = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": ai_message})
            
            print(f"🤖 AI: {ai_message}\n")
            
            # Start conversation loop
            self._conversation_loop(system_prompt)
            
        except ValueError as e:
            print(f"❌ Error: {e}\n")
    
    def _conversation_loop(self, system_prompt):
        """Main conversation loop."""
        while True:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'quit':
                print("\n👋 Conversation ended.\n")
                break
            
            if user_input.lower() == 'feedback':
                if self.conversation_history:
                    self._show_detailed_feedback()
                else:
                    print("❌ No messages to evaluate yet.\n")
                continue
            
            if user_input.lower() == 'summary':
                self._show_session_summary()
                break
            
            # Add user message to history
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # Get AI response
            messages = [{"role": "system", "content": system_prompt}] + self.conversation_history
            
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.8,
                    max_tokens=200
                )
                
                ai_message = response.choices[0].message.content
                self.conversation_history.append({"role": "assistant", "content": ai_message})
                
                print(f"\n🤖 AI: {ai_message}\n")
                
                # Optional: Show inline feedback
                inline_feedback = self._get_inline_feedback(user_input)
                if inline_feedback and inline_feedback != "NONE":
                    print(f"💡 Quick tip: {inline_feedback}\n")
                
            except Exception as e:
                print(f"❌ Error: {e}\n")
                break
    
    def _get_inline_feedback(self, user_message):
        """Get brief inline feedback for a message."""
        try:
            prompt = create_inline_feedback_prompt(self.current_scenario, user_message)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=50
            )
            
            return response.choices[0].message.content.strip()
        except Exception:
            return None
    
    def _show_detailed_feedback(self):
        """Show detailed feedback for the last user message."""
        if not self.client:
            print("❌ Cannot generate feedback without OpenAI API key.\n")
            return
        
        # Find last user message
        user_messages = [msg for msg in self.conversation_history if msg["role"] == "user"]
        if not user_messages:
            print("❌ No user messages to evaluate.\n")
            return
        
        last_message = user_messages[-1]["content"]
        
        try:
            system_prompt, user_prompt = create_feedback_prompt(
                self.current_scenario,
                self.conversation_history,
                last_message
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500,
                response_format={"type": "json_object"} if self.provider == "openai" else None
            )
            
            feedback = json.loads(response.choices[0].message.content)
            self.feedback_history.append(feedback)
            
            print("\n" + "="*60)
            print("📊 DETAILED FEEDBACK")
            print("="*60)
            print(f"\n📝 Your message: \"{last_message}\"\n")
            print(f"🎯 Tone: {feedback['tone']['score']}/100")
            print(f"   {feedback['tone']['feedback']}\n")
            print(f"✨ Clarity: {feedback['clarity']['score']}/100")
            print(f"   {feedback['clarity']['feedback']}\n")
            print(f"❤️  Empathy: {feedback['empathy']['score']}/100")
            print(f"   {feedback['empathy']['feedback']}\n")
            print(f"🔄 Engagement: {feedback['engagement']['score']}/100")
            print(f"   {feedback['engagement']['feedback']}\n")
            print(f"💭 Overall: {feedback['overall_impression']}\n")
            print(f"💡 Quick tip: {feedback['quick_tip']}\n")
            print("="*60 + "\n")
            
        except Exception as e:
            print(f"❌ Error generating feedback: {e}\n")
    
    def _show_session_summary(self):
        """Show end-of-session summary."""
        if not self.client:
            print("❌ Cannot generate summary without OpenAI API key.\n")
            return
        
        if not self.conversation_history:
            print("❌ No conversation to summarize.\n")
            return
        
        try:
            system_prompt, user_prompt = create_summary_prompt(
                self.current_scenario,
                self.conversation_history,
                self.feedback_history
            )
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=600,
                response_format={"type": "json_object"} if self.provider == "openai" else None
            )
            
            summary = json.loads(response.choices[0].message.content)
            
            print("\n" + "="*60)
            print("🎓 SESSION SUMMARY")
            print("="*60)
            print(f"\n✨ {summary['session_headline']}\n")
            print("💪 STRENGTHS:")
            for i, strength in enumerate(summary['strengths'], 1):
                print(f"   {i}. {strength}")
            print("\n🌱 AREAS TO GROW:")
            for i, area in enumerate(summary['growth_areas'], 1):
                print(f"   {i}. {area}")
            print(f"\n🎯 NEXT STEP: {summary['next_step']}\n")
            print(f"💌 {summary['encouragement']}\n")
            print("="*60 + "\n")
            
        except Exception as e:
            print(f"❌ Error generating summary: {e}\n")
    
    def test_feedback_prompt(self, scenario, sample_conversation, sample_message):
        """Test feedback prompt with sample data."""
        print("\n" + "="*60)
        print("🧪 TESTING FEEDBACK PROMPT")
        print("="*60)
        
        system_prompt, user_prompt = create_feedback_prompt(
            scenario,
            sample_conversation,
            sample_message
        )
        
        print("\n📋 SYSTEM PROMPT:")
        print("-" * 60)
        print(system_prompt)
        print("\n📋 USER PROMPT:")
        print("-" * 60)
        print(user_prompt)
        print("\n" + "="*60 + "\n")
        
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7,
                    max_tokens=500,
                    response_format={"type": "json_object"}
                )
                
                feedback = json.loads(response.choices[0].message.content)
                print("🤖 AI RESPONSE:")
                print("-" * 60)
                print(json.dumps(feedback, indent=2))
                print("\n" + "="*60 + "\n")
                
            except Exception as e:
                print(f"❌ Error: {e}\n")


def main():
    """Main interactive menu."""
    print("\n" + "="*60)
    print("🧠 NEUROPILOT PROMPT TESTING PLAYGROUND")
    print("="*60)
    print("\nThis tool lets you:")
    print("  1. View and test roleplay prompts")
    print("  2. Test feedback/evaluation prompts")
    print("  3. Practice live conversations with AI")
    print("  4. Experiment and refine prompt engineering")
    print("\n" + "="*60)
    
    tester = PromptTester()
    
    while True:
        print("\n📋 MENU:")
        print("  1. List available scenarios")
        print("  2. View a roleplay prompt")
        print("  3. Start a practice conversation")
        print("  4. Test feedback prompt (with sample data)")
        print("  5. Quit")
        
        choice = input("\nChoice: ").strip()
        
        if choice == "1":
            tester.list_available_scenarios()
        
        elif choice == "2":
            scenario = input("Enter scenario key (e.g., 'diwali_party'): ").strip()
            tester.view_roleplay_prompt(scenario)
        
        elif choice == "3":
            scenario = input("Enter scenario key (e.g., 'diwali_party'): ").strip()
            tester.start_conversation(scenario)
        
        elif choice == "4":
            # Sample test data
            sample_conv = [
                {"role": "assistant", "content": "Hey! So glad you could make it! How have you been?"},
                {"role": "user", "content": "Good."}
            ]
            tester.test_feedback_prompt(
                "diwali_party",
                sample_conv,
                "Good."
            )
        
        elif choice == "5":
            print("\n👋 Thanks for testing! Happy prompting!\n")
            break
        
        else:
            print("❌ Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()

"""
Batch Prompt Comparison Tool
Test multiple variations of prompts and compare results side-by-side
"""

import os
import json
from openai import OpenAI
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from examples.test_cases import *


class BatchTester:
    """Compare different prompt variations on the same test cases."""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable.")
        self.client = OpenAI(api_key=self.api_key)
    
    def test_single_case(self, test_case, system_prompt, user_prompt_template):
        """Run a single test case and return results."""
        try:
            # Build conversation history for context
            history_text = ""
            for msg in test_case['conversation_history']:
                role = "AI" if msg["role"] == "assistant" else "User"
                history_text += f"{role}: {msg['content']}\n"
            
            user_prompt = user_prompt_template.format(
                context=test_case['scenario'],
                conversation_history=history_text.strip(),
                user_message=test_case['user_message']
            )
            
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
            return feedback
            
        except Exception as e:
            return {"error": str(e)}
    
    def compare_prompts(self, prompt_versions, test_cases):
        """
        Compare multiple prompt versions on the same test cases.
        
        Args:
            prompt_versions: List of dicts with 'name', 'system_prompt', 'user_template'
            test_cases: List of test case dicts
        
        Returns:
            Comparison results
        """
        results = {}
        
        for prompt_version in prompt_versions:
            version_name = prompt_version['name']
            print(f"\n🧪 Testing: {version_name}")
            print("-" * 60)
            
            results[version_name] = []
            
            for i, test_case in enumerate(test_cases, 1):
                print(f"  Test case {i}/{len(test_cases)}...", end=" ")
                
                feedback = self.test_single_case(
                    test_case,
                    prompt_version['system_prompt'],
                    prompt_version['user_template']
                )
                
                results[version_name].append({
                    'test_case': i,
                    'feedback': feedback,
                    'expected': test_case.get('expected_feedback', {})
                })
                
                print("✓")
        
        return results
    
    def print_comparison(self, results, test_cases):
        """Print side-by-side comparison of results."""
        print("\n" + "="*80)
        print("📊 RESULTS COMPARISON")
        print("="*80)
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📝 TEST CASE {i}:")
            print(f"   Message: \"{test_case['user_message'][:60]}...\"")
            print(f"   Expected: {test_case.get('expected_feedback', {}).get('tone', 'N/A')}")
            print()
            
            for version_name, version_results in results.items():
                result = version_results[i-1]
                feedback = result['feedback']
                
                print(f"   🔹 {version_name}:")
                if 'error' in feedback:
                    print(f"      ❌ Error: {feedback['error']}")
                else:
                    print(f"      Tone: {feedback.get('tone', {}).get('score', 'N/A')}/100")
                    print(f"      Clarity: {feedback.get('clarity', {}).get('score', 'N/A')}/100")
                    print(f"      Empathy: {feedback.get('empathy', {}).get('score', 'N/A')}/100")
                    print(f"      Engagement: {feedback.get('engagement', {}).get('score', 'N/A')}/100")
                    if 'quick_tip' in feedback:
                        print(f"      Tip: {feedback['quick_tip'][:70]}...")
                print()
        
        # Calculate average scores
        print("\n" + "="*80)
        print("📈 AVERAGE SCORES BY PROMPT VERSION")
        print("="*80 + "\n")
        
        for version_name, version_results in results.items():
            valid_results = [r for r in version_results if 'error' not in r['feedback']]
            
            if valid_results:
                avg_tone = sum(r['feedback']['tone']['score'] for r in valid_results) / len(valid_results)
                avg_clarity = sum(r['feedback']['clarity']['score'] for r in valid_results) / len(valid_results)
                avg_empathy = sum(r['feedback']['empathy']['score'] for r in valid_results) / len(valid_results)
                avg_engagement = sum(r['feedback']['engagement']['score'] for r in valid_results) / len(valid_results)
                
                print(f"🔹 {version_name}:")
                print(f"   Tone:       {avg_tone:.1f}/100")
                print(f"   Clarity:    {avg_clarity:.1f}/100")
                print(f"   Empathy:    {avg_empathy:.1f}/100")
                print(f"   Engagement: {avg_engagement:.1f}/100")
                print(f"   Overall:    {(avg_tone + avg_clarity + avg_empathy + avg_engagement) / 4:.1f}/100")
                print()


def main():
    """Example: Compare original prompt vs. a modified version."""
    
    # Import the original feedback prompt
    from prompts.feedback_prompts import FEEDBACK_SYSTEM_PROMPT, FEEDBACK_USER_PROMPT_TEMPLATE
    
    # Define test prompt versions
    prompt_versions = [
        {
            "name": "Original Prompt",
            "system_prompt": FEEDBACK_SYSTEM_PROMPT,
            "user_template": FEEDBACK_USER_PROMPT_TEMPLATE
        },
        # Example: You can add variations here
        # {
        #     "name": "More Strict Scoring",
        #     "system_prompt": MODIFIED_SYSTEM_PROMPT,
        #     "user_template": FEEDBACK_USER_PROMPT_TEMPLATE
        # }
    ]
    
    # Select test cases
    test_cases = [
        TEST_CASE_1,  # Needs more engagement
        TEST_CASE_2,  # Tone mismatch (too casual)
        TEST_CASE_3,  # Strong response
        TEST_CASE_6,  # Conversation killer
        TEST_CASE_7,  # Rambling
    ]
    
    print("\n" + "="*80)
    print("🧪 NEUROPILOT BATCH PROMPT TESTING")
    print("="*80)
    print(f"\nTesting {len(prompt_versions)} prompt version(s) on {len(test_cases)} test cases...")
    
    tester = BatchTester()
    results = tester.compare_prompts(prompt_versions, test_cases)
    tester.print_comparison(results, test_cases)
    
    print("\n" + "="*80)
    print("✅ Testing complete!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()

"""
Sample Test Cases for Prompt Evaluation
Use these to manually test and compare prompt outputs
"""

# Test Case 1: Casual social setting - needs more engagement
TEST_CASE_1 = {
    "scenario": "diwali_party",
    "conversation_history": [
        {"role": "assistant", "content": "Hey! So glad you could make it to the party! Have you been to a Diwali celebration before?"},
        {"role": "user", "content": "No, this is my first time."},
        {"role": "assistant", "content": "Oh that's exciting! Well, you picked a great one to start with. My friend Raj really went all out with the decorations this year. Are you hungry? There's tons of food in the kitchen."},
    ],
    "user_message": "Yeah, I'm pretty hungry.",
    "expected_feedback": {
        "tone": "Should be 60-75 (appropriate but could be more enthusiastic for a party)",
        "clarity": "Should be 70-80 (clear but brief)",
        "empathy": "Should be 50-60 (doesn't acknowledge the AI's comment about decorations or food)",
        "engagement": "Should be 50-65 (doesn't provide hooks for conversation)"
    },
    "improvement_example": "I'm starving! Everything looks amazing. What would you recommend trying first?"
}

# Test Case 2: Professional setting - tone mismatch
TEST_CASE_2 = {
    "scenario": "job_interview",
    "conversation_history": [
        {"role": "assistant", "content": "Thanks for coming in today. I'm Alex, I'll be interviewing you for the junior developer position. To start, could you tell me a bit about your background and what interests you about this role?"},
    ],
    "user_message": "Hey Alex! Yeah so I've been coding for like 3 years and honestly your company seems pretty cool lol. I'm really into React and stuff.",
    "expected_feedback": {
        "tone": "Should be 40-55 (way too casual for interview - 'Hey', 'lol', 'stuff')",
        "clarity": "Should be 50-65 (vague - 'pretty cool', 'stuff')",
        "empathy": "Should be 65-75 (does respond to the question)",
        "engagement": "Should be 60-70 (opens conversation but unprofessionally)"
    },
    "improvement_example": "Thanks for having me, Alex. I've been developing software for three years, focusing mainly on frontend technologies like React. I'm really drawn to your company's focus on accessible design—it aligns well with my interest in building user-friendly applications."
}

# Test Case 3: Strong response - should score high
TEST_CASE_3 = {
    "scenario": "office_lunch",
    "conversation_history": [
        {"role": "assistant", "content": "Hey! Mind if I join you?"},
        {"role": "user", "content": "Of course! Please sit down."},
        {"role": "assistant", "content": "Thanks! How's your week going so far?"},
    ],
    "user_message": "Pretty good! That client presentation yesterday went better than expected. How about you? I heard your team had a big deadline this week.",
    "expected_feedback": {
        "tone": "Should be 85-95 (friendly, appropriate for workplace lunch)",
        "clarity": "Should be 85-95 (clear, well-structured)",
        "empathy": "Should be 90-100 (acknowledges their question AND shows interest in their work)",
        "engagement": "Should be 90-100 (great conversation flow, asks follow-up)"
    }
}

# Test Case 4: Overly formal in casual setting
TEST_CASE_4 = {
    "scenario": "diwali_party",
    "conversation_history": [
        {"role": "assistant", "content": "Hey! Want to grab some samosas? They're incredible."},
    ],
    "user_message": "Thank you for the suggestion. I would be pleased to partake in the culinary offerings.",
    "expected_feedback": {
        "tone": "Should be 30-45 (way too formal for a party)",
        "clarity": "Should be 75-85 (technically clear but awkwardly phrased)",
        "empathy": "Should be 55-65 (responds but stiffly)",
        "engagement": "Should be 40-55 (doesn't create natural flow)"
    },
    "improvement_example": "Yes! I'd love to try them. Have you had any yet?"
}

# Test Case 5: Good empathy, needs better engagement
TEST_CASE_5 = {
    "scenario": "networking_event",
    "conversation_history": [
        {"role": "assistant", "content": "Hi! I'm Sam. This is my first time at one of these networking events—feeling a bit out of my element to be honest!"},
    ],
    "user_message": "I totally understand, networking events can be intimidating. I felt the same way at my first one.",
    "expected_feedback": {
        "tone": "Should be 80-90 (appropriate, professional yet friendly)",
        "clarity": "Should be 80-90 (clear and relatable)",
        "empathy": "Should be 85-95 (excellent acknowledgment and relating)",
        "engagement": "Should be 60-70 (good but could ask a question to continue conversation)"
    },
    "improvement_example": "I totally understand, networking events can be intimidating. I felt the same way at my first one. What brings you here tonight? Are you looking for opportunities in a specific area?"
}

# Test Case 6: One-word response (conversation killer)
TEST_CASE_6 = {
    "scenario": "office_lunch",
    "conversation_history": [
        {"role": "assistant", "content": "How was your weekend? Do anything fun?"},
    ],
    "user_message": "Fine.",
    "expected_feedback": {
        "tone": "Should be 50-60 (neutral but too brief)",
        "clarity": "Should be 70-80 (clear but minimal)",
        "empathy": "Should be 30-40 (doesn't acknowledge or reciprocate)",
        "engagement": "Should be 20-35 (conversation killer, no hooks)"
    },
    "improvement_example": "It was good! Spent most of it hiking. How about yours?"
}

# Test Case 7: Rambling/unclear message
TEST_CASE_7 = {
    "scenario": "job_interview",
    "conversation_history": [
        {"role": "assistant", "content": "Can you tell me about a challenging project you worked on?"},
    ],
    "user_message": "Well there was this one time when we were working on this app and it was really complicated because there were so many features and also the deadline was tight and I had to learn some new stuff but I mean it all worked out eventually even though there were some issues along the way with the team and stuff.",
    "expected_feedback": {
        "tone": "Should be 60-70 (appropriate anxiety/nervousness but rambling)",
        "clarity": "Should be 35-50 (very unclear, run-on, lacks structure)",
        "empathy": "Should be 60-70 (attempts to answer the question)",
        "engagement": "Should be 50-60 (shares information but hard to follow)"
    },
    "improvement_example": "One challenging project was building a customer-facing mobile app in three weeks. The tight deadline and learning curve for React Native were tough, but I broke it into smaller milestones and collaborated closely with my team. We delivered on time, and I learned a lot about project management under pressure."
}


def print_test_case(test_case):
    """Pretty print a test case."""
    print("\n" + "="*70)
    print(f"📝 SCENARIO: {test_case['scenario']}")
    print("="*70)
    print("\n💬 CONVERSATION HISTORY:")
    for msg in test_case['conversation_history']:
        role = "AI" if msg['role'] == 'assistant' else "User"
        print(f"  {role}: {msg['content']}")
    print(f"\n➡️  USER MESSAGE TO EVALUATE:")
    print(f"  {test_case['user_message']}")
    print(f"\n📊 EXPECTED FEEDBACK:")
    for category, expectation in test_case['expected_feedback'].items():
        print(f"  • {category.title()}: {expectation}")
    if 'improvement_example' in test_case:
        print(f"\n✨ IMPROVEMENT EXAMPLE:")
        print(f"  {test_case['improvement_example']}")
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    """Print all test cases for review."""
    test_cases = [
        ("Needs More Engagement", TEST_CASE_1),
        ("Tone Mismatch (Too Casual)", TEST_CASE_2),
        ("Strong Response", TEST_CASE_3),
        ("Tone Mismatch (Too Formal)", TEST_CASE_4),
        ("Good Empathy, Needs Engagement", TEST_CASE_5),
        ("Conversation Killer", TEST_CASE_6),
        ("Rambling/Unclear", TEST_CASE_7),
    ]
    
    print("\n" + "="*70)
    print("🧪 NEUROPILOT PROMPT TEST CASES")
    print("="*70)
    print("\nUse these test cases to evaluate your feedback prompts.")
    print("Compare AI-generated feedback against expected scores/feedback.")
    
    for name, test_case in test_cases:
        print(f"\n\n{'='*70}")
        print(f"TEST: {name}")
        print_test_case(test_case)

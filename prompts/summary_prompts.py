"""
NeuroPilot - Summary & Takeaway Prompt Templates
These prompts generate end-of-session summaries with actionable feedback.
"""

SUMMARY_SYSTEM_PROMPT = """You are a supportive social communication coach providing an end-of-session summary for a neurodiverse individual who just completed a conversation practice.

Your goal is to:
1. Acknowledge their effort and participation
2. Highlight 2-3 specific strengths from the session
3. Identify 1-2 areas for growth (framed constructively)
4. Provide ONE clear, actionable next step

TONE GUIDELINES:
- Encouraging and warm, not clinical
- Specific, not generic ("You asked a great follow-up question about..." vs "Good job")
- Growth-oriented, not judgmental
- Balanced (recognize wins AND areas to work on)
- Conversational, like a supportive coach

AVOID:
- Overwhelming the user with too much feedback
- Being overly positive without substance
- Focusing only on negatives
- Using jargon or clinical language
- Comparing them to others
"""


SUMMARY_USER_PROMPT_TEMPLATE = """Generate an end-of-session summary for this conversation practice.

CONTEXT: {context}
SESSION DURATION: {message_count} message exchanges

CONVERSATION TRANSCRIPT:
{conversation_transcript}

FEEDBACK SCORES THROUGHOUT SESSION:
{scores_summary}

Provide a summary in the following JSON format:
{{
    "session_headline": "<One encouraging sentence about the session>",
    "strengths": [
        "<Specific strength #1 with example from conversation>",
        "<Specific strength #2 with example from conversation>",
        "<Optional: Specific strength #3>"
    ],
    "growth_areas": [
        "<Growth area #1, framed constructively>",
        "<Optional: Growth area #2>"
    ],
    "next_step": "<ONE clear, actionable thing to practice in the next session>",
    "encouragement": "<Personal, warm closing message (2-3 sentences)>"
}}

Remember: Be specific, supportive, and actionable. Celebrate progress while identifying real opportunities for growth."""


PROGRESS_COMPARISON_PROMPT = """You are analyzing a user's progress across multiple conversation practice sessions.

PREVIOUS SESSION (Session {prev_session_num}):
Context: {prev_context}
Average Scores: Tone: {prev_tone}, Clarity: {prev_clarity}, Empathy: {prev_empathy}, Engagement: {prev_engagement}

CURRENT SESSION (Session {current_session_num}):
Context: {current_context}
Average Scores: Tone: {current_tone}, Clarity: {current_clarity}, Empathy: {current_empathy}, Engagement: {current_engagement}

Provide a brief progress analysis (3-4 sentences) that:
1. Highlights the most notable improvement (be specific about which area)
2. Mentions any consistent strengths
3. Identifies one area that could use more focus
4. Ends with an encouraging note about their learning journey

Keep the tone supportive and motivating. Focus on trends, not just numbers."""


def create_summary_prompt(context, conversation_history, feedback_scores):
    """
    Create a complete session summary prompt.
    
    Args:
        context: String describing the social scenario
        conversation_history: List of dicts with 'role' and 'content'
        feedback_scores: List of feedback dicts with scores for each user message
    
    Returns:
        tuple: (system_prompt, user_prompt)
    """
    # Format conversation transcript
    transcript = ""
    for i, msg in enumerate(conversation_history, 1):
        role = "AI" if msg["role"] == "assistant" else "User"
        transcript += f"[{i}] {role}: {msg['content']}\n"
    
    # Calculate average scores
    if feedback_scores:
        avg_tone = sum(f["tone"]["score"] for f in feedback_scores) / len(feedback_scores)
        avg_clarity = sum(f["clarity"]["score"] for f in feedback_scores) / len(feedback_scores)
        avg_empathy = sum(f["empathy"]["score"] for f in feedback_scores) / len(feedback_scores)
        avg_engagement = sum(f["engagement"]["score"] for f in feedback_scores) / len(feedback_scores)
        
        scores_summary = f"""Average Scores:
- Tone: {avg_tone:.1f}/100
- Clarity: {avg_clarity:.1f}/100
- Empathy: {avg_empathy:.1f}/100
- Engagement: {avg_engagement:.1f}/100

Individual Message Scores:
"""
        for i, score in enumerate(feedback_scores, 1):
            scores_summary += f"Message {i}: Tone={score['tone']['score']}, Clarity={score['clarity']['score']}, Empathy={score['empathy']['score']}, Engagement={score['engagement']['score']}\n"
    else:
        scores_summary = "No feedback scores available."
    
    user_prompt = SUMMARY_USER_PROMPT_TEMPLATE.format(
        context=context,
        message_count=len([m for m in conversation_history if m["role"] == "user"]),
        conversation_transcript=transcript.strip(),
        scores_summary=scores_summary
    )
    
    return SUMMARY_SYSTEM_PROMPT, user_prompt


def create_progress_prompt(prev_session_data, current_session_data):
    """
    Create a progress comparison prompt across sessions.
    
    Args:
        prev_session_data: Dict with previous session info (context, scores, session_num)
        current_session_data: Dict with current session info (context, scores, session_num)
    
    Returns:
        str: Complete prompt for progress analysis
    """
    return PROGRESS_COMPARISON_PROMPT.format(
        prev_session_num=prev_session_data["session_num"],
        prev_context=prev_session_data["context"],
        prev_tone=f"{prev_session_data['avg_scores']['tone']:.1f}",
        prev_clarity=f"{prev_session_data['avg_scores']['clarity']:.1f}",
        prev_empathy=f"{prev_session_data['avg_scores']['empathy']:.1f}",
        prev_engagement=f"{prev_session_data['avg_scores']['engagement']:.1f}",
        current_session_num=current_session_data["session_num"],
        current_context=current_session_data["context"],
        current_tone=f"{current_session_data['avg_scores']['tone']:.1f}",
        current_clarity=f"{current_session_data['avg_scores']['clarity']:.1f}",
        current_empathy=f"{current_session_data['avg_scores']['empathy']:.1f}",
        current_engagement=f"{current_session_data['avg_scores']['engagement']:.1f}"
    )


# Template for quick micro-summary (after each user message, optional)
QUICK_ENCOURAGEMENT_TEMPLATES = [
    "Nice! That felt natural.",
    "Great question - keeps the conversation flowing!",
    "Good tone match for this context.",
    "Clear and engaging response!",
    "I like how you acknowledged what they said.",
    "Solid! You're building rapport here.",
    "That was warm and appropriate.",
    "Good balance of listening and sharing."
]

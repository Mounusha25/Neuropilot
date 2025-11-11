"""
NeuroPilot Prompts Package
Core prompt templates for conversation simulation, feedback, and summaries.
Enhanced with adaptive neurodiversity-aware intelligence.
"""

from .roleplay_prompts import (
    get_roleplay_prompt,
    list_scenarios,
    ROLEPLAY_PROMPTS
)

from .feedback_prompts import (
    create_feedback_prompt,
    create_inline_feedback_prompt,
    FEEDBACK_SYSTEM_PROMPT,
    SCORING_RUBRIC
)

from .summary_prompts import (
    create_summary_prompt,
    create_progress_prompt,
    SUMMARY_SYSTEM_PROMPT
)

from .adaptive_agent_system import (
    get_adaptive_context,
    ADAPTIVE_AGENT_CORE,
    NEURODIVERSITY_PATTERNS,
    ENGAGEMENT_MONITORING_PROMPT,
    CONVERSATION_CHECKPOINT_SYSTEM
)

from .avatar_profiles import (
    get_avatar_profile,
    get_all_avatars,
    get_avatar_for_scenario,
    AVATAR_PROFILES
)

__all__ = [
    # Roleplay
    'get_roleplay_prompt',
    'list_scenarios',
    'ROLEPLAY_PROMPTS',
    
    # Feedback
    'create_feedback_prompt',
    'create_inline_feedback_prompt',
    'FEEDBACK_SYSTEM_PROMPT',
    'SCORING_RUBRIC',
    
    # Summary
    'create_summary_prompt',
    'create_progress_prompt',
    'SUMMARY_SYSTEM_PROMPT',
    
    # Adaptive Agent System
    'get_adaptive_context',
    'ADAPTIVE_AGENT_CORE',
    'NEURODIVERSITY_PATTERNS',
    'ENGAGEMENT_MONITORING_PROMPT',
    'CONVERSATION_CHECKPOINT_SYSTEM',
    
    # Avatar Profiles
    'get_avatar_profile',
    'get_all_avatars',
    'get_avatar_for_scenario',
    'AVATAR_PROFILES',
]

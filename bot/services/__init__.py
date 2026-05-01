"""
خدمات البوت - FitCoach Bot
"""
from bot.services.nutrition_service import NutritionService
from bot.services.analytics_service import AdaptiveIntelligence, get_adaptive_insights, generate_weekly_summary
from bot.services.ai_coach import AICoach, ai_coach, get_ai_coach

__all__ = [
    'NutritionService',
    'AdaptiveIntelligence',
    'get_adaptive_insights',
    'generate_weekly_summary',
    'AICoach',
    'ai_coach',
    'get_ai_coach'
]

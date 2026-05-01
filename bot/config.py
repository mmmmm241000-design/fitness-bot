"""
إعدادات البوت - FitCoach Bot
"""
import os
from dataclasses import dataclass, field
from typing import Optional, List
from dotenv import load_dotenv

load_dotenv()


def _get_admin_ids():
    admin_ids_str = os.getenv("ADMIN_IDS", "")
    return admin_ids_str.split(",") if admin_ids_str else []


def _get_activity_multipliers():
    return {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "athlete": 1.9
    }


@dataclass
class BotConfig:
    """إعدادات البوت"""
    bot_token: str = ""
    admin_ids: List[str] = field(default_factory=list)
    database_path: str = "data/fitness.db"
    log_level: str = "INFO"
    log_file: str = "logs/bot.log"

    # إعدادات Telegram
    parse_mode: str = "HTML"
    disable_web_preview: bool = True

    # إعدادات التتبع
    max_meal_name_length: int = 100
    max_notes_length: int = 500

    # إعدادات الحسابات
    min_age: int = 14
    max_age: int = 70
    min_height: float = 140.0
    max_height: float = 220.0
    min_weight: float = 30.0
    max_weight: float = 200.0
    min_body_fat: float = 3.0
    max_body_fat: float = 50.0

    # معاملات النشاط البدني
    activity_multipliers: dict = field(default_factory=_get_activity_multipliers)

    def __post_init__(self):
        if not self.bot_token:
            self.bot_token = os.getenv("BOT_TOKEN", "")
        if not self.admin_ids:
            self.admin_ids = _get_admin_ids()

    def validate(self) -> bool:
        """التحقق من الإعدادات المطلوبة"""
        if not self.bot_token:
            return False
        return True


def _get_protein_per_kg():
    return {
        "bulking": 2.0,      # ضخامة
        "cutting": 2.5,      # تنشيف
        "recomp": 2.2        # إعادة تركيب
    }


def _get_macro_ratios():
    return {
        "bulking": {"protein": 25, "carbs": 55, "fats": 20},
        "cutting": {"protein": 40, "carbs": 35, "fats": 25},
        "recomp": {"protein": 35, "carbs": 40, "fats": 25}
    }


@dataclass
class NutritionConfig:
    """إعدادات التغذية"""
    # معاملات حساب البروتين (غرام لكل كيلو من وزن الجسم)
    protein_per_kg: dict = field(default_factory=_get_protein_per_kg)

    # نسب توزيع المغذيات (حسب الهدف)
    macro_ratios: dict = field(default_factory=_get_macro_ratios)


def _get_rest_days():
    return {
        "chest": 48,
        "back": 48,
        "shoulders": 48,
        "biceps": 24,
        "triceps": 24,
        "legs": 72,
        "abs": 24
    }


def _get_default_sets_reps():
    return {
        "beginner": {"sets": 3, "reps_min": 12, "reps_max": 15},
        "intermediate": {"sets": 4, "reps_min": 8, "reps_max": 12},
        "advanced": {"sets": 5, "reps_min": 6, "reps_max": 10}
    }


@dataclass
class WorkoutConfig:
    """إعدادات التدريب"""
    # أيام الراحة بين مجموعات العضلات
    rest_days: dict = field(default_factory=_get_rest_days)

    # عدد المجموعات والتكرارات المقترحة
    default_sets_reps: dict = field(default_factory=_get_default_sets_reps)


# إنشاء كائنات الإعدادات العامة
config = BotConfig()
nutrition_config = NutritionConfig()
workout_config = WorkoutConfig()

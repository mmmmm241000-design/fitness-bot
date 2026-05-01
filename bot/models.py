"""
نماذج البيانات - FitCoach Bot
نحدد هنا جميع هياكل البيانات المستخدمة في البوت
"""
from datetime import datetime, date
from typing import Optional, List
from dataclasses import dataclass, field
from enum import Enum

from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Float, Boolean, DateTime, Date, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from bot.config import config, nutrition_config

# إنشاء قاعدة الاتصال
engine = create_engine(f'sqlite:///{config.database_path}', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)


class ExperienceLevel(str, Enum):
    """مستوى الخبرة"""
    BEGINNER = "beginner"      # مبتدئ
    INTERMEDIATE = "intermediate"  # متوسط
    ADVANCED = "advanced"      # متقدم


class GoalType(str, Enum):
    """نوع الهدف"""
    BULKING = "bulking"        # ضخامة
    CUTTING = "cutting"        # تنشيف
    RECOMP = "recomp"          # إعادة تركيب


class ActivityLevel(str, Enum):
    """مستوى النشاط"""
    SEDENTARY = "sedentary"     # خامل
    LIGHT = "light"            # نشاط خفيف
    MODERATE = "moderate"      # نشاط متوسط
    ACTIVE = "active"          # نشط جداً
    ATHLETE = "athlete"        # رياضي محترف


class MealType(str, Enum):
    """نوع الوجبة"""
    BREAKFAST = "breakfast"     # إفطار
    LUNCH = "lunch"            # غداء
    DINNER = "dinner"          # عشاء
    SNACK = "snack"            # وجبة خفيفة


class MuscleGroup(str, Enum):
    """مجموعات العضلات"""
    CHEST = "chest"            # صدر
    BACK = "back"              # ظهر
    SHOULDERS = "shoulders"    # أكتاف
    BICEPS = "biceps"          # عضلات الذراع الأمامية
    TRICEPS = "triceps"        # عضلات الذراع الخلفية
    LEGS = "legs"              # ساقيك
    ABS = "abs"                # بطن


class EquipmentType(str, Enum):
    """نوع المعدات"""
    FREE_WEIGHTS = "free_weights"      # أوزان حرة
    MACHINE = "machine"                # آلة
    BODYWEIGHT = "bodyweight"          # وزن الجسم
    CABLE = "cable"                    # كابل


class User(Base):
    """جدول المستخدمين"""
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    name = Column(String(100))
    age = Column(Integer)
    height = Column(Float)
    weight = Column(Float)
    body_fat = Column(Float)
    experience_level = Column(String(20), default=ExperienceLevel.BEGINNER.value)
    workout_days = Column(Integer, default=3)
    goal = Column(String(20), default=GoalType.RECOMP.value)
    activity_level = Column(String(20), default=ActivityLevel.MODERATE.value)
    water_goal = Column(Float, default=3.0)  # لتر يومياً
    sleep_goal = Column(Float, default=8.0)  # ساعات
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # العلاقات
    daily_progress = relationship("DailyProgress", back_populates="user", cascade="all, delete-orphan")
    meals = relationship("Meal", back_populates="user", cascade="all, delete-orphan")
    workouts = relationship("Workout", back_populates="user", cascade="all, delete-orphan")
    settings = relationship("Settings", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.user_id}, name={self.name})>"

    def calculate_bmr(self) -> float:
        """حساب معدل الأيض الأساسي (Basal Metabolic Rate)"""
        # معادلة ميفلين-ستور
        return (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + 5

    def calculate_tdee(self) -> float:
        """حساب إجمالي استهلاك الطاقة اليومي (Total Daily Energy Expenditure)"""
        bmr = self.calculate_bmr()
        multiplier = config.activity_multipliers.get(self.activity_level, 1.55)
        return bmr * multiplier

    def get_nutrition_targets(self) -> dict:
        """حساب الأهداف الغذائية"""
        tdee = self.calculate_tdee()
        protein_ratio = nutrition_config.macro_ratios.get(self.goal, {}).get("protein", 35) / 100
        carbs_ratio = nutrition_config.macro_ratios.get(self.goal, {}).get("carbs", 40) / 100
        fats_ratio = nutrition_config.macro_ratios.get(self.goal, {}).get("fats", 25) / 100

        protein_grams = (self.weight * nutrition_config.protein_per_kg.get(self.goal, 2.2))

        return {
            "calories": round(tdee * 1.1 if self.goal == GoalType.BULKING.value else tdee, 0),
            "protein": round(protein_grams, 1),
            "carbs": round((tdee * carbs_ratio) / 4, 1),
            "fats": round((tdee * fats_ratio) / 9, 1)
        }


class DailyProgress(Base):
    """جدول التقدم اليومي"""
    __tablename__ = 'daily_progress'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    date = Column(Date, default=date.today)
    weight = Column(Float)
    calories = Column(Integer, default=0)
    protein = Column(Float, default=0)
    carbs = Column(Float, default=0)
    fats = Column(Float, default=0)
    water = Column(Float, default=0)  # لتر
    sleep_hours = Column(Float, default=0)
    steps = Column(Integer, default=0)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

    # العلاقات
    user = relationship("User", back_populates="daily_progress")

    def __repr__(self):
        return f"<DailyProgress(user_id={self.user_id}, date={self.date})>"


class Meal(Base):
    """جدول الوجبات"""
    __tablename__ = 'meals'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    date = Column(Date, default=date.today)
    meal_type = Column(String(20))
    name = Column(String(100))
    calories = Column(Integer)
    protein = Column(Float)
    carbs = Column(Float)
    fats = Column(Float)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

    # العلاقات
    user = relationship("User", back_populates="meals")

    def __repr__(self):
        return f"<Meal(id={self.id}, name={self.name}, calories={self.calories})>"


class Exercise(Base):
    """جدول التمارين المرجعي"""
    __tablename__ = 'exercises'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_ar = Column(String(100), nullable=False)
    name_en = Column(String(100))
    muscle_group = Column(String(20))
    equipment = Column(String(20))
    difficulty = Column(String(20))
    description = Column(Text)
    instructions = Column(Text)
    video_url = Column(String(200))
    image_url = Column(String(200))
    calories_per_minute = Column(Float, default=5.0)

    def __repr__(self):
        return f"<Exercise(id={self.id}, name={self.name_ar})>"


class Workout(Base):
    """جدول التمارين المنفذة"""
    __tablename__ = 'workouts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    date = Column(Date, default=date.today)
    exercise_id = Column(Integer, ForeignKey('exercises.id'))
    sets = Column(Integer)
    reps = Column(Integer)
    weight = Column(Float)  # كيلوغرام
    duration = Column(Integer)  # دقائق
    rest_seconds = Column(Integer, default=90)
    notes = Column(Text)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)

    # العلاقات
    user = relationship("User", back_populates="workouts")
    exercise = relationship("Exercise")

    def __repr__(self):
        return f"<Workout(exercise_id={self.exercise_id}, sets={self.sets}, reps={self.reps})>"


class Settings(Base):
    """جدول الإعدادات"""
    __tablename__ = 'settings'

    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    language = Column(String(5), default='ar')
    notifications_enabled = Column(Boolean, default=True)
    reminder_water = Column(Boolean, default=True)
    reminder_meal = Column(Boolean, default=True)
    reminder_workout = Column(Boolean, default=True)
    reminder_time = Column(String(10), default="20:00")
    theme = Column(String(10), default='dark')
    units = Column(String(10), default='metric')  # metric / imperial
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # العلاقات
    user = relationship("User", back_populates="settings")

    def __repr__(self):
        return f"<Settings(user_id={self.user_id}, language={self.language})>"


class NutritionLog(Base):
    """جدول سجل التغذية"""
    __tablename__ = 'nutrition_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    date = Column(Date, default=date.today)
    calories_consumed = Column(Integer, default=0)
    calories_target = Column(Integer)
    protein_consumed = Column(Float, default=0)
    protein_target = Column(Float)
    carbs_consumed = Column(Float, default=0)
    carbs_target = Column(Float)
    fats_consumed = Column(Float, default=0)
    fats_target = Column(Float)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.now)


@dataclass
class UserStats:
    """إحصائيات المستخدم"""
    total_workouts: int = 0
    total_meals: int = 0
    avg_calories: float = 0
    avg_protein: float = 0
    avg_water: float = 0
    avg_sleep: float = 0
    current_streak: int = 0
    longest_streak: int = 0
    weight_change: float = 0
    weight_change_percent: float = 0
    consistency_score: float = 0  # درجة الالتزام


def init_database():
    """إنشاء جميع الجداول"""
    Base.metadata.create_all(engine)


def get_session() -> Session:
    """الحصول على جلسة قاعدة البيانات"""
    return Session()

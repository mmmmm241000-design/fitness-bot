"""
وحدة قاعدة البيانات - FitCoach Bot
تتعامل مع العمليات الأساسية لقاعدة البيانات
"""
from datetime import datetime, date, timedelta
from typing import Optional, List, Tuple
import logging

from sqlalchemy import func, and_, or_
from sqlalchemy.orm import Session as DBSession

from bot.models import (
    Base, engine, Session, User, DailyProgress, Meal, Exercise,
    Workout, Settings, NutritionLog, ExperienceLevel, GoalType,
    MuscleGroup, MealType, UserStats
)
from bot.config import config

logger = logging.getLogger(__name__)


# ==================== وظائف المستخدم ====================

def create_user(telegram_id: int, name: str = None) -> User:
    """إنشاء مستخدم جديد"""
    session = Session()
    try:
        user = User(telegram_id=telegram_id, name=name)
        session.add(user)
        session.commit()
        session.refresh(user)

        # إنشاء الإعدادات الافتراضية
        settings = Settings(user_id=user.user_id)
        session.add(settings)
        session.commit()

        logger.info(f"تم إنشاء مستخدم جديد: {telegram_id}")
        return user
    except Exception as e:
        session.rollback()
        logger.error(f"خطأ في إنشاء المستخدم: {e}")
        raise
    finally:
        session.close()


def get_user_by_telegram_id(telegram_id: int) -> Optional[User]:
    """الحصول على مستخدم بواسطة Telegram ID"""
    session = Session()
    try:
        user = session.query(User).filter(User.telegram_id == telegram_id).first()
        return user
    finally:
        session.close()


def update_user_profile(
    user_id: int,
    age: int = None,
    height: float = None,
    weight: float = None,
    body_fat: float = None,
    experience_level: str = None,
    workout_days: int = None,
    goal: str = None,
    activity_level: str = None
) -> Optional[User]:
    """تحديث الملف الشخصي للمستخدم"""
    session = Session()
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        if not user:
            return None

        if age is not None:
            user.age = age
        if height is not None:
            user.height = height
        if weight is not None:
            user.weight = weight
        if body_fat is not None:
            user.body_fat = body_fat
        if experience_level is not None:
            user.experience_level = experience_level
        if workout_days is not None:
            user.workout_days = workout_days
        if goal is not None:
            user.goal = goal
        if activity_level is not None:
            user.activity_level = activity_level

        user.updated_at = datetime.now()
        session.commit()
        session.refresh(user)

        logger.info(f"تم تحديث الملف الشخصي للمستخدم {user_id}")
        return user
    except Exception as e:
        session.rollback()
        logger.error(f"خطأ في تحديث الملف الشخصي: {e}")
        raise
    finally:
        session.close()


def get_or_create_user(telegram_id: int, name: str = None) -> User:
    """الحصول على مستخدم أو إنشاؤه إذا لم يكن موجوداً"""
    user = get_user_by_telegram_id(telegram_id)
    if not user:
        user = create_user(telegram_id, name)
    return user


# ==================== وظائف التقدم اليومي ====================

def log_daily_progress(
    user_id: int,
    date: date = None,
    weight: float = None,
    water: float = None,
    sleep_hours: float = None,
    steps: int = None,
    notes: str = None
) -> DailyProgress:
    """تسجيل التقدم اليومي"""
    session = Session()
    try:
        if date is None:
            date = date.today()

        # البحث عن سجل موجود لليوم
        progress = session.query(DailyProgress).filter(
            and_(
                DailyProgress.user_id == user_id,
                DailyProgress.date == date
            )
        ).first()

        if progress:
            # تحديث السجل الموجود
            if weight is not None:
                progress.weight = weight
            if water is not None:
                progress.water = water
            if sleep_hours is not None:
                progress.sleep_hours = sleep_hours
            if steps is not None:
                progress.steps = steps
            if notes is not None:
                progress.notes = notes
        else:
            # إنشاء سجل جديد
            progress = DailyProgress(
                user_id=user_id,
                date=date,
                weight=weight,
                water=water,
                sleep_hours=sleep_hours,
                steps=steps,
                notes=notes
            )
            session.add(progress)

        session.commit()
        session.refresh(progress)
        return progress
    except Exception as e:
        session.rollback()
        logger.error(f"خطأ في تسجيل التقدم اليومي: {e}")
        raise
    finally:
        session.close()


def get_daily_progress(user_id: int, target_date: date = None) -> Optional[DailyProgress]:
    """الحصول على التقدم اليومي ليوم معين"""
    session = Session()
    try:
        if target_date is None:
            target_date = date.today()

        progress = session.query(DailyProgress).filter(
            and_(
                DailyProgress.user_id == user_id,
                DailyProgress.date == target_date
            )
        ).first()
        return progress
    finally:
        session.close()


def get_progress_range(user_id: int, days: int = 7) -> List[DailyProgress]:
    """الحصول على سجل التقدم لأيام محددة"""
    session = Session()
    try:
        start_date = date.today() - timedelta(days=days)
        progress_list = session.query(DailyProgress).filter(
            and_(
                DailyProgress.user_id == user_id,
                DailyProgress.date >= start_date
            )
        ).order_by(DailyProgress.date).all()
        return progress_list
    finally:
        session.close()


# ==================== وظائف الوجبات ====================

def add_meal(
    user_id: int,
    meal_type: str,
    name: str,
    calories: int,
    protein: float,
    carbs: float,
    fats: float,
    date: date = None,
    notes: str = None
) -> Meal:
    """إضافة وجبة"""
    session = Session()
    try:
        if date is None:
            date = date.today()

        meal = Meal(
            user_id=user_id,
            date=date,
            meal_type=meal_type,
            name=name,
            calories=calories,
            protein=protein,
            carbs=carbs,
            fats=fats,
            notes=notes
        )
        session.add(meal)
        session.commit()
        session.refresh(meal)

        # تحديث سجل التقدم اليومي
        update_daily_nutrition(user_id, date)

        return meal
    except Exception as e:
        session.rollback()
        logger.error(f"خطأ في إضافة الوجبة: {e}")
        raise
    finally:
        session.close()


def get_meals_for_day(user_id: int, target_date: date = None) -> List[Meal]:
    """الحصول على الوجبات ليوم معين"""
    session = Session()
    try:
        if target_date is None:
            target_date = date.today()

        meals = session.query(Meal).filter(
            and_(
                Meal.user_id == user_id,
                Meal.date == target_date
            )
        ).order_by(Meal.meal_type).all()
        return meals
    finally:
        session.close()


def get_meals_summary(user_id: int, target_date: date = None) -> dict:
    """الحصول على ملخص الوجبات ليوم معين"""
    meals = get_meals_for_day(user_id, target_date)
    return {
        "total_calories": sum(m.calories for m in meals),
        "total_protein": sum(m.protein for m in meals),
        "total_carbs": sum(m.carbs for m in meals),
        "total_fats": sum(m.fats for m in meals),
        "meal_count": len(meals)
    }


def delete_meal(meal_id: int, user_id: int) -> bool:
    """حذف وجبة"""
    session = Session()
    try:
        meal = session.query(Meal).filter(
            and_(
                Meal.id == meal_id,
                Meal.user_id == user_id
            )
        ).first()

        if meal:
            meal_date = meal.date
            session.delete(meal)
            session.commit()

            # تحديث سجل التقدم اليومي
            update_daily_nutrition(user_id, meal_date)
            return True
        return False
    except Exception as e:
        session.rollback()
        logger.error(f"خطأ في حذف الوجبة: {e}")
        return False
    finally:
        session.close()


def update_daily_nutrition(user_id: int, target_date: date):
    """تحديث سجل التغذية اليومي"""
    summary = get_meals_summary(user_id, target_date)

    session = Session()
    try:
        progress = session.query(DailyProgress).filter(
            and_(
                DailyProgress.user_id == user_id,
                DailyProgress.date == target_date
            )
        ).first()

        if progress:
            progress.calories = summary["total_calories"]
            progress.protein = summary["total_protein"]
            progress.carbs = summary["total_carbs"]
            progress.fats = summary["total_fats"]
            session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"خطأ في تحديث التغذية اليومية: {e}")
    finally:
        session.close()


# ==================== وظائف التمارين ====================

def add_exercise(exercise_data: dict) -> Exercise:
    """إضافة تمرين جديد لقاعدة البيانات"""
    session = Session()
    try:
        # تصفيه الحقول لتتوافق مع نموذج SQLAlchemy
        valid_fields = {
            'name_ar', 'name_en', 'muscle_group', 'equipment',
            'difficulty', 'description', 'instructions',
            'video_url', 'image_url', 'calories_per_minute'
        }
        filtered_data = {k: v for k, v in exercise_data.items() if k in valid_fields}

        exercise = Exercise(**filtered_data)
        session.add(exercise)
        session.commit()
        session.refresh(exercise)
        return exercise
    except Exception as e:
        session.rollback()
        logger.error(f"خطأ في إضافة التمرين: {e}")
        raise
    finally:
        session.close()


def get_exercises_by_muscle(muscle_group: str) -> List[Exercise]:
    """الحصول على التمارين حسب مجموعة العضلات"""
    session = Session()
    try:
        exercises = session.query(Exercise).filter(
            Exercise.muscle_group == muscle_group
        ).all()
        return exercises
    finally:
        session.close()


def get_all_exercises() -> List[Exercise]:
    """الحصول على جميع التمارين"""
    session = Session()
    try:
        return session.query(Exercise).all()
    finally:
        session.close()


def log_workout(
    user_id: int,
    exercise_id: int,
    sets: int,
    reps: int,
    weight: float = None,
    duration: int = None,
    rest_seconds: int = 90,
    date: date = None,
    notes: str = None,
    completed: bool = True
) -> Workout:
    """تسجيل تمرين منفذ"""
    session = Session()
    try:
        if date is None:
            date = date.today()

        workout = Workout(
            user_id=user_id,
            date=date,
            exercise_id=exercise_id,
            sets=sets,
            reps=reps,
            weight=weight,
            duration=duration,
            rest_seconds=rest_seconds,
            notes=notes,
            completed=completed
        )
        session.add(workout)
        session.commit()
        session.refresh(workout)
        return workout
    except Exception as e:
        session.rollback()
        logger.error(f"خطأ في تسجيل التمرين: {e}")
        raise
    finally:
        session.close()


def get_workouts_for_day(user_id: int, target_date: date = None) -> List[Workout]:
    """الحصول على التمارين ليوم معين"""
    session = Session()
    try:
        if target_date is None:
            target_date = date.today()

        workouts = session.query(Workout).filter(
            and_(
                Workout.user_id == user_id,
                Workout.date == target_date
            )
        ).all()
        return workouts
    finally:
        session.close()


def get_workout_history(user_id: int, limit: int = 30) -> List[Workout]:
    """الحصول على تاريخ التمارين"""
    session = Session()
    try:
        workouts = session.query(Workout).filter(
            Workout.user_id == user_id
        ).order_by(Workout.date.desc()).limit(limit).all()
        return workouts
    finally:
        session.close()


# ==================== وظائف الإعدادات ====================

def get_user_settings(user_id: int) -> Optional[Settings]:
    """الحصول على إعدادات المستخدم"""
    session = Session()
    try:
        settings = session.query(Settings).filter(
            Settings.user_id == user_id
        ).first()
        return settings
    finally:
        session.close()


def update_user_settings(user_id: int, **kwargs) -> Optional[Settings]:
    """تحديث إعدادات المستخدم"""
    session = Session()
    try:
        settings = session.query(Settings).filter(
            Settings.user_id == user_id
        ).first()

        if not settings:
            settings = Settings(user_id=user_id)
            session.add(settings)

        for key, value in kwargs.items():
            if hasattr(settings, key):
                setattr(settings, key, value)

        session.commit()
        session.refresh(settings)
        return settings
    except Exception as e:
        session.rollback()
        logger.error(f"خطأ في تحديث الإعدادات: {e}")
        raise
    finally:
        session.close()


# ==================== وظائف الإحصائيات ====================

def get_user_stats(user_id: int) -> UserStats:
    """الحصول على إحصائيات المستخدم"""
    session = Session()
    try:
        # إجمالي التمارين
        total_workouts = session.query(func.count(Workout.id)).filter(
            Workout.user_id == user_id,
            Workout.completed == True
        ).scalar() or 0

        # إجمالي الوجبات
        total_meals = session.query(func.count(Meal.id)).filter(
            Meal.user_id == user_id
        ).scalar() or 0

        # متوسط السعرات والمغذيات
        avg_stats = session.query(
            func.avg(DailyProgress.calories),
            func.avg(DailyProgress.protein),
            func.avg(DailyProgress.water),
            func.avg(DailyProgress.sleep_hours)
        ).filter(DailyProgress.user_id == user_id).first()

        # حساب سلسلة الالتزام
        current_streak, longest_streak = calculate_streaks(user_id)

        # حساب تغير الوزن
        weight_change, weight_change_percent = calculate_weight_change(user_id)

        # درجة الالتزام
        consistency_score = calculate_consistency_score(user_id)

        return UserStats(
            total_workouts=total_workouts,
            total_meals=total_meals,
            avg_calories=avg_stats[0] or 0,
            avg_protein=avg_stats[1] or 0,
            avg_water=avg_stats[2] or 0,
            avg_sleep=avg_stats[3] or 0,
            current_streak=current_streak,
            longest_streak=longest_streak,
            weight_change=weight_change,
            weight_change_percent=weight_change_percent,
            consistency_score=consistency_score
        )
    finally:
        session.close()


def calculate_streaks(user_id: int) -> Tuple[int, int]:
    """حساب سلسلة الالتزام (أيام متتالية)"""
    session = Session()
    try:
        # الحصول على تاريخ البدء
        first_workout = session.query(DailyProgress).filter(
            DailyProgress.user_id == user_id
        ).order_by(DailyProgress.date).first()

        if not first_workout:
            return 0, 0

        # حساب السلسلة الحالية
        current_streak = 0
        today = date.today()

        # البحث عن آخر يوم بدون نشاط
        check_date = today
        has_activity = True

        while has_activity:
            progress = session.query(DailyProgress).filter(
                and_(
                    DailyProgress.user_id == user_id,
                    DailyProgress.date == check_date
                )
            ).first()

            if progress and (progress.calories > 0 or progress.weight):
                current_streak += 1
                check_date -= timedelta(days=1)
            else:
                has_activity = False

        # حساب أطول سلسلة
        all_progress = session.query(DailyProgress.date).filter(
            DailyProgress.user_id == user_id
        ).order_by(DailyProgress.date).all()

        longest_streak = 0
        current_count = 0
        prev_date = None

        for p in all_progress:
            if prev_date is None or (p.date - prev_date).days == 1:
                current_count += 1
            else:
                current_count = 1

            longest_streak = max(longest_streak, current_count)
            prev_date = p.date

        return current_streak, longest_streak
    finally:
        session.close()


def calculate_weight_change(user_id: int) -> Tuple[float, float]:
    """حساب تغير الوزن"""
    session = Session()
    try:
        # الحصول على أول وآخر وزن مسجل
        first_weight = session.query(DailyProgress).filter(
            and_(
                DailyProgress.user_id == user_id,
                DailyProgress.weight.isnot(None)
            )
        ).order_by(DailyProgress.date).first()

        last_weight = session.query(DailyProgress).filter(
            and_(
                DailyProgress.user_id == user_id,
                DailyProgress.weight.isnot(None)
            )
        ).order_by(DailyProgress.date.desc()).first()

        if not first_weight or not last_weight:
            return 0.0, 0.0

        change = last_weight.weight - first_weight.weight
        change_percent = (change / first_weight.weight) * 100 if first_weight.weight else 0

        return round(change, 2), round(change_percent, 2)
    finally:
        session.close()


def calculate_consistency_score(user_id: int) -> float:
    """حساب درجة الالتزام"""
    session = Session()
    try:
        # حساب الالتزام بالتمارين
        thirty_days_ago = date.today() - timedelta(days=30)
        workouts = session.query(Workout).filter(
            and_(
                Workout.user_id == user_id,
                Workout.date >= thirty_days_ago,
                Workout.completed == True
            )
        ).all()

        # الحصول على أيام التمرين المبرمجة
        user = get_user_by_telegram_id(user_id)
        if not user:
            return 0

        expected_workouts = 30 * user.workout_days / 7
        actual_workouts = len(workouts)

        score = (actual_workouts / expected_workouts) * 100 if expected_workouts > 0 else 0
        return min(round(score, 1), 100)
    finally:
        session.close()


# ==================== وظائف البيانات الضخمة ====================

def get_weekly_report(user_id: int) -> dict:
    """الحصول على التقرير الأسبوعي"""
    session = Session()
    try:
        week_ago = date.today() - timedelta(days=7)

        # التقدم الأسبوعي
        weekly_progress = session.query(DailyProgress).filter(
            and_(
                DailyProgress.user_id == user_id,
                DailyProgress.date >= week_ago
            )
        ).all()

        # الوجبات
        weekly_meals = session.query(Meal).filter(
            and_(
                Meal.user_id == user_id,
                Meal.date >= week_ago
            )
        ).all()

        # التمارين
        weekly_workouts = session.query(Workout).filter(
            and_(
                Workout.user_id == user_id,
                Workout.date >= week_ago,
                Workout.completed == True
            )
        ).all()

        # الوزن
        weights = [p.weight for p in weekly_progress if p.weight]
        weight_start = weights[0] if weights else None
        weight_end = weights[-1] if weights else None
        weight_change = weight_end - weight_start if weight_start and weight_end else 0

        return {
            "start_date": week_ago,
            "end_date": date.today(),
            "days_logged": len(weekly_progress),
            "total_meals": len(weekly_meals),
            "total_workouts": len(weekly_workouts),
            "total_calories": sum(m.calories for m in weekly_meals),
            "total_protein": sum(m.protein for m in weekly_meals),
            "avg_daily_calories": sum(m.calories for m in weekly_meals) / 7 if weekly_meals else 0,
            "avg_daily_protein": sum(m.protein for m in weekly_meals) / 7 if weekly_meals else 0,
            "avg_water": sum(p.water for p in weekly_progress) / len(weekly_progress) if weekly_progress else 0,
            "avg_sleep": sum(p.sleep_hours for p in weekly_progress) / len(weekly_progress) if weekly_progress else 0,
            "weight_start": weight_start,
            "weight_end": weight_end,
            "weight_change": round(weight_change, 2),
            "workouts_by_day": [(w.date, w.exercise_id) for w in weekly_workouts]
        }
    finally:
        session.close()


# ==================== الوظائف الإدارية ====================

def get_all_users() -> List[User]:
    """الحصول على جميع المستخدمين"""
    session = Session()
    try:
        return session.query(User).all()
    finally:
        session.close()


def get_active_users(days: int = 7) -> List[User]:
    """الحصول على المستخدمين النشطين"""
    session = Session()
    try:
        active_date = date.today() - timedelta(days=days)
        active_users = session.query(User).join(DailyProgress).filter(
            DailyProgress.date >= active_date
        ).distinct().all()
        return active_users
    finally:
        session.close()


def init_database():
    """تهيئة قاعدة البيانات"""
    Base.metadata.create_all(engine)
    logger.info("تم إنشاء قاعدة البيانات بنجاح")

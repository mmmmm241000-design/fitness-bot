"""
خدمات التغذية - FitCoach Bot
"""
from datetime import date, timedelta
from typing import List, Dict, Optional, Tuple
import logging

from bot.models import User, Meal, DailyProgress, Session
from bot.database import get_meals_summary, get_user_by_telegram_id
from bot.config import nutrition_config

logger = logging.getLogger(__name__)


class NutritionService:
    """خدمة التغذية"""

    # قاعدة بيانات الوجبات الشائعة (لكل 100 غرام)
    COMMON_FOODS = {
        # البروتينات
        "صدر دجاج": {"calories": 165, "protein": 31, "carbs": 0, "fats": 3.6},
        "لحم بقري": {"calories": 250, "protein": 26, "carbs": 0, "fats": 15},
        "سمك تونا": {"calories": 130, "protein": 29, "carbs": 0, "fats": 1},
        "بيض": {"calories": 155, "protein": 13, "carbs": 1.1, "fats": 11},
        "بروتين مصل اللبن": {"calories": 120, "protein": 24, "carbs": 3, "fats": 1},
        "جبنة قcottage": {"calories": 98, "protein": 11, "carbs": 3.4, "fats": 4.3},

        # الكربوهيدرات
        "أرز بني": {"calories": 112, "protein": 2.6, "carbs": 23.5, "fats": 0.9},
        "أرز أبيض": {"calories": 130, "protein": 2.7, "carbs": 28, "fats": 0.3},
        "بطاطا": {"calories": 77, "protein": 2, "carbs": 17, "fats": 0.1},
        "معكرونة": {"calories": 131, "protein": 5, "carbs": 25, "fats": 1.1},
        "خبز أسمر": {"calories": 247, "protein": 13, "carbs": 41, "fats": 3.4},

        # الدهون الصحية
        "أفوكادو": {"calories": 160, "protein": 2, "carbs": 9, "fats": 15},
        "زيت زيتون": {"calories": 884, "protein": 0, "carbs": 0, "fats": 100},
        "مكسرات": {"calories": 607, "protein": 20, "carbs": 15, "fats": 54},
        "زبدة فول سوداني": {"calories": 588, "protein": 25, "carbs": 20, "fats": 50},

        # الخضروات
        "بروكلي": {"calories": 34, "protein": 2.8, "carbs": 7, "fats": 0.4},
        "سبانخ": {"calories": 23, "protein": 2.9, "carbs": 3.6, "fats": 0.4},
        "جزر": {"calories": 41, "protein": 0.9, "carbs": 10, "fats": 0.2},

        # الفواكه
        "موز": {"calories": 89, "protein": 1.1, "carbs": 23, "fats": 0.3},
        "تفاح": {"calories": 52, "protein": 0.3, "carbs": 14, "fats": 0.2},
        "برتقالي": {"calories": 47, "protein": 0.9, "carbs": 12, "fats": 0.1},
    }

    # وجبات جاهزة مقترحة
    MEAL_PLANS = {
        "bulking": {
            "breakfast": [
                {"name": "4 بيضات + شوفان بالموز", "calories": 650, "protein": 38, "carbs": 75, "fats": 22},
                {"name": "سموذي البروتين", "calories": 400, "protein": 35, "carbs": 45, "fats": 8},
            ],
            "lunch": [
                {"name": "صدر دجاج + أرز + خضار", "calories": 650, "protein": 55, "carbs": 70, "fats": 12},
                {"name": "لحم بقري + بطاطا", "calories": 700, "protein": 50, "carbs": 65, "fats": 22},
            ],
            "dinner": [
                {"name": "سمك + أرز + سلطة", "calories": 550, "protein": 45, "carbs": 60, "fats": 12},
                {"name": "معكرونة بلحم", "calories": 600, "protein": 40, "carbs": 75, "fats": 15},
            ],
            "snack": [
                {"name": "موز + زبدة فول سوداني", "calories": 350, "protein": 12, "carbs": 45, "fats": 18},
                {"name": "كottage + مكسرات", "calories": 300, "protein": 22, "carbs": 10, "fats": 20},
            ]
        },
        "recomp": {
            "breakfast": [
                {"name": "بيض + شوفان + فواكه", "calories": 450, "protein": 28, "carbs": 50, "fats": 14},
                {"name": "زبادي يوناني + موز + مكسرات", "calories": 380, "protein": 25, "carbs": 40, "fats": 12},
            ],
            "lunch": [
                {"name": "صدر دجاج + أرز بني + خضار", "calories": 500, "protein": 50, "carbs": 45, "fats": 10},
                {"name": "سمك + بطاطا مشوية + سلطة", "calories": 480, "protein": 45, "carbs": 40, "fats": 12},
            ],
            "dinner": [
                {"name": "لحم مفروم + خضار + أرز", "calories": 520, "protein": 45, "carbs": 42, "fats": 15},
                {"name": "دجاج مشوي + بروكلي + معكرونة", "calories": 490, "protein": 48, "carbs": 40, "fats": 10},
            ],
            "snack": [
                {"name": "بروتين شيك + موز", "calories": 280, "protein": 28, "carbs": 30, "fats": 4},
                {"name": "جبن قريش + مكسرات", "calories": 250, "protein": 20, "carbs": 8, "fats": 16},
            ]
        },
        "cutting": {
            "breakfast": [
                {"name": "زبادي يوناني + توت", "calories": 200, "protein": 20, "carbs": 15, "fats": 5},
            ],
            "lunch": [
                {"name": "صدر دجاج مشوي + سلطة", "calories": 350, "protein": 50, "carbs": 12, "fats": 10},
                {"name": "تونا + سلطة خضراء", "calories": 300, "protein": 45, "carbs": 8, "fats": 8},
            ],
            "dinner": [
                {"name": "سمك مشوي + بروكلي", "calories": 320, "protein": 45, "carbs": 10, "fats": 10},
                {"name": "صدر ديك رومي + خضار", "calories": 300, "protein": 48, "carbs": 8, "fats": 8},
            ],
            "snack": [
                {"name": "بروتين شيك", "calories": 150, "protein": 30, "carbs": 5, "fats": 2},
                {"name": "جبن قcottage + خضار", "calories": 180, "protein": 20, "carbs": 8, "fats": 8},
            ]
        }
    }

    @staticmethod
    def calculate_food_nutrition(food_name: str, grams: float) -> Dict:
        """حساب القيم الغذائية لطعام"""
        food = NutritionService.COMMON_FOODS.get(food_name)
        if not food:
            return None

        multiplier = grams / 100
        return {
            "name": food_name,
            "grams": grams,
            "calories": round(food["calories"] * multiplier),
            "protein": round(food["protein"] * multiplier, 1),
            "carbs": round(food["carbs"] * multiplier, 1),
            "fats": round(food["fats"] * multiplier, 1)
        }

    @staticmethod
    def search_foods(query: str) -> List[Dict]:
        """البحث عن أطعمة"""
        results = []
        query_lower = query.lower()

        for name, data in NutritionService.COMMON_FOODS.items():
            if query_lower in name.lower():
                results.append({
                    "name": name,
                    "calories_100g": data["calories"],
                    "protein_100g": data["protein"],
                    "carbs_100g": data["carbs"],
                    "fats_100g": data["fats"]
                })

        return results

    @staticmethod
    def get_meal_suggestion(goal: str, meal_type: str, budget: str = "medium") -> List[Dict]:
        """الحصول على اقتراحات وجبات"""
        goal_plans = NutritionService.MEAL_PLANS.get(goal, NutritionService.MEAL_PLANS["bulking"])
        meals = goal_plans.get(meal_type, goal_plans["breakfast"])

        # تصفية حسب الميزانية
        if budget == "low":
            return [m for m in meals if m["calories"] < 400]
        elif budget == "high":
            return meals
        else:
            return meals

    @staticmethod
    def get_daily_targets(user: User) -> Dict:
        """الحصول على الأهداف الغذائية اليومية للمستخدم"""
        targets = user.get_nutrition_targets()
        return {
            "calories": round(targets["calories"]),
            "protein": round(targets["protein"], 1),
            "carbs": round(targets["carbs"], 1),
            "fats": round(targets["fats"], 1)
        }

    @staticmethod
    def calculate_progress(user_id: int, target_date: date = None) -> Dict:
        """حساب نسبة الإنجاز"""
        if target_date is None:
            target_date = date.today()

        # الحصول على ملخص الوجبات
        summary = get_meals_summary(user_id, target_date)

        # الحصول على المستخدم والأهداف
        session = Session()
        user = session.query(User).filter(User.user_id == user_id).first()
        session.close()

        if not user:
            return None

        targets = NutritionService.get_daily_targets(user)

        # حساب النسب المئوية
        return {
            "date": target_date,
            "consumed": {
                "calories": summary["total_calories"],
                "protein": summary["total_protein"],
                "carbs": summary["total_carbs"],
                "fats": summary["total_fats"]
            },
            "targets": targets,
            "progress": {
                "calories": round(summary["total_calories"] / targets["calories"] * 100, 1) if targets["calories"] > 0 else 0,
                "protein": round(summary["total_protein"] / targets["protein"] * 100, 1) if targets["protein"] > 0 else 0,
                "carbs": round(summary["total_carbs"] / targets["carbs"] * 100, 1) if targets["carbs"] > 0 else 0,
                "fats": round(summary["total_fats"] / targets["fats"] * 100, 1) if targets["fats"] > 0 else 0
            }
        }

    @staticmethod
    def generate_nutrition_summary_text(progress: Dict) -> str:
        """إنشاء نص ملخص التغذية"""
        p = progress["progress"]
        c = progress["consumed"]
        t = progress["targets"]

        text = "📊 <b>ملخص التغذية</b>\n\n"
        text += "━━━━━━━━━━━━━━━━\n"

        # السعرات
        cal_status = "🟢" if p["calories"] >= 90 else "🟡" if p["calories"] >= 70 else "🔴"
        text += f"{cal_status} <b>السعرات:</b> {c['calories']} / {t['calories']} سعرة\n"
        text += f"   ▪️ {p['calories']}% من الهدف\n\n"

        # البروتين
        protein_status = "🟢" if p["protein"] >= 90 else "🟡" if p["protein"] >= 70 else "🔴"
        text += f"{protein_status} <b>البروتين:</b> {c['protein']}غ / {t['protein']}غ\n"
        text += f"   ▪️ {p['protein']}% من الهدف\n\n"

        # الكربوهيدرات
        carbs_status = "🟢" if p["carbs"] >= 80 else "🟡" if p["carbs"] >= 60 else "🔴"
        text += f"{carbs_status} <b>الكربوهيدرات:</b> {c['carbs']}غ / {t['carbs']}غ\n"
        text += f"   ▪️ {p['carbs']}% من الهدف\n\n"

        # الدهون
        fats_status = "🟢" if p["fats"] >= 80 else "🟡" if p["fats"] >= 60 else "🔴"
        text += f"{fats_status} <b>الدهون:</b> {c['fats']}غ / {t['fats']}غ\n"
        text += f"   ▪️ {p['fats']}% من الهدف\n"

        text += "━━━━━━━━━━━━━━━━"

        return text

    @staticmethod
    def get_budget_alternatives(high_cal_food: str) -> List[Dict]:
        """الحصول على بدائل رخيصة"""
        alternatives = {
            "صدر دجاج": [
                {"name": "بيض (6 حبات)", "calories": 450, "protein": 36, "price": "اقتصادي"},
                {"name": "بروتين نباتي + حبوب", "calories": 400, "protein": 35, "price": "اقتصادي"}
            ],
            "لحم بقري": [
                {"name": "دجاج + بيض", "calories": 400, "protein": 45, "price": "اقتصادي"},
                {"name": "سمك معلب + أرز", "calories": 380, "protein": 35, "price": "اقتصادي"}
            ]
        }
        return alternatives.get(high_cal_food, [])

    @staticmethod
    def suggest_meal_adjustment(user_id: int, days: int = 7) -> Optional[str]:
        """اقتراح تعديل على النظام الغذائي"""
        session = Session()

        # تحليل متوسط الاستهلاك خلال الأيام الأخيرة
        week_ago = date.today() - timedelta(days=days)

        meals = session.query(Meal).filter(
            Meal.user_id == user_id,
            Meal.date >= week_ago
        ).all()

        if len(meals) < days:
            session.close()
            return None

        avg_calories = sum(m.calories for m in meals) / len(meals)

        user = session.query(User).filter(User.user_id == user_id).first()
        session.close()

        if not user:
            return None

        target_calories = user.get_nutrition_targets()["calories"]

        # تحليل والحصول على اقتراح
        if avg_calories < target_calories * 0.8:
            deficit = target_calories - avg_calories
            return f"⚠️ <b>تنبيه:</b>\nلاحظت أن استهلاكك أقل من الهدف بـ {round(deficit)} سعرة.\n\n" \
                   f"💡 اقتراحي: أضف {round(deficit/2)} سعرة عن طريق:\n" \
                   f"• حصة إضافية من البروتين\n• وجبة خفيفة غنية بالكربوهيدرات"
        elif avg_calories > target_calories * 1.1:
            surplus = avg_calories - target_calories
            return f"⚠️ <b>تنبيه:</b>\nاستهلاكك أعلى من الهدف بـ {round(surplus)} سعرة.\n\n" \
                   f"💡 اقتراحي: قلل {round(surplus/2)} سعرة عن طريق:\n" \
                   f"• تقليل الزيوت\n• تقليل الوجبات الخفيفة"
        else:
            return "✅ أداء ممتاز! استهلاكك قريب جداً من الهدف.\nاستمر على هذا النحو!"

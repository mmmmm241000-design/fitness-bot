"""
خدمة التحليلات والذكاء التكيفي - FitCoach Bot
"""
from datetime import date, timedelta
from typing import Dict, List, Optional, Tuple
import logging

from bot.models import User, DailyProgress, Meal, Workout, Session
from bot.database import (
    get_progress_range, get_meals_summary, get_user_by_telegram_id,
    get_workout_history
)
from bot.config import config, nutrition_config, workout_config
from bot.data.exercises import get_exercise_by_id

logger = logging.getLogger(__name__)


class AdaptiveIntelligence:
    """نظام الذكاء التكيفي"""

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.session = Session()
        self.user = self.session.query(User).filter(
            User.user_id == user_id
        ).first()

    def analyze_progress(self, days: int = 28) -> Dict:
        """
        تحليل التقدم خلال فترة زمنية
        يرجع توصيات ذكية بناءً على البيانات
        """
        if not self.user:
            return {"status": "error", "message": "المستخدم غير موجود"}

        # تحليل الوزن
        weight_analysis = self._analyze_weight(days)

        # تحليل التغذية
        nutrition_analysis = self._analyze_nutrition(days)

        # تحليل التمارين
        workout_analysis = self._analyze_workouts(days)

        # إنشاء التوصيات
        recommendations = self._generate_recommendations(
            weight_analysis,
            nutrition_analysis,
            workout_analysis
        )

        return {
            "status": "success",
            "weight_analysis": weight_analysis,
            "nutrition_analysis": nutrition_analysis,
            "workout_analysis": workout_analysis,
            "recommendations": recommendations
        }

    def _analyze_weight(self, days: int) -> Dict:
        """تحليل تغير الوزن"""
        progress_list = get_progress_range(self.user_id, days)
        weights = [p.weight for p in progress_list if p.weight]

        if len(weights) < 2:
            return {
                "trend": "insufficient_data",
                "change": 0,
                "avg_weekly_change": 0,
                "status": "need_more_data"
            }

        first_weight = weights[0]
        last_weight = weights[-1]
        total_change = last_weight - first_weight

        # حساب التغير الأسبوعي
        weeks = len(weights) / 7
        avg_weekly_change = total_change / weeks if weeks > 0 else 0

        # تحديد الاتجاه
        if avg_weekly_change > 0.2:
            trend = "gaining"
        elif avg_weekly_change < -0.2:
            trend = "losing"
        else:
            trend = "stable"

        # حساب الانحراف المعياري
        import statistics
        std_dev = statistics.stdev(weights) if len(weights) > 1 else 0

        return {
            "first_weight": first_weight,
            "last_weight": last_weight,
            "total_change": round(total_change, 2),
            "avg_weekly_change": round(avg_weekly_change, 2),
            "std_dev": round(std_dev, 2),
            "trend": trend,
            "data_points": len(weights)
        }

    def _analyze_nutrition(self, days: int) -> Dict:
        """تحليل التغذية"""
        week_ago = date.today() - timedelta(days=days)
        meals = self.session.query(Meal).filter(
            Meal.user_id == self.user_id,
            Meal.date >= week_ago
        ).all()

        if not meals:
            return {
                "avg_daily_calories": 0,
                "avg_daily_protein": 0,
                "adherence": 0,
                "status": "no_data"
            }

        # حساب المتوسطات
        avg_calories = sum(m.calories for m in meals) / days
        avg_protein = sum(m.protein for m in meals) / days

        # الحصول على الهدف
        try:
            targets = self.user.get_nutrition_targets()
            target_calories = targets["calories"]
            target_protein = targets["protein"]
        except:
            target_calories = 2500
            target_protein = 150

        # حساب نسبة الالتزام
        adherence_calories = min(100, (avg_calories / target_calories * 100)) if target_calories > 0 else 0
        adherence_protein = min(100, (avg_protein / target_protein * 100)) if target_protein > 0 else 0

        return {
            "avg_daily_calories": round(avg_calories),
            "avg_daily_protein": round(avg_protein, 1),
            "target_calories": round(target_calories),
            "target_protein": round(target_protein),
            "adherence_calories": round(adherence_calories, 1),
            "adherence_protein": round(adherence_protein, 1),
            "status": "good" if adherence_calories > 80 else "needs_improvement"
        }

    def _analyze_workouts(self, days: int) -> Dict:
        """تحليل التمارين"""
        week_ago = date.today() - timedelta(days=days)
        workouts = self.session.query(Workout).filter(
            Workout.user_id == self.user_id,
            Workout.date >= week_ago,
            Workout.completed == True
        ).all()

        if not workouts:
            return {
                "total_workouts": 0,
                "expected_workouts": days // 7 * self.user.workout_days,
                "completion_rate": 0,
                "status": "no_workouts"
            }

        # تحليل مجموعات العضلات
        muscle_groups = {}
        for w in workouts:
            ex = get_exercise_by_id(w.exercise_id)
            if ex:
                mg = ex["muscle_group"]
                muscle_groups[mg] = muscle_groups.get(mg, 0) + 1

        expected = days // 7 * self.user.workout_days
        completion_rate = len(workouts) / expected * 100 if expected > 0 else 0

        return {
            "total_workouts": len(workouts),
            "expected_workouts": expected,
            "completion_rate": round(completion_rate, 1),
            "muscle_groups": muscle_groups,
            "avg_sets": sum(w.sets for w in workouts) / len(workouts),
            "status": "good" if completion_rate > 70 else "needs_improvement"
        }

    def _generate_recommendations(
        self,
        weight: Dict,
        nutrition: Dict,
        workouts: Dict
    ) -> List[Dict]:
        """إنشاء توصيات ذكية"""
        recommendations = []

        # تحليل الوزن والتوصية
        if weight["status"] == "need_more_data":
            recommendations.append({
                "type": "info",
                "priority": "high",
                "message": "📊 نحتاج المزيد من البيانات.\nسجل وزنك يومياً للحصول على تحليل دقيق."
            })
        else:
            # التغير في الوزن
            if self.user.goal == "bulking":
                if weight["trend"] == "stable":
                    recommendations.append({
                        "type": "warning",
                        "priority": "high",
                        "message": "⚠️ وزنك ثابت!\nلتحقيق هدف الضخامة، زد من السعرات بمقدار 250-500 سعرة."
                    })
                elif weight["trend"] == "losing":
                    recommendations.append({
                        "type": "warning",
                        "priority": "critical",
                        "message": "🔴 وزنّك ينخفض!\nزد السعرات فوراً (+500 سعرة) لتجنب حرق العضلات."
                    })
                elif weight["avg_weekly_change"] > 0.5:
                    recommendations.append({
                        "type": "success",
                        "priority": "medium",
                        "message": "✅ ممتاز! تكتسب وزناً صحياً.\nالاستمرار على هذا المنوال."
                    })

            elif self.user.goal == "cutting":
                if weight["trend"] == "gaining":
                    recommendations.append({
                        "type": "warning",
                        "priority": "high",
                        "message": "⚠️ وزنك يزداد!\nقلل السعرات بمقدار 250-500 سعرة."
                    })
                elif weight["avg_weekly_change"] > 0.7:
                    recommendations.append({
                        "type": "warning",
                        "priority": "critical",
                        "message": "🔴 فقدان الوزن سريع جداً!\nأضف 200-300 سعرة لتجنب حرق العضلات."
                    })
                elif weight["avg_weekly_change"] >= 0.3 and weight["avg_weekly_change"] <= 0.7:
                    recommendations.append({
                        "type": "success",
                        "priority": "medium",
                        "message": "✅ تنشيف ممتاز!\nفقدان 0.5-1 كجم أسبوعياً مثالي."
                    })

        # تحليل التغذية
        if nutrition["status"] != "no_data":
            if nutrition["adherence_protein"] < 80:
                recommendations.append({
                    "type": "warning",
                    "priority": "high",
                    "message": f"🥩 بروتينك منخفض!\nهدفك: {nutrition['target_protein']}غ\n"
                              f"استهلاكك: {nutrition['avg_daily_protein']}غ\n"
                              f"أضف مصادر بروتين عالية."
                })

            if nutrition["adherence_calories"] < 70:
                recommendations.append({
                    "type": "warning",
                    "priority": "medium",
                    "message": "🍽️ سعراتك منخفضة!\nتأكد من تناول وجبات كافية."
                })

        # تحليل التمارين
        if workouts["status"] != "no_workouts":
            if workouts["completion_rate"] < 50:
                recommendations.append({
                    "type": "warning",
                    "priority": "high",
                    "message": f"🏋️ معدل تمارينك منخفض!\n"
                              f"أنجزت: {workouts['total_workouts']}\n"
                              f"المتوقع: {workouts['expected_workouts']}\n"
                              f"حاول الالتزام بجدولك."
                })

        # توصيات عامة
        if not recommendations:
            recommendations.append({
                "type": "success",
                "priority": "low",
                "message": "🎉 كل شيء يسير بشكل ممتاز!\nاستمر على هذا المنوال."
            })

        return recommendations

    def get_daily_motivation(self) -> str:
        """رسالة تحفيزية يومية"""
        import random

        messages = [
            "💪 اليوم هو يوم جديد للتقدم!",
            "🔥 كل تمرين يقربك من هدفك!",
            "🏋️ لا تتوقف، النتائج قادمة!",
            "⭐ أنت أقوى مما تظن!",
            "🎯 الهدف قريب، استمر!",
            "💯 بذل قصارى جهدك اليوم!",
            "🚀 الطريق إلى النجاح يبدأ بخطوة واحدة!",
            "🏆 أنت في منتصف رحلتك، لا تستسلم!",
            "🌟 كل يوم هو فرصة جديدة!",
            "🔄 التغيير يبدأ من داخلك!"
        ]

        return random.choice(messages)

    def check_streak_status(self) -> Tuple[bool, str]:
        """التحقق من حالة السلسلة"""
        from bot.database import calculate_streaks

        current, longest = calculate_streaks(self.user_id)

        if current >= 7:
            return True, f"🏆 سلسلة {current} يوم! مذهل!"
        elif current >= 3:
            return True, f"🔥 {current} أيام متتالية! مستمر!"
        elif current > 0:
            return False, f"📅 {current} يوم، لا توقف الآن!"
        else:
            return False, "📅 ابدأ سلسلة جديدة اليوم!"

    def suggest_adjustments(self) -> List[Dict]:
        """اقتراح تعديلات على البرنامج"""
        suggestions = []

        try:
            # تحليل آخر 4 أسابيع
            analysis = self.analyze_progress(28)
            nutrition = analysis.get("nutrition_analysis", {})
            workouts = analysis.get("workout_analysis", {})
            weight = analysis.get("weight_analysis", {})

            # تعديل البروتين
            if nutrition.get("adherence_protein", 0) < 70:
                suggestions.append({
                    "category": "nutrition",
                    "action": "increase_protein",
                    "message": "زد من مصادر البروتين: بيض، دجاج، سمك، بروتين مصل اللبن"
                })

            # تعديل السعرات حسب الهدف
            if self.user.goal == "bulking":
                if nutrition.get("adherence_calories", 0) < 85:
                    suggestions.append({
                        "category": "nutrition",
                        "action": "increase_calories",
                        "message": "زد السعرات بمقدار 250-500 سعرة للضخامة"
                    })
            elif self.user.goal == "cutting":
                if nutrition.get("adherence_calories", 0) > 105:
                    suggestions.append({
                        "category": "nutrition",
                        "action": "decrease_calories",
                        "message": "قلل السعرات بمقدار 250 سعرة للتنشيف"
                    })

            # تعديل التمارين
            if workouts.get("completion_rate", 0) < 60:
                suggestions.append({
                    "category": "workout",
                    "action": "increase_frequency",
                    "message": "حاول الالتزام أكثر بجدول التمارين"
                })

        except Exception as e:
            logger.error(f"خطأ في اقتراح التعديلات: {e}")

        return suggestions

    def __del__(self):
        """إغلاق الجلسة"""
        try:
            self.session.close()
        except:
            pass


def get_adaptive_insights(user_id: int) -> Dict:
    """وظيفة مساعدة للحصول على التحليلات"""
    ai = AdaptiveIntelligence(user_id)
    return ai.analyze_progress()


def generate_weekly_summary(user_id: int) -> str:
    """إنشاء ملخص أسبوعي ذكي"""
    ai = AdaptiveIntelligence(user_id)
    analysis = ai.analyze_progress(7)

    if analysis["status"] != "success":
        return "❌ لا توجد بيانات كافية."

    recommendations = analysis.get("recommendations", [])
    weight = analysis.get("weight_analysis", {})
    nutrition = analysis.get("nutrition_analysis", {})
    workouts = analysis.get("workout_analysis", {})

    message = "📊 <b>ملخص الأسبوع الذكي</b>\n\n"
    message += "━━━━━━━━━━━━━━━━\n\n"

    # الوزن
    if weight.get("status") != "need_more_data":
        change = weight.get("total_change", 0)
        change_icon = "📈" if change > 0 else "📉" if change < 0 else "➡️"
        message += f"{change_icon} <b>الوزن:</b> {change:+.1f} كجم\n\n"

    # التغذية
    message += f"🍽️ <b>التغذية:</b>\n"
    message += f"   متوسط السعرات: {nutrition.get('avg_daily_calories', 0)}\n"
    message += f"   متوسط البروتين: {nutrition.get('avg_daily_protein', 0)}غ\n\n"

    # التمارين
    message += f"🏋️ <b>التمارين:</b>\n"
    message += f"   تمارين أنجزت: {workouts.get('total_workouts', 0)}\n"
    message += f"   معدل الإنجاز: {workouts.get('completion_rate', 0)}%\n\n"

    # أهم توصية
    if recommendations:
        top_rec = recommendations[0]
        message += f"💡 <b>التوصية:</b>\n{top_rec['message']}\n"

    message += "\n━━━━━━━━━━━━━━━━"

    return message

"""
معالجات الملف الشخصي - FitCoach Bot
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from bot.database import (
    get_user_by_telegram_id, update_user_profile, get_or_create_user
)
from bot.keyboards import (
    get_profile_menu_keyboard, get_back_to_main_keyboard,
    get_experience_level_keyboard, get_goal_type_keyboard,
    get_activity_level_keyboard, get_profile_edit_keyboard
)
from bot.models import User


PROFILE_VIEW_MESSAGE = """
👤 <b>ملفك الشخصي</b>

━━━━━━━━━━━━━━━━

📋 <b>البيانات الأساسية:</b>

🎂 العمر: {age} سنة
📏 الطول: {height} سم
⚖️ الوزن الحالي: {weight} كجم
📐 نسبة الدهون: {body_fat}%

━━━━━━━━━━━━━━━━

🎯 <b>الهدف:</b> {goal}

━━━━━━━━━━━━━━━━

⭐ <b>معلومات التمرين:</b>

مستوى الخبرة: {experience}
أيام التمرين: {workout_days} أيام/أسبوع
مستوى النشاط: {activity}

━━━━━━━━━━━━━━━━

📊 <b>إحصائياتك:</b>

🏋️ إجمالي التمارين: {total_workouts}
🍽️ إجمالي الوجبات: {total_meals}
🔥 سلسلة الالتزام: {streak} يوم

━━━━━━━━━━━━━━━━
"""

EDIT_PROFILE_WELCOME = """
✏️ <b>تعديل الملف الشخصي</b>

اختر الحقل الذي تريد تعديله:
"""

AGE_PROMPT = """
🎂 <b>أدخل عمرك:</b>

الرجاء إدخال عمرك بالأرقام (14-70 سنة)

مثال: <code>25</code>
"""

HEIGHT_PROMPT = """
📏 <b>أدخل طولك:</b>

الرجاء إدخال طولك بالسنتيمتر (140-220 سم)

مثال: <code>175</code>
"""

WEIGHT_PROMPT = """
⚖️ <b>أدخل وزنك:</b>

الرجاء إدخال وزنك بالكيلوغرام (30-200 كجم)

مثال: <code>75</code>
"""

BODYFAT_PROMPT = """
📐 <b>أدخل نسبة الدهون في جسمك:</b>

هذا اختياري. إذا كنت لا تعرف، يمكنك تخطي هذه الخطوة.

النطاق: 3% - 50%

مثال: <code>18</code>
"""

WORKOUT_DAYS_PROMPT = """
📅 <b>كم يوم تريد التمرين أسبوعياً؟</b>

اختر بين 1 إلى 7 أيام:

• 3 أيام: مناسب للمبتدئين
• 4-5 أيام: جيد للتقدم
• 6-7 أيام: للرياضيين المتقدمين
"""


async def profile_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض قائمة الملف الشخصي"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "👤 <b>قائمة الملف الشخصي</b>\n\nاختر ما تريد:",
        parse_mode="HTML",
        reply_markup=get_profile_menu_keyboard()
    )


async def profile_view_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض الملف الشخصي"""
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    db_user = get_user_by_telegram_id(user.id)

    if not db_user or not db_user.age:
        await query.edit_message_text(
            "❌ لم تقم بإنشاء ملف شخصي بعد.\n\nاضغط /start للبدء.",
            parse_mode="HTML"
        )
        return

    from bot.database import get_user_stats

    stats = get_user_stats(db_user.user_id)

    goal_names = {
        "bulking": "🔥 ضخامة عضلية",
        "cutting": "❄️ تنشيف",
        "recomp": "🔄 إعادة تركيب"
    }
    exp_names = {
        "beginner": "🌱 مبتدئ",
        "intermediate": "🏃 متوسط",
        "advanced": "💪 متقدم"
    }
    activity_names = {
        "sedentary": "🛋️ خامل",
        "light": "🚶 نشاط خفيف",
        "moderate": "🏃 نشاط متوسط",
        "active": "🔥 نشط جداً",
        "athlete": "🏆 رياضي محترف"
    }

    message = PROFILE_VIEW_MESSAGE.format(
        age=db_user.age or "غير محدد",
        height=db_user.height or "غير محدد",
        weight=db_user.weight or "غير محدد",
        body_fat=f"{db_user.body_fat}%" if db_user.body_fat else "غير محدد",
        goal=goal_names.get(db_user.goal, db_user.goal),
        experience=exp_names.get(db_user.experience_level, db_user.experience_level),
        workout_days=db_user.workout_days or 3,
        activity=activity_names.get(db_user.activity_level, db_user.activity_level),
        total_workouts=stats.total_workouts,
        total_meals=stats.total_meals,
        streak=stats.current_streak
    )

    await query.edit_message_text(
        message,
        parse_mode="HTML",
        reply_markup=get_profile_edit_keyboard()
    )


async def profile_edit_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تعديل الملف الشخصي"""
    query = update.callback_query
    await query.answer()

    edit_field = query.data.replace("edit_", "")

    prompts = {
        "age": AGE_PROMPT,
        "height": HEIGHT_PROMPT,
        "weight": WEIGHT_PROMPT,
        "bodyfat": BODYFAT_PROMPT,
        "workout_days": WORKOUT_DAYS_PROMPT
    }

    if edit_field in prompts:
        context.user_data["edit_field"] = edit_field
        await query.edit_message_text(
            prompts[edit_field],
            parse_mode="HTML"
        )


async def exp_level_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """اختيار مستوى الخبرة"""
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    db_user = get_user_by_telegram_id(user.id)

    if not db_user:
        return

    level = query.data.replace("exp_", "")
    level_names = {
        "beginner": "🌱 مبتدئ",
        "intermediate": "🏃 متوسط",
        "advanced": "💪 متقدم"
    }

    update_user_profile(db_user.user_id, experience_level=level)

    await query.edit_message_text(
        f"✅ تم تحديث مستوى الخبرة إلى: <b>{level_names[level]}</b>",
        parse_mode="HTML",
        reply_markup=get_back_to_main_keyboard()
    )


async def goal_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """اختيار الهدف"""
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    db_user = get_user_by_telegram_id(user.id)

    if not db_user:
        return

    goal = query.data.replace("goal_", "")
    goal_names = {
        "bulking": "🔥 ضخامة عضلية",
        "cutting": "❄️ تنشيف",
        "recomp": "🔄 إعادة تركيب"
    }

    update_user_profile(db_user.user_id, goal=goal)

    await query.edit_message_text(
        f"✅ تم تحديث الهدف إلى: <b>{goal_names[goal]}</b>",
        parse_mode="HTML",
        reply_markup=get_back_to_main_keyboard()
    )


async def activity_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """اختيار مستوى النشاط"""
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    db_user = get_user_by_telegram_id(user.id)

    if not db_user:
        return

    activity = query.data.replace("activity_", "")
    activity_names = {
        "sedentary": "🛋️ خامل",
        "light": "🚶 نشاط خفيف",
        "moderate": "🏃 نشاط متوسط",
        "active": "🔥 نشط جداً",
        "athlete": "🏆 رياضي محترف"
    }

    update_user_profile(db_user.user_id, activity_level=activity)

    await query.edit_message_text(
        f"✅ تم تحديث مستوى النشاط إلى: <b>{activity_names[activity]}</b>",
        parse_mode="HTML",
        reply_markup=get_back_to_main_keyboard()
    )


async def handle_profile_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة مدخلات الملف الشخصي"""
    text = update.message.text.strip()

    user = update.effective_user
    db_user = get_user_by_telegram_id(user.id)

    if not db_user:
        return

    # التحقق من وجود أمر تعديل
    edit_field = context.user_data.get("edit_field")

    if edit_field:
        try:
            if edit_field == "age":
                value = int(text)
                if 14 <= value <= 70:
                    update_user_profile(db_user.user_id, age=value)
                    await update.message.reply_text(
                        f"✅ تم تحديث العمر إلى: <b>{value}</b> سنة",
                        parse_mode="HTML"
                    )
                else:
                    await update.message.reply_text("❌ العمر يجب أن يكون بين 14 و 70 سنة")
                context.user_data.pop("edit_field", None)

            elif edit_field == "height":
                value = float(text)
                if 140 <= value <= 220:
                    update_user_profile(db_user.user_id, height=value)
                    await update.message.reply_text(
                        f"✅ تم تحديث الطول إلى: <b>{value}</b> سم",
                        parse_mode="HTML"
                    )
                else:
                    await update.message.reply_text("❌ الطول يجب أن يكون بين 140 و 220 سم")
                context.user_data.pop("edit_field", None)

            elif edit_field == "weight":
                value = float(text)
                if 30 <= value <= 200:
                    update_user_profile(db_user.user_id, weight=value)
                    await update.message.reply_text(
                        f"✅ تم تحديث الوزن إلى: <b>{value}</b> كجم",
                        parse_mode="HTML"
                    )
                else:
                    await update.message.reply_text("❌ الوزن يجب أن يكون بين 30 و 200 كجم")
                context.user_data.pop("edit_field", None)

            elif edit_field == "bodyfat":
                value = float(text)
                if 3 <= value <= 50:
                    update_user_profile(db_user.user_id, body_fat=value)
                    await update.message.reply_text(
                        f"✅ تم تحديث نسبة الدهون إلى: <b>{value}</b>%",
                        parse_mode="HTML"
                    )
                else:
                    await update.message.reply_text("❌ نسبة الدهون يجب أن تكون بين 3% و 50%")
                context.user_data.pop("edit_field", None)

            elif edit_field == "workout_days":
                value = int(text)
                if 1 <= value <= 7:
                    update_user_profile(db_user.user_id, workout_days=value)
                    await update.message.reply_text(
                        f"✅ تم تحديث أيام التمرين إلى: <b>{value}</b> أيام/أسبوع",
                        parse_mode="HTML"
                    )
                else:
                    await update.message.reply_text("❌ أيام التمرين يجب أن تكون بين 1 و 7")
                context.user_data.pop("edit_field", None)

        except ValueError:
            await update.message.reply_text("❌ يرجى إدخال رقم صحيح")

"""
معالجات التمارين - FitCoach Bot
"""
from telegram import Update
from telegram.ext import ContextTypes

from bot.database import (
    get_user_by_telegram_id, get_exercises_by_muscle as db_get_exercises,
    log_workout as db_log_workout, get_workouts_for_day, get_workout_history
)
from bot.keyboards import (
    get_workout_menu_keyboard, get_muscle_group_keyboard,
    get_back_to_main_keyboard, get_workout_exercise_keyboard,
    get_workout_sets_reps_keyboard, get_back_keyboard, get_confirmation_keyboard
)
from bot.data.exercises import (
    EXERCISES, get_exercise_by_id, get_exercises_by_muscle,
    format_exercise_text, get_alternative_exercises,
    get_workout_template, get_muscle_group_name
)
from datetime import date


WORKOUT_MENU_MESSAGE = """
🏋️ <b>قائمة التمارين</b>

━━━━━━━━━━━━━━━━

إدارة تمارينك وبرنامجك التدريبي.

━━━━━━━━━━━━━━━━
"""

MUSCLE_GROUP_MENU = """
💪 <b>اختر مجموعة العضلات</b>

━━━━━━━━━━━━━━━━

اختر العضلة التي تريد تدريبها اليوم:
"""


async def workout_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض قائمة التمارين"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        WORKOUT_MENU_MESSAGE,
        parse_mode="HTML",
        reply_markup=get_workout_menu_keyboard()
    )


async def muscle_group_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """اختيار مجموعة العضلات"""
    query = update.callback_query
    await query.answer()

    muscle = query.data.replace("muscle_", "")

    # الحصول على التمارين
    exercises = get_exercises_by_muscle(muscle)

    if not exercises:
        await query.edit_message_text(
            "❌ لا توجد تمارين لهذه العضلة.",
            parse_mode="HTML",
            reply_markup=get_back_keyboard("workout_menu")
        )
        return

    # تخزين المجموعة المختارة
    context.user_data["selected_muscle"] = muscle

    # تنسيق رسالة التمارين
    muscle_name = get_muscle_group_name(muscle)
    message = f"💪 <b>تمارين {muscle_name}</b>\n\n"
    message += "اختر تمريناً للبدء:\n\n"

    for i, ex in enumerate(exercises[:6], 1):
        message += f"{i}. {ex['name_ar']}\n"

    keyboard = get_workout_exercise_keyboard(exercises)

    await query.edit_message_text(
        message,
        parse_mode="HTML",
        reply_markup=keyboard
    )


async def exercise_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض تفاصيل التمرين"""
    query = update.callback_query
    await query.answer()

    exercise_id = int(query.data.replace("exercise_", ""))
    exercise = get_exercise_by_id(exercise_id)

    if not exercise:
        await query.edit_message_text(
            "❌ التمرين غير موجود.",
            parse_mode="HTML"
        )
        return

    # تخزين التمرين المختار
    context.user_data["selected_exercise"] = exercise_id

    # تنسيق النص
    text = format_exercise_text(exercise)

    # إضافة التمرين للتسجيل
    keyboard = get_workout_sets_reps_keyboard()

    # إضافة زر البدء
    from telegram import InlineKeyboardButton
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("▶️ بدء التمرين", callback_data=f"start_exercise_{exercise_id}")],
        [InlineKeyboardButton("📹 البدائل", callback_data=f"alternatives_{exercise_id}")],
        [InlineKeyboardButton("🔙 رجوع", callback_data=f"muscle_{context.user_data.get('selected_muscle', 'chest')}")]
    ])

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=keyboard
    )


async def start_exercise_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بدء التمرين"""
    query = update.callback_query
    await query.answer()

    exercise_id = int(query.data.replace("start_exercise_", ""))
    exercise = get_exercise_by_id(exercise_id)

    if not exercise:
        return

    context.user_data["active_exercise"] = exercise_id

    message = f"""
🏋️ <b>تسجيل تمرين: {exercise['name_ar']}</b>

━━━━━━━━━━━━━━━━

📝 أدخل بيانات التمرين بالشكل التالي:

<b>المجموعات</b>: عدد المجموعات
<b>التكرارات</b>: عدد التكرارات لكل مجموعة
<b>الوزن</b>: الوزن بالكيلوغرام (اختياري)

━━━━━━━━━━━━━━━━

مثال:
<code>4</code> (مجموعات)
<code>10</code> (تكرارات)
<code>60</code> (وزن، اختياري)

أو في سطر واحد:
<code>4x10x60</code>
"""

    await query.edit_message_text(
        message,
        parse_mode="HTML",
        reply_markup=get_back_keyboard(f"exercise_{exercise_id}")
    )


async def workout_today_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض تمارين اليوم"""
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    db_user = get_user_by_telegram_id(user.id)

    if not db_user or not db_user.age:
        await query.edit_message_text(
            "❌ لم تقم بإنشاء ملف شخصي بعد.",
            parse_mode="HTML"
        )
        return

    today = date.today()
    workouts = get_workouts_for_day(db_user.user_id, today)

    if not workouts:
        message = """
🏋️ <b>تمارين اليوم</b>

لم تقم بتسجيل أي تمارين اليوم.

💡 ابدأ بتسجيل تمارينك من القائمة.
"""
    else:
        message = f"""
🏋️ <b>تمارين اليوم</b> - {today.strftime('%Y-%m-%d')}

━━━━━━━━━━━━━━━━
"""

        for workout in workouts:
            exercise = get_exercise_by_id(workout.exercise_id)
            exercise_name = exercise['name_ar'] if exercise else 'تمرين'

            message += f"✅ <b>{exercise_name}</b>\n"
            message += f"   {workout.sets} × {workout.reps}"
            if workout.weight:
                message += f" @ {workout.weight} كجم"
            message += "\n\n"

        message += "━━━━━━━━━━━━━━━━"

    await query.edit_message_text(
        message,
        parse_mode="HTML",
        reply_markup=get_back_keyboard("workout_menu")
    )


async def workout_history_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض تاريخ التمارين"""
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    db_user = get_user_by_telegram_id(user.id)

    if not db_user or not db_user.age:
        await query.edit_message_text(
            "❌ لم تقم بإنشاء ملف شخصي بعد.",
            parse_mode="HTML"
        )
        return

    history = get_workout_history(db_user.user_id, limit=20)

    if not history:
        message = """
🏋️ <b>تاريخ التمارين</b>

لا يوجد تاريخ تمارين حالياً.
"""
    else:
        message = "🏋️ <b>آخر التمارين</b>\n\n"

        current_date = None
        for workout in history:
            if workout.date != current_date:
                current_date = workout.date
                message += f"\n📅 {current_date.strftime('%Y-%m-%d')}\n"
                message += "━━━━━━━━━━━━━━━━\n"

            exercise = get_exercise_by_id(workout.exercise_id)
            exercise_name = exercise['name_ar'] if exercise else 'تمرين'

            message += f"• {exercise_name}: {workout.sets}×{workout.reps}"
            if workout.weight:
                message += f" @ {workout.weight}ك"
            message += "\n"

    await query.edit_message_text(
        message,
        parse_mode="HTML",
        reply_markup=get_back_keyboard("workout_menu")
    )


async def handle_workout_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة إدخال بيانات التمرين"""
    text = update.message.text.strip()

    user = update.effective_user
    db_user = get_user_by_telegram_id(user.id)

    if not db_user:
        return

    exercise_id = context.user_data.get("active_exercise")

    if not exercise_id:
        return

    try:
        # تحليل المدخلات
        lines = text.split("\n")
        weights = None
        reps = None
        weight = None

        if "x" in text.lower():
            # تنسيق 4x10x60
            parts = text.lower().replace(" ", "").split("x")
            sets = int(parts[0])
            reps = int(parts[1])
            weight = float(parts[2]) if len(parts) > 2 else None
        else:
            sets = int(lines[0])
            reps = int(lines[1])
            weight = float(lines[2]) if len(lines) > 2 else None

        # تسجيل التمرين
        db_log_workout(
            user_id=db_user.user_id,
            exercise_id=exercise_id,
            sets=sets,
            reps=reps,
            weight=weight,
            date=date.today(),
            completed=True
        )

        exercise = get_exercise_by_id(exercise_id)
        exercise_name = exercise['name_ar'] if exercise else 'التمرين'

        await update.message.reply_text(
            f"✅ تم تسجيل: <b>{exercise_name}</b>\n\n"
            f"   📊 {sets} × {reps}"
            + (f" @ {weight} كجم" if weight else ""),
            parse_mode="HTML"
        )

        # تنظيف السياق
        context.user_data.pop("active_exercise", None)

    except Exception as e:
        await update.message.reply_text(
            f"❌ خطأ: {str(e)}\n\n"
            "📝 أدخل: المجموعات والتكرارات والوزن (اختياري)"
        )


async def workout_schedule_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض الجدول الأسبوعي"""
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    db_user = get_user_by_telegram_id(user.id)

    if not db_user or not db_user.age:
        await query.edit_message_text(
            "❌ لم تقم بإنشاء ملف شخصي بعد.",
            parse_mode="HTML"
        )
        return

    # إنشاء الجدول
    template = get_workout_template(
        db_user.experience_level,
        db_user.goal,
        db_user.workout_days
    )

    message = "📅 <b>جدولك الأسبوعي</b>\n\n"
    message += "━━━━━━━━━━━━━━━━\n\n"

    day_names = ["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة"]

    for i, (day, muscles) in enumerate(template.items()):
        muscles_text = " + ".join([get_muscle_group_name(m) for m in muscles])
        message += f"<b>{day_names[i]}:</b> {muscles_text}\n\n"

    message += "━━━━━━━━━━━━━━━━\n"
    message += "\n💡 هذا جدول مقترح. يمكنك تخصيصه حسب وقتك."

    await query.edit_message_text(
        message,
        parse_mode="HTML",
        reply_markup=get_back_keyboard("workout_menu")
    )

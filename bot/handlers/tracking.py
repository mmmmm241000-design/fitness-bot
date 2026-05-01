"""
معالجات التتبع - FitCoach Bot
"""
from telegram import Update
from telegram.ext import ContextTypes

from bot.database import (
    get_user_by_telegram_id, log_daily_progress, get_daily_progress,
    get_progress_range, update_user_profile
)
from bot.keyboards import (
    get_tracking_menu_keyboard, get_back_to_main_keyboard,
    get_water_unit_keyboard, get_back_keyboard
)
from datetime import date, timedelta


TRACKING_MENU_MESSAGE = """
📈 <b>قائمة التتبع</b>

━━━━━━━━━━━━━━━━

تتبع تقدمك اليومي في كل المجالات.

━━━━━━━━━━━━━━━━
"""


async def tracking_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض قائمة التتبع"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        TRACKING_MENU_MESSAGE,
        parse_mode="HTML",
        reply_markup=get_tracking_menu_keyboard()
    )


async def track_weight_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تسجيل الوزن"""
    query = update.callback_query
    await query.answer()

    context.user_data["tracking_type"] = "weight"

    message = """
⚖️ <b>تسجيل الوزن</b>

━━━━━━━━━━━━━━━━

أدخل وزنك بالكيلوغرام:

مثال: <code>75.5</code>

💡 أدخل وزنك بدون كلمة "كيلو" أو أي نص إضافي.
"""

    await query.edit_message_text(
        message,
        parse_mode="HTML",
        reply_markup=get_back_keyboard("tracking_menu")
    )


async def track_water_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تسجيل الماء"""
    query = update.callback_query
    await query.answer()

    context.user_data["tracking_type"] = "water"

    await query.edit_message_text(
        "💧 <b>تسجيل الماء</b>\n\n"
        "━━━━━━━━━━━━━━━━\n\n"
        "كم شربت؟",
        parse_mode="HTML",
        reply_markup=get_water_unit_keyboard()
    )


async def water_unit_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """اختيار وحدة الماء"""
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    db_user = get_user_by_telegram_id(user.id)

    if not db_user:
        return

    unit = query.data.replace("water_", "")

    # تحويل إلى لتر
    water_amounts = {
        "250": 0.25,
        "500": 0.5,
        "1000": 1.0
    }

    water = water_amounts.get(unit, 0)

    if unit == "custom":
        context.user_data["tracking_type"] = "water_custom"
        await query.edit_message_text(
            "💧 <b>أدخل كمية الماء</b>\n\n"
            "━━━━━━━━━━━━━━━━\n\n"
            "أدخل الكمية بالملليلتر (مل):\n\n"
            "مثال: <code>350</code>",
            parse_mode="HTML"
        )
        return

    # الحصول على التقدم الحالي
    today = date.today()
    progress = get_daily_progress(db_user.user_id, today)

    current_water = progress.water if progress and progress.water else 0
    new_water = current_water + water

    # تحديث التقدم
    log_daily_progress(
        user_id=db_user.user_id,
        date=today,
        water=new_water
    )

    goal = db_user.water_goal or 3.0
    remaining = max(0, goal - new_water)

    await query.edit_message_text(
        f"✅ <b>تم تحديث الماء</b>\n\n"
        f"💧 الاستهلاك: {new_water} لتر\n"
        f"🎯 الهدف: {goal} لتر\n"
        f"📊 المتبقي: {remaining} لتر\n\n"
        f"{'💪 ممتاز! وصلت للهدف!' if remaining <= 0 else '💪 اقتربت من الهدف!'}",
        parse_mode="HTML",
        reply_markup=get_water_unit_keyboard()
    )


async def track_sleep_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تسجيل النوم"""
    query = update.callback_query
    await query.answer()

    context.user_data["tracking_type"] = "sleep"

    message = """
😴 <b>تسجيل ساعات النوم</b>

━━━━━━━━━━━━━━━━

أدخل عدد ساعات نومك بالأمس:

مثال: <code>7.5</code>

💡 أدخل الساعات بالأرقام (يمكن استخدام .5 للنصف ساعة)
"""

    await query.edit_message_text(
        message,
        parse_mode="HTML",
        reply_markup=get_back_keyboard("tracking_menu")
    )


async def track_today_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض ملخص اليوم"""
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

    from bot.database import get_meals_summary
    from bot.services.nutrition_service import NutritionService

    today = date.today()
    progress = get_daily_progress(db_user.user_id, today)
    meals_summary = get_meals_summary(db_user.user_id, today)
    targets = NutritionService.get_daily_targets(db_user)

    # حساب نسبة الإنجاز
    water_progress = (progress.water / db_user.water_goal * 100) if progress and progress.water else 0
    sleep_progress = (progress.sleep_hours / db_user.sleep_goal * 100) if progress and progress.sleep_hours else 0

    cal_progress = (meals_summary['total_calories'] / targets['calories'] * 100) if targets['calories'] > 0 else 0

    cal_bar = self_progress_bar(cal_progress)
    water_bar = self_progress_bar(water_progress)
    sleep_bar = self_progress_bar(sleep_progress)

    message = f"""
📊 <b>ملخص اليوم</b> - {today.strftime('%Y-%m-%d')}

━━━━━━━━━━━━━━━━

⚖️ <b>الوزن:</b>
   {progress.weight if progress and progress.weight else 'غير مسجل'} كجم

━━━━━━━━━━━━━━━━

🍽️ <b>التغذية:</b>
   💰 السعرات: {meals_summary['total_calories']}/{round(targets['calories'])}
   [{cal_bar}]

━━━━━━━━━━━━━━━━

💧 <b>الماء:</b>
   {progress.water if progress and progress.water else 0}/{db_user.water_goal} لتر
   [{water_bar}]

━━━━━━━━━━━━━━━━

😴 <b>النوم:</b>
   {progress.sleep_hours if progress and progress.sleep_hours else 0}/{db_user.sleep_goal} ساعات
   [{sleep_bar}]

━━━━━━━━━━━━━━━━
"""

    await query.edit_message_text(
        message,
        parse_mode="HTML",
        reply_markup=get_back_keyboard("tracking_menu")
    )


def self_progress_bar(percentage: float) -> str:
    """إنشاء شريط تقدم نصي"""
    filled = min(10, max(0, int(percentage / 10)))
    empty = 10 - filled
    return "█" * filled + "░" * empty


async def track_progress_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض التقدم"""
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

    # الحصول على آخر 7 أيام
    progress_list = get_progress_range(db_user.user_id, 7)

    if not progress_list or len(progress_list) < 2:
        await query.edit_message_text(
            "📈 <b>تقدمك</b>\n\n"
            "━━━━━━━━━━━━━━━━\n\n"
            "لا يوجد بيانات كافية بعد.\n"
            "تابع التسجيل للحصول على إحصائيات دقيقة.",
            parse_mode="HTML",
            reply_markup=get_back_keyboard("tracking_menu")
        )
        return

    # حساب التغير
    first_weight = progress_list[0].weight
    last_weight = progress_list[-1].weight
    weight_change = last_weight - first_weight
    weight_change_text = f"+{weight_change:.1f}" if weight_change > 0 else f"{weight_change:.1f}"

    # المتوسط الحسابي
    weights = [p.weight for p in progress_list if p.weight]
    avg_weight = sum(weights) / len(weights) if weights else 0

    message = f"""
📈 <b>تقدمك الأسبوعي</b>

━━━━━━━━━━━━━━━━

⚖️ <b>الوزن:</b>

   البداية: {first_weight:.1f} كجم
   الحالية: {last_weight:.1f} كجم
   التغير: {weight_change_text} كجم
   المعدل: {avg_weight:.1f} كجم

━━━━━━━━━━━━━━━━

📊 <b>السعرات المتوسطة:</b>

   {sum(p.calories for p in progress_list) // len(progress_list)} سعرة/يوم

━━━━━━━━━━━━━━━━

💧 <b>الماء المتوسط:</b>

   {sum(p.water for p in progress_list) / len(progress_list):.1f} لتر/يوم

━━━━━━━━━━━━━━━━
"""

    await query.edit_message_text(
        message,
        parse_mode="HTML",
        reply_markup=get_back_keyboard("tracking_menu")
    )


async def handle_tracking_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة إدخال التتبع"""
    text = update.message.text.strip()
    tracking_type = context.user_data.get("tracking_type")

    user = update.effective_user
    db_user = get_user_by_telegram_id(user.id)

    if not db_user:
        return

    today = date.today()

    try:
        if tracking_type == "weight":
            weight = float(text)
            if 20 <= weight <= 300:
                log_daily_progress(
                    user_id=db_user.user_id,
                    date=today,
                    weight=weight
                )

                # تحديث وزن المستخدم أيضاً
                update_user_profile(db_user.user_id, weight=weight)

                await update.message.reply_text(
                    f"✅ تم تسجيل الوزن: <b>{weight}</b> كجم",
                    parse_mode="HTML"
                )
            else:
                await update.message.reply_text("❌ الوزن غير صالح (20-300 كجم)")

        elif tracking_type == "sleep":
            sleep_hours = float(text)
            if 0 <= sleep_hours <= 24:
                log_daily_progress(
                    user_id=db_user.user_id,
                    date=today,
                    sleep_hours=sleep_hours
                )

                await update.message.reply_text(
                    f"✅ تم تسجيل النوم: <b>{sleep_hours}</b> ساعات",
                    parse_mode="HTML"
                )
            else:
                await update.message.reply_text("❌ ساعات النوم غير صالحة (0-24)")

        elif tracking_type == "water_custom":
            ml = float(text)
            liters = ml / 1000

            progress = get_daily_progress(db_user.user_id, today)
            current_water = progress.water if progress and progress.water else 0
            new_water = current_water + liters

            log_daily_progress(
                user_id=db_user.user_id,
                date=today,
                water=new_water
            )

            await update.message.reply_text(
                f"✅ تم إضافة: <b>{ml}</b> مل ({liters:.2f} لتر)\n\n"
                f"💧 الإجمالي: {new_water:.2f} لتر",
                parse_mode="HTML"
            )

    except ValueError:
        await update.message.reply_text("❌ يرجى إدخال رقم صحيح")

    # تنظيف السياق
    context.user_data.pop("tracking_type", None)

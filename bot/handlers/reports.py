"""
معالجات التقارير والإعدادات - FitCoach Bot
"""
from telegram import Update
from telegram.ext import ContextTypes

from bot.database import (
    get_user_by_telegram_id, get_user_stats, get_weekly_report
)
from bot.keyboards import (
    get_reports_menu_keyboard, get_settings_menu_keyboard,
    get_back_to_main_keyboard, get_notification_toggle_keyboard,
    get_back_keyboard
)
from datetime import date, timedelta


REPORTS_MENU_MESSAGE = """
📋 <b>قائمة التقارير</b>

━━━━━━━━━━━━━━━━

راجع تقدمك وإحصائياتك التفصيلية.

━━━━━━━━━━━━━━━━
"""


async def reports_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض قائمة التقارير"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        REPORTS_MENU_MESSAGE,
        parse_mode="HTML",
        reply_markup=get_reports_menu_keyboard()
    )


async def report_weekly_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """التقرير الأسبوعي"""
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

    report = get_weekly_report(db_user.user_id)

    weight_status = "📈" if report['weight_change'] > 0 else "📉" if report['weight_change'] < 0 else "➡️"

    message = f"""
📆 <b>التقرير الأسبوعي</b>

━━━━━━━━━━━━━━━━

📅 الفترة: {report['start_date'].strftime('%Y-%m-%d')} - {report['end_date'].strftime('%Y-%m-%d')}

━━━━━━━━━━━━━━━━

⚖️ <b>الوزن:</b>
   البداية: {report['weight_start'] or 'غير مسجل'} كجم
   النهاية: {report['weight_end'] or 'غير مسجل'} كجم
   التغير: {weight_status} {report['weight_change']} كجم

━━━━━━━━━━━━━━━━

🏋️ <b>التمارين:</b>
   إجمالي التمارين: {report['total_workouts']}
   أيام التمرين: {len(set([str(w[0]) for w in report['workouts_by_day']]))}

━━━━━━━━━━━━━━━━

🍽️ <b>التغذية:</b>
   الوجبات: {report['total_meals']}
   السعرات المتوسطة: {round(report['avg_daily_calories'])} سعرة/يوم
   البروتين المتوسط: {round(report['avg_daily_protein'], 1)} غ/يوم

━━━━━━━━━━━━━━━━

💧 <b>السوائل:</b>
   متوسط الماء: {round(report['avg_water'], 1)} لتر/يوم

━━━━━━━━━━━━━━━━

😴 <b>النوم:</b>
   متوسط النوم: {round(report['avg_sleep'], 1)} ساعات/يوم

━━━━━━━━━━━━━━━━
"""

    await query.edit_message_text(
        message,
        parse_mode="HTML",
        reply_markup=get_back_keyboard("reports_menu")
    )


async def report_stats_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """إحصائيات المستخدم"""
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

    stats = get_user_stats(db_user.user_id)

    message = f"""
📊 <b>إحصائياتك الشاملة</b>

━━━━━━━━━━━━━━━━

🏋️ <b>التمارين:</b>
   إجمالي التمارين: {stats.total_workouts}
   سلسلة الالتزام: {stats.current_streak} يوم
   أطول سلسلة: {stats.longest_streak} يوم

━━━━━━━━━━━━━━━━

🍽️ <b>التغذية:</b>
   الوجبات المسجلة: {stats.total_meals}
   متوسط السعرات: {round(stats.avg_calories)} سعرة
   متوسط البروتين: {round(stats.avg_protein, 1)} غ

━━━━━━━━━━━━━━━━

💧 <b>العناية:</b>
   متوسط الماء: {round(stats.avg_water, 1)} لتر
   متوسط النوم: {round(stats.avg_sleep, 1)} ساعات

━━━━━━━━━━━━━━━━

⚖️ <b>الوزن:</b>
   التغير الكلي: {stats.weight_change:+.1f} كجم
   نسبة التغير: {stats.weight_change_percent:+.1f}%

━━━━━━━━━━━━━━━━

🎯 <b>التزامك:</b>
   درجة الالتزام: {stats.consistency_score}%

━━━━━━━━━━━━━━━━
"""

    await query.edit_message_text(
        message,
        parse_mode="HTML",
        reply_markup=get_back_keyboard("reports_menu")
    )


async def report_achievements_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """إنجازات المستخدم"""
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

    stats = get_user_stats(db_user.user_id)

    achievements = []

    # التحقق من الإنجازات
    if stats.total_workouts >= 1:
        achievements.append(("🏋️", "أول تمرين", "بدأت رحلتك!"))
    if stats.total_workouts >= 10:
        achievements.append(("💪", "10 تمارين", "ممتاز، تستمر!"))
    if stats.total_workouts >= 50:
        achievements.append(("🔥", "50 تمرين", "أنت محترف!"))
    if stats.current_streak >= 3:
        achievements.append(("📅", "3 أيام متتالية", "الالتزام طريق النجاح"))
    if stats.current_streak >= 7:
        achievements.append(("⭐", "أسبوع متتالي", "لا تتوقف!"))
    if stats.current_streak >= 30:
        achievements.append(("👑", "شهر متتالي", "أنت بطل حقيقي!"))
    if stats.consistency_score >= 80:
        achievements.append(("🎯", "التزام عالي", "أداء استثنائي!"))

    if not achievements:
        message = """
🏆 <b>إنجازاتك</b>

━━━━━━━━━━━━━━━━

لا توجد إنجازات بعد!

💡 ابدأ بالتمارين المنتظمة لكسب إنجازاتك الأولى.
"""
    else:
        message = "🏆 <b>إنجازاتك</b>\n\n━━━━━━━━━━━━━━━━\n\n"

        for icon, title, desc in achievements:
            message += f"{icon} <b>{title}</b>\n   {desc}\n\n"

        message += "━━━━━━━━━━━━━━━━"

    await query.edit_message_text(
        message,
        parse_mode="HTML",
        reply_markup=get_back_keyboard("reports_menu")
    )


# ===== معالجات الإعدادات =====

SETTINGS_MENU_MESSAGE = """
⚙️ <b>الإعدادات</b>

━━━━━━━━━━━━━━━━

خصص البوت حسب رغبتك.

━━━━━━━━━━━━━━━━
"""


async def settings_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض قائمة الإعدادات"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        SETTINGS_MENU_MESSAGE,
        parse_mode="HTML",
        reply_markup=get_settings_menu_keyboard()
    )


async def settings_notifications_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """إعدادات التنبيهات"""
    query = update.callback_query
    await query.answer()

    from bot.database import get_user_settings

    user = update.effective_user
    db_user = get_user_by_telegram_id(user.id)

    if not db_user:
        return

    settings = get_user_settings(db_user.user_id)
    enabled = settings.notifications_enabled if settings else True

    await query.edit_message_text(
        "🔔 <b>إعدادات التنبيهات</b>\n\n"
        "━━━━━━━━━━━━━━━━\n\n"
        "تفعيل أو تعطيل أنواع التنبيهات:",
        parse_mode="HTML",
        reply_markup=get_notification_toggle_keyboard(enabled)
    )


async def toggle_notification_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """تبديل حالة التنبيه"""
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    db_user = get_user_by_telegram_id(user.id)

    if not db_user:
        return

    from bot.database import get_user_settings, update_user_settings

    toggle_type = query.data.replace("toggle_", "")

    settings = get_user_settings(db_user.user_id)

    if toggle_type == "water_reminder":
        update_user_settings(
            db_user.user_id,
            reminder_water=not settings.reminder_water
        )
    elif toggle_type == "meal_reminder":
        update_user_settings(
            db_user.user_id,
            reminder_meal=not settings.reminder_meal
        )
    elif toggle_type == "workout_reminder":
        update_user_settings(
            db_user.user_id,
            reminder_workout=not settings.reminder_workout
        )

    # إعادة عرض القائمة
    settings = get_user_settings(db_user.user_id)
    enabled = settings.notifications_enabled if settings else True

    await query.edit_message_text(
        "🔔 <b>إعدادات التنبيهات</b>\n\n"
        "━━━━━━━━━━━━━━━━\n\n"
        "تم التحديث!",
        parse_mode="HTML",
        reply_markup=get_notification_toggle_keyboard(enabled)
    )


async def settings_account_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معلومات الحساب"""
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

    from bot.database import get_user_stats

    stats = get_user_stats(db_user.user_id)

    message = f"""
👤 <b>معلومات الحساب</b>

━━━━━━━━━━━━━━━━

🆔 معرف Telegram: <code>{user.id}</code>
📅 تاريخ التسجيل: {db_user.created_at.strftime('%Y-%m-%d') if db_user.created_at else 'غير معروف'}

━━━━━━━━━━━━━━━━

🏋️ إجمالي التمارين: {stats.total_workouts}
🍽️ الوجبات المسجلة: {stats.total_meals}
📈 أيام الاستخدام: {stats.current_streak}

━━━━━━━━━━━━━━━━

💡 لحذف حسابك، تواصل مع المطور.
"""

    await query.edit_message_text(
        message,
        parse_mode="HTML",
        reply_markup=get_back_keyboard("settings_menu")
    )


async def settings_help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مساعدة"""
    query = update.callback_query
    await query.answer()

    message = """
ℹ️ <b>مساعدة FitCoach</b>

━━━━━━━━━━━━━━━━

<b>أوامر البوت:</b>

/start - بدء البوت
/menu - القائمة الرئيسية
/profile - الملف الشخصي
/today - ملخص اليوم
/help - المساعدة

━━━━━━━━━━━━━━━━

<b>مشاكل شائعة:</b>

❓ البوت لا يستجيب
   → أعد التشغيل بـ /start

❓ لا أستطيع إضافة وجبة
   → تأكد من إدخال الاسم والوزن بشكل صحيح

❓ كيف أحسب السعرات؟
   → أدخل اسم الطعام ووزنه، البوت يحسب تلقائياً

━━━━━━━━━━━━━━━━

💡 للمزيد من المساعدة، تواصل مع المطور.
"""

    await query.edit_message_text(
        message,
        parse_mode="HTML",
        reply_markup=get_back_keyboard("settings_menu")
    )

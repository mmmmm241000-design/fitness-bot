"""
FitCoach Bot - نقطة الدخول الرئيسية
بوت تلجرام متكامل لكمال الأجسام وبناء الكتلة العضلية
"""
import logging
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

# إضافة مسار المشروع
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes
)

from bot.config import config
from bot.models import init_database

# استيراد المعالجات
from bot.handlers.start import (
    start_command, help_command, menu_command,
    profile_command, today_command
)
from bot.handlers.profile import (
    profile_menu_callback, profile_view_callback, profile_edit_callback,
    exp_level_callback, goal_callback, activity_callback,
    handle_profile_input
)
from bot.handlers.nutrition import (
    nutrition_menu_callback, nutrition_add_callback,
    meal_type_callback, nutrition_today_callback,
    nutrition_summary_callback, nutrition_goals_callback,
    nutrition_suggest_callback, handle_meal_input
)
from bot.handlers.workout import (
    workout_menu_callback, muscle_group_callback,
    exercise_callback, start_exercise_callback,
    workout_today_callback, workout_history_callback,
    workout_schedule_callback, handle_workout_input
)
from bot.handlers.tracking import (
    tracking_menu_callback, track_weight_callback,
    track_water_callback, water_unit_callback,
    track_sleep_callback, track_today_callback,
    track_progress_callback, handle_tracking_input
)
from bot.handlers.reports import (
    reports_menu_callback, report_weekly_callback,
    report_stats_callback, report_achievements_callback,
    settings_menu_callback, settings_notifications_callback,
    toggle_notification_callback, settings_account_callback,
    settings_help_callback
)

# استيراد لوحة المفاتيح
from bot.keyboards import get_main_menu_keyboard, get_back_to_main_keyboard

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def main_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """القائمة الرئيسية"""
    query = update.callback_query
    await query.answer()

    from bot.handlers.start import MAIN_MENU_MESSAGE
    await query.edit_message_text(
        MAIN_MENU_MESSAGE,
        parse_mode="HTML",
        reply_markup=get_main_menu_keyboard()
    )


async def cancel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """إلغاء العملية"""
    query = update.callback_query
    await query.answer()

    context.user_data.clear()

    await query.edit_message_text(
        "❌ تم الإلغاء.\n\nاضغط /menu للعودة للقائمة الرئيسية.",
        parse_mode="HTML",
        reply_markup=get_main_menu_keyboard()
    )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج الأخطاء"""
    logger.error(f"خطأ: {context.error}")
    try:
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ حدث خطأ غير متوقع.\n"
                "💡 جرب مرة أخرى أو اضغط /start"
            )
    except:
        pass


def setup_handlers(app: Application):
    """إعداد جميع المعالجات"""

    # أوامر البوت الأساسية
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("menu", menu_command))
    app.add_handler(CommandHandler("profile", profile_command))
    app.add_handler(CommandHandler("today", today_command))

    # القائمة الرئيسية
    app.add_handler(CallbackQueryHandler(main_menu_callback, pattern="^main_menu$"))

    # ===== الملف الشخصي =====
    app.add_handler(CallbackQueryHandler(profile_menu_callback, pattern="^profile_menu$"))
    app.add_handler(CallbackQueryHandler(profile_view_callback, pattern="^profile_view$"))
    app.add_handler(CallbackQueryHandler(profile_edit_callback, pattern="^edit_"))

    # مستوى الخبرة
    app.add_handler(CallbackQueryHandler(exp_level_callback, pattern="^exp_"))

    # الهدف
    app.add_handler(CallbackQueryHandler(goal_callback, pattern="^goal_"))

    # النشاط
    app.add_handler(CallbackQueryHandler(activity_callback, pattern="^activity_"))

    # ===== التغذية =====
    app.add_handler(CallbackQueryHandler(nutrition_menu_callback, pattern="^nutrition_menu$"))
    app.add_handler(CallbackQueryHandler(nutrition_add_callback, pattern="^nutrition_add$"))
    app.add_handler(CallbackQueryHandler(meal_type_callback, pattern="^meal_"))
    app.add_handler(CallbackQueryHandler(nutrition_today_callback, pattern="^nutrition_today$"))
    app.add_handler(CallbackQueryHandler(nutrition_summary_callback, pattern="^nutrition_summary$"))
    app.add_handler(CallbackQueryHandler(nutrition_goals_callback, pattern="^nutrition_goals$"))
    app.add_handler(CallbackQueryHandler(nutrition_suggest_callback, pattern="^nutrition_suggest$"))

    # ===== التمارين =====
    app.add_handler(CallbackQueryHandler(workout_menu_callback, pattern="^workout_menu$"))
    app.add_handler(CallbackQueryHandler(muscle_group_callback, pattern="^muscle_"))
    app.add_handler(CallbackQueryHandler(exercise_callback, pattern="^exercise_"))
    app.add_handler(CallbackQueryHandler(start_exercise_callback, pattern="^start_exercise_"))
    app.add_handler(CallbackQueryHandler(workout_today_callback, pattern="^workout_today$"))
    app.add_handler(CallbackQueryHandler(workout_history_callback, pattern="^workout_history$"))
    app.add_handler(CallbackQueryHandler(workout_schedule_callback, pattern="^workout_schedule$"))

    # ===== التتبع =====
    app.add_handler(CallbackQueryHandler(tracking_menu_callback, pattern="^tracking_menu$"))
    app.add_handler(CallbackQueryHandler(track_weight_callback, pattern="^track_weight$"))
    app.add_handler(CallbackQueryHandler(track_water_callback, pattern="^track_water$"))
    app.add_handler(CallbackQueryHandler(water_unit_callback, pattern="^water_"))
    app.add_handler(CallbackQueryHandler(track_sleep_callback, pattern="^track_sleep$"))
    app.add_handler(CallbackQueryHandler(track_today_callback, pattern="^track_today$"))
    app.add_handler(CallbackQueryHandler(track_progress_callback, pattern="^track_progress$"))

    # ===== التقارير =====
    app.add_handler(CallbackQueryHandler(reports_menu_callback, pattern="^reports_menu$"))
    app.add_handler(CallbackQueryHandler(report_weekly_callback, pattern="^report_weekly$"))
    app.add_handler(CallbackQueryHandler(report_stats_callback, pattern="^report_stats$"))
    app.add_handler(CallbackQueryHandler(report_achievements_callback, pattern="^report_achievements$"))

    # ===== الإعدادات =====
    app.add_handler(CallbackQueryHandler(settings_menu_callback, pattern="^settings_menu$"))
    app.add_handler(CallbackQueryHandler(settings_notifications_callback, pattern="^settings_notifications$"))
    app.add_handler(CallbackQueryHandler(toggle_notification_callback, pattern="^toggle_"))
    app.add_handler(CallbackQueryHandler(settings_account_callback, pattern="^settings_account$"))
    app.add_handler(CallbackQueryHandler(settings_help_callback, pattern="^settings_help$"))

    # الإلغاء
    app.add_handler(CallbackQueryHandler(cancel_callback, pattern="^cancel$"))

    # معالجات الرسائل النصية
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        handle_text_input
    ))

    # معالج الأخطاء
    app.add_error_handler(error_handler)


async def handle_text_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الإدخال النصي"""

    # التحقق من نوع المعالجة المطلوبة
    if context.user_data.get("edit_field"):
        await handle_profile_input(update, context)
    elif context.user_data.get("nutrition_step") == "meal_details":
        await handle_meal_input(update, context)
    elif context.user_data.get("active_exercise"):
        await handle_workout_input(update, context)
    elif context.user_data.get("tracking_type"):
        await handle_tracking_input(update, context)
    else:
        await update.message.reply_text(
            "📝 استخدم الأزرار للقائمة.\n\n"
            "أو اضغط /menu للعودة للقائمة الرئيسية."
        )


class HealthCheckHandler(BaseHTTPRequestHandler):
    """معالج health check لـ Render"""
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')
    def log_message(self, format, *args):
        pass  # Suppress logs

def start_health_server(port=10000):
    """تشغيل خادم health check"""
    try:
        server = HTTPServer(('', port), HealthCheckHandler)
        import threading
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        print(f"✅ Health check server running on port {port}")
    except Exception as e:
        print(f"⚠️ Health server error: {e}")

def main():
    """الدالة الرئيسية"""

    # إنشاء مجلدات البيانات والسجلات
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("config", exist_ok=True)

    # تشغيل health check server أولاً
    start_health_server()

    # تهيئة قاعدة البيانات
    logger.info("جاري تهيئة قاعدة البيانات...")
    init_database()

    # ملء قاعدة بيانات التمارين
    from bot.database import add_exercise, get_all_exercises
    from bot.data.exercises import EXERCISES

    existing_exercises = get_all_exercises()
    if not existing_exercises:
        logger.info("جاري ملء قاعدة بيانات التمارين...")
        for exercise_data in EXERCISES:
            add_exercise(exercise_data)
        logger.info(f"تم إضافة {len(EXERCISES)} تمرين")

    # التحقق من وجود Token
    if not config.bot_token:
        logger.error("❌ لم يتم العثور على BOT_TOKEN!")
        logger.error("يرجى إضافة Token في ملف .env أو متغير البيئة BOT_TOKEN")
        print("\n" + "="*50)
        print("⚠️  خطأ: لم يتم العثور على Bot Token!")
        print("="*50)
        print("\nلتشغيل البوت:")
        print("1. احصل على Token من @BotFather في Telegram")
        print("2. أنشئ ملف .env في مجلد المشروع")
        print("3. أضف السطر: BOT_TOKEN=your_token_here")
        print("="*50 + "\n")
        return

    # إنشاء التطبيق
    app = Application.builder().token(config.bot_token).build()

    # إعداد المعالجات
    setup_handlers(app)

    # بدء البوت
    logger.info("="*50)
    logger.info("🏋️ FitCoach Bot يبدأ التشغيل...")
    logger.info("="*50)

    print("\n" + "="*50)
    print("🏋️ FitCoach Bot - بوت المدرب الذكي")
    print("="*50)
    print("✅ البوت يعمل الآن!")
    print("📱 افتح Telegram وابحث عن بوتك")
    print("="*50 + "\n")

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

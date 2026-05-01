"""
معالجات الأوامر الأساسية - FitCoach Bot
"""
from datetime import date
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from bot.database import (
    get_or_create_user, get_user_by_telegram_id, update_user_profile
)
from bot.keyboards import (
    get_main_menu_keyboard, get_profile_menu_keyboard,
    get_experience_level_keyboard, get_goal_type_keyboard,
    get_activity_level_keyboard
)
from bot.models import User


# ===== رسائل البوت =====
WELCOME_MESSAGE = """
🏋️ <b>أهلاً بك في FitCoach!</b>

أنا مدربك الشخصي الذكي، جاهز لمساعدتك في تحقيق أهدافك الرياضية والتغذوية.

━━━━━━━━━━━━━━━━

🎯 <b>ما الذي أستطيع مساعدتك فيه:</b>

📊 <b>تتبع تقدمك</b> - الوزن، التغذية، التمارين
🍽️ <b>تخطيط غذائي ذكي</b> - وجبات حسب هدفك
💪 <b>برامج تدريب</b> - جداول مخصصة لك
📈 <b>تقارير وتحليلات</b> - لمتابعة تطورك
🤖 <b>ذكاء تكيفي</b> - يتعلم من بياناتك

━━━━━━━━━━━━━━━━

📝 للبدء، أحتاج بعض المعلومات عنك:

• عمرك وبياناتك الجسدية
• هدفك (ضخامة / تنشيف / بناء)
• مستوى خبرتك في التمرين

━━━━━━━━━━━━━━━━

💡 <b>ابدأ الآن:</b> اضغط على "👤 إنشاء الملف الشخصي"
"""

SETUP_START_MESSAGE = """
👤 <b>لنبدأ بإنشاء ملفك الشخصي!</b>

سأطرح عليك بعض الأسئلة البسيطة لتقديم أفضل تجربة لك.

━━━━━━━━━━━━━━━━

🎂 <b>السؤال الأول:</b>

كم عمرك؟ (14-70 سنة)

📌 أرسل رقم عمرك كمثال: <code>25</code>
"""

PROFILE_CREATED_MESSAGE = """
✅ <b>تم إنشاء ملفك الشخصي بنجاح!</b>

━━━━━━━━━━━━━━━━

📋 <b>ملخص ملفك:</b>

🎂 العمر: {age} سنة
📏 الطول: {height} سم
⚖️ الوزن: {weight} كجم
🎯 الهدف: {goal}
⭐ الخبرة: {experience}
📅 أيام التمرين: {workout_days} أيام/أسبوع

━━━━━━━━━━━━━━━━

🔢 <b>احتياجك اليومي من السعرات:</b> ~{calories} سعرة

💡 هذا تقدير مبدئي. يمكنك تعديله لاحقاً.
"""

MAIN_MENU_MESSAGE = """
🏋️ <b>FitCoach - القائمة الرئيسية</b>

أختر ما تريد من الأزرار أدناه:

━━━━━━━━━━━━━━━━
"""

HELP_MESSAGE = """
📖 <b>دليل استخدام FitCoach</b>

━━━━━━━━━━━━━━━━

<b>كيفية الاستخدام:</b>

1️⃣ <b>إنشاء الملف الشخصي</b>
   اضغط على "إنشاء الملف الشخصي"
   وأجب على الأسئلة

2️⃣ <b>تتبع يومك</b>
   • سجل وزنك يومياً
   • أضف وجباتك
   • تتبع الماء والنوم

3️⃣ <b>التدريب</b>
   • اختر مجموعة العضلات
   • ابدأ التمرين
   • سجّل الأوزان والتكرارات

4️⃣ <b>رؤية تقدمك</b>
   • تحقق من التقارير
   • راقب تغير وزنك
   • اضبط خطتك

━━━━━━━━━━━━━━━━

<b>أوامر سريعة:</b>

/start - إعادة تشغيل البوت
/menu - القائمة الرئيسية
/profile - ملفك الشخصي
/today - ملخص اليوم
/help - المساعدة

━━━━━━━━━━━━━━━━

💡 <b>نصيحة:</b>
التزم بالاستخدام اليومي للحصول على أفضل النتائج!
"""


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر البدء"""
    user = update.effective_user

    # الحصول على المستخدم أو إنشاؤه
    db_user = get_or_create_user(user.id, user.first_name)

    if not db_user.age:
        # المستخدم جديد - يحتاج إنشاء ملف شخصي
        await update.message.reply_text(
            WELCOME_MESSAGE,
            parse_mode="HTML",
            reply_markup=get_profile_menu_keyboard()
        )
    else:
        # المستخدم موجود
        await update.message.reply_text(
            MAIN_MENU_MESSAGE,
            parse_mode="HTML",
            reply_markup=get_main_menu_keyboard()
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر المساعدة"""
    await update.message.reply_text(
        HELP_MESSAGE,
        parse_mode="HTML"
    )


async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر القائمة الرئيسية"""
    await update.message.reply_text(
        MAIN_MENU_MESSAGE,
        parse_mode="HTML",
        reply_markup=get_main_menu_keyboard()
    )


async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر الملف الشخصي"""
    user = update.effective_user
    db_user = get_user_by_telegram_id(user.id)

    if not db_user or not db_user.age:
        await update.message.reply_text(
            "❌ لم تقم بإنشاء ملف شخصي بعد.\n\nاضغط /start للبدء.",
            parse_mode="HTML"
        )
        return

    # حساب السعرات
    try:
        calories = round(db_user.calculate_tdee())
    except:
        calories = 0

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

    message = f"""
👤 <b>ملفك الشخصي</b>

━━━━━━━━━━━━━━━━

🎂 العمر: {db_user.age} سنة
📏 الطول: {db_user.height} سم
⚖️ الوزن: {db_user.weight} كجم
📐 نسبة الدهون: {db_user.body_fat or 'غير محدد'}%

━━━━━━━━━━━━━━━━

🎯 الهدف: {goal_names.get(db_user.goal, db_user.goal)}
⭐ الخبرة: {exp_names.get(db_user.experience_level, db_user.experience_level)}
📅 أيام التمرين: {db_user.workout_days} أيام/أسبوع
🏃 النشاط: {db_user.activity_level}

━━━━━━━━━━━━━━━━

🔢 <b>احتياجك اليومي:</b>
💰 السعرات: ~{calories} سعرة
🥩 البروتين: ~{round(db_user.weight * 2.2)}غ
🍚 الكربوهيدرات: ~{round(calories * 0.4 / 4)}غ
🧈 الدهون: ~{round(calories * 0.25 / 9)}غ

━━━━━━━━━━━━━━━━
"""

    await update.message.reply_text(
        message,
        parse_mode="HTML",
        reply_markup=get_profile_menu_keyboard()
    )


async def today_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """أمر ملخص اليوم"""
    user = update.effective_user
    db_user = get_user_by_telegram_id(user.id)

    if not db_user or not db_user.age:
        await update.message.reply_text(
            "❌ لم تقم بإنشاء ملف شخصي بعد.\n\nاضغط /start للبدء.",
            parse_mode="HTML"
        )
        return

    from bot.database import get_daily_progress, get_meals_summary
    from bot.services.nutrition_service import NutritionService

    today = date.today()

    # التقدم اليومي
    progress = get_daily_progress(db_user.user_id, today)
    meals_summary = get_meals_summary(db_user.user_id, today)
    nutrition_progress = NutritionService.calculate_progress(db_user.user_id, today)
    targets = NutritionService.get_daily_targets(db_user)

    message = f"""
📅 <b>ملخص يوم {today.strftime('%Y-%m-%d')}</b>

━━━━━━━━━━━━━━━━

⚖️ <b>الوزن:</b> {progress.weight if progress and progress.weight else 'غير مسجل'} كجم

━━━━━━━━━━━━━━━━

🍽️ <b>التغذية:</b>

💰 السعرات: {meals_summary['total_calories']} / {round(targets['calories'])} سعرة
🥩 البروتين: {round(meals_summary['total_protein'], 1)} / {round(targets['protein'])}غ
🍚 الكربوهيدرات: {round(meals_summary['total_carbs'], 1)} / {round(targets['carbs'])}غ
🧈 الدهون: {round(meals_summary['total_fats'], 1)} / {round(targets['fats'])}غ

━━━━━━━━━━━━━━━━

💧 <b>الماء:</b> {progress.water if progress and progress.water else 0} لتر
   الهدف: {db_user.water_goal} لتر

😴 <b>النوم:</b> {progress.sleep_hours if progress and progress.sleep_hours else 0} ساعات
   الهدف: {db_user.sleep_goal} ساعات

━━━━━━━━━━━━━━━━
"""

    await update.message.reply_text(
        message,
        parse_mode="HTML"
    )


async def setup_profile_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بدء إعداد الملف الشخصي"""
    await update.message.reply_text(
        SETUP_START_MESSAGE,
        parse_mode="HTML"
    )
    context.user_data["setup_step"] = "age"

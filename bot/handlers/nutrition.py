"""
معالجات التغذية - FitCoach Bot
"""
from telegram import Update
from telegram.ext import ContextTypes

from bot.database import (
    get_user_by_telegram_id, add_meal, get_meals_for_day,
    get_meals_summary, delete_meal
)
from bot.keyboards import (
    get_nutrition_menu_keyboard, get_meal_type_keyboard,
    get_back_to_main_keyboard, get_back_keyboard
)
from bot.services.nutrition_service import NutritionService
from bot.models import MealType
from datetime import date


NUTRITION_MENU_MESSAGE = """
🍽️ <b>قائمة التغذية</b>

━━━━━━━━━━━━━━━━

إدارة وجباتك وتتبع تغذيتك اليومية.

━━━━━━━━━━━━━━━━
"""

ADD_MEAL_PROMPT = """
🍽️ <b>إضافة وجبة</b>

━━━━━━━━━━━━━━━━

اختر نوع الوجبة:
"""

MEAL_DETAILS_PROMPT = """
📝 <b>أدخل تفاصيل الوجبة</b>

━━━━━━━━━━━━━━━━

الرجاء إدخال البيانات بالشكل التالي:

<b>اسم الطعام</b>: [الاسم]
<b>الوزن بالغرام</b>: [الوزن]

مثال:
<code>صدر دجاج</code>
<code>200</code>

💡 أو أدخل القيم مباشرة:
<code>صدر دجاج | 200 | 330 | 62 | 0 | 6</code>

حيث: اسم | وزن | سعرات | بروتين | كارب | دهون
"""

TODAY_MEALS_MESSAGE = """
🍽️ <b>وجبات اليوم</b> - {date}

━━━━━━━━━━━━━━━━

{meals}

━━━━━━━━━━━━━━━━

📊 <b>الملخص:</b>

💰 السعرات: {total_calories} / {target_calories}
🥩 البروتين: {total_protein}غ / {target_protein}غ
🍚 الكربوهيدرات: {total_carbs}غ / {target_carbs}غ
🧈 الدهون: {total_fats}غ / {target_fats}غ

━━━━━━━━━━━━━━━━
"""

NO_MEALS_MESSAGE = """
🍽️ <b>وجبات اليوم</b>

لم تقم بإضافة أي وجبات حتى الآن.

🍳 ابدأ بإضافة وجباتك من القائمة.
"""


async def nutrition_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض قائمة التغذية"""
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        NUTRITION_MENU_MESSAGE,
        parse_mode="HTML",
        reply_markup=get_nutrition_menu_keyboard()
    )


async def nutrition_add_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """بدء إضافة وجبة"""
    query = update.callback_query
    await query.answer()

    context.user_data["nutrition_step"] = "meal_type"

    await query.edit_message_text(
        ADD_MEAL_PROMPT,
        parse_mode="HTML",
        reply_markup=get_meal_type_keyboard()
    )


async def meal_type_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """اختيار نوع الوجبة"""
    query = update.callback_query
    await query.answer()

    meal_type = query.data.replace("meal_", "")
    context.user_data["meal_type"] = meal_type

    meal_type_names = {
        "breakfast": "🍳 إفطار",
        "lunch": "🥗 غداء",
        "dinner": "🍽️ عشاء",
        "snack": "🍼 وجبة خفيفة"
    }

    await query.edit_message_text(
        f"🍽️ نوع الوجبة: <b>{meal_type_names.get(meal_type, meal_type)}</b>\n\n"
        f"{MEAL_DETAILS_PROMPT}",
        parse_mode="HTML"
    )

    context.user_data["nutrition_step"] = "meal_details"


async def nutrition_today_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض وجبات اليوم"""
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

    today = date.today()
    meals = get_meals_for_day(db_user.user_id, today)
    summary = get_meals_summary(db_user.user_id, today)
    targets = NutritionService.get_daily_targets(db_user)

    if not meals:
        await query.edit_message_text(
            NO_MEALS_MESSAGE,
            parse_mode="HTML",
            reply_markup=get_back_keyboard("nutrition_menu")
        )
        return

    meals_text = ""
    meal_type_names = {
        "breakfast": "🍳 إفطار",
        "lunch": "🥗 غداء",
        "dinner": "🍽️ عشاء",
        "snack": "🍼 وجبة خفيفة"
    }

    for meal in meals:
        meals_text += f"<b>{meal_type_names.get(meal.meal_type, meal.meal_type)}:</b>\n"
        meals_text += f"  • {meal.name}\n"
        meals_text += f"  💰 {meal.calories} سعرة | 🥩 {round(meal.protein, 1)}غ | 🍚 {round(meal.carbs, 1)}غ | 🧈 {round(meal.fats, 1)}غ\n\n"

    message = TODAY_MEALS_MESSAGE.format(
        date=today.strftime("%Y-%m-%d"),
        meals=meals_text,
        total_calories=summary["total_calories"],
        total_protein=round(summary["total_protein"], 1),
        total_carbs=round(summary["total_carbs"], 1),
        total_fats=round(summary["total_fats"], 1),
        target_calories=round(targets["calories"]),
        target_protein=round(targets["protein"]),
        target_carbs=round(targets["carbs"]),
        target_fats=round(targets["fats"])
    )

    await query.edit_message_text(
        message,
        parse_mode="HTML",
        reply_markup=get_back_keyboard("nutrition_menu")
    )


async def nutrition_summary_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض ملخص التغذية"""
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

    progress = NutritionService.calculate_progress(db_user.user_id)
    summary_text = NutritionService.generate_nutrition_summary_text(progress)

    await query.edit_message_text(
        summary_text,
        parse_mode="HTML",
        reply_markup=get_back_keyboard("nutrition_menu")
    )


async def nutrition_goals_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """عرض الأهداف الغذائية"""
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

    targets = NutritionService.get_daily_targets(db_user)

    goal_names = {
        "bulking": "🔥 ضخامة عضلية",
        "cutting": "❄️ تنشيف",
        "recomp": "🔄 إعادة تركيب"
    }

    message = f"""
🎯 <b>أهدافك الغذائية اليومية</b>

━━━━━━━━━━━━━━━━

🎯 الهدف: <b>{goal_names.get(db_user.goal, db_user.goal)}</b>

━━━━━━━━━━━━━━━━

💰 <b>السعرات:</b> ~{round(targets['calories'])} سعرة/يوم
   (لتحقيق هدفك)

🥩 <b>البروتين:</b> {round(targets['protein'])}غ/يوم
   ({round(targets['protein'] / db_user.weight, 1)} غ لكل كجم من وزن الجسم)

🍚 <b>الكربوهيدرات:</b> {round(targets['carbs'])}غ/يوم
   ({round(targets['carbs'] / targets['calories'] * 100, 1)}% من السعرات)

🧈 <b>الدهون:</b> {round(targets['fats'])}غ/يوم
   ({round(targets['fats'] / targets['calories'] * 100, 1)}% من السعرات)

━━━━━━━━━━━━━━━━

💡 <b>ملاحظة:</b>
هذه القيم تقديرية. يمكنك تعديلها حسب استجابة جسمك.
"""

    await query.edit_message_text(
        message,
        parse_mode="HTML",
        reply_markup=get_back_keyboard("nutrition_menu")
    )


async def nutrition_suggest_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """اقتراح وجبات"""
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

    goal = db_user.goal or "bulking"

    goal_names = {
        "bulking": "🔥 ضخامة عضلية",
        "cutting": "❄️ تنشيف",
        "recomp": "🔄 إعادة تركيب"
    }

    suggestions = []
    for meal_type in ["breakfast", "lunch", "dinner", "snack"]:
        meals = NutritionService.get_meal_suggestion(goal, meal_type)
        if meals:
            meal_type_names = {
                "breakfast": "🍳 الإفطار",
                "lunch": "🥗 الغداء",
                "dinner": "🍽️ العشاء",
                "snack": "🍼 الوجبات الخفيفة"
            }
            suggestions.append(f"<b>{meal_type_names[meal_type]}:</b>")
            for i, meal in enumerate(meals, 1):
                suggestions.append(
                    f"{i}. {meal['name']}\n"
                    f"   💰 {meal['calories']} سعرة | "
                    f"🥩 {meal['protein']}غ بروتين"
                )
            suggestions.append("")

    message = f"""
🍽️ <b>اقتراحات وجبات</b> - هدف: {goal_names.get(goal, goal)}

━━━━━━━━━━━━━━━━

""" + "\n\n".join(suggestions) + """
━━━━━━━━━━━━━━━━

💡 هذه مجرد اقتراحات. عدّل الكميات حسب هدفك.
"""

    await query.edit_message_text(
        message,
        parse_mode="HTML",
        reply_markup=get_back_keyboard("nutrition_menu")
    )


async def handle_meal_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة إدخال الوجبة"""
    text = update.message.text.strip()

    user = update.effective_user
    db_user = get_user_by_telegram_id(user.id)

    if not db_user:
        return

    # تحليل المدخلات
    lines = text.split("\n")
    meal_type = context.user_data.get("meal_type", "snack")

    try:
        # طريقة الإدخال السهلة: اسم + وزن
        if len(lines) == 2:
            food_name = lines[0].strip()
            grams = float(lines[1].strip())

            nutrition = NutritionService.calculate_food_nutrition(food_name, grams)

            if nutrition:
                add_meal(
                    user_id=db_user.user_id,
                    meal_type=meal_type,
                    name=food_name,
                    calories=nutrition["calories"],
                    protein=nutrition["protein"],
                    carbs=nutrition["carbs"],
                    fats=nutrition["fats"]
                )

                await update.message.reply_text(
                    f"✅ تم إضافة: <b>{food_name}</b>\n\n"
                    f"💰 {nutrition['calories']} سعرة\n"
                    f"🥩 {nutrition['protein']}غ بروتين\n"
                    f"🍚 {nutrition['carbs']}غ كربو\n"
                    f"🧈 {nutrition['fats']}غ دهون",
                    parse_mode="HTML"
                )
            else:
                # البحث في قاعدة البيانات
                results = NutritionService.search_foods(food_name)
                if results:
                    response = "🔍 <b>نتائج البحث:</b>\n\n"
                    for i, food in enumerate(results[:5], 1):
                        response += f"{i}. {food['name']}\n"
                        response += f"   💰 {food['calories_100g']} سعرة/100غ\n\n"
                    response += "📝 أدخل الاسم والوزن بالغرام:\n"
                    response += "مثال:\n"
                    response += "<code>صدر دجاج</code>\n<code>200</code>"
                    await update.message.reply_text(response, parse_mode="HTML")
                else:
                    await update.message.reply_text(
                        "❌ لم يتم العثور على هذا الطعام.\n"
                        "💡 جرب البحث بكلمة مختلفة."
                    )

        # طريقة الإدخال المخصصة
        elif "|" in text:
            parts = [p.strip() for p in text.split("|")]
            if len(parts) >= 6:
                name = parts[0]
                calories = int(parts[2])
                protein = float(parts[3])
                carbs = float(parts[4])
                fats = float(parts[5])

                add_meal(
                    user_id=db_user.user_id,
                    meal_type=meal_type,
                    name=name,
                    calories=calories,
                    protein=protein,
                    carbs=carbs,
                    fats=fats
                )

                await update.message.reply_text(
                    f"✅ تم إضافة: <b>{name}</b>",
                    parse_mode="HTML"
                )

        else:
            await update.message.reply_text(
                "❌ تنسيق غير صحيح.\n"
                "📝 أدخل:\n"
                "<code>اسم الطعام</code>\n<code>الوزن بالغرام</code>"
            )

    except Exception as e:
        await update.message.reply_text(
            f"❌ خطأ: {str(e)}\n"
            "📝 تأكد من صحة البيانات المدخلة."
        )

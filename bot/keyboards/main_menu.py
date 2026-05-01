"""
لوحة المفاتيح الرئيسية - FitCoach Bot
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update, CallbackQuery


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """القائمة الرئيسية"""
    keyboard = [
        [
            InlineKeyboardButton("📊 لوحة التحكم", callback_data="dashboard"),
            InlineKeyboardButton("🏋️ التمارين", callback_data="workout_menu")
        ],
        [
            InlineKeyboardButton("🍽️ التغذية", callback_data="nutrition_menu"),
            InlineKeyboardButton("📈 التتبع", callback_data="tracking_menu")
        ],
        [
            InlineKeyboardButton("📋 التقارير", callback_data="reports_menu"),
            InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings_menu")
        ],
        [
            InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_to_main_keyboard() -> InlineKeyboardMarkup:
    """زر العودة للقائمة الرئيسية"""
    keyboard = [
        [InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_back_keyboard(callback_data: str = "main_menu") -> InlineKeyboardMarkup:
    """زر العودة"""
    keyboard = [
        [InlineKeyboardButton("🔙 رجوع", callback_data=callback_data)]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_profile_menu_keyboard() -> InlineKeyboardMarkup:
    """قائمة الملف الشخصي"""
    keyboard = [
        [
            InlineKeyboardButton("👤 عرض الملف الشخصي", callback_data="profile_view"),
            InlineKeyboardButton("✏️ تعديل الملف الشخصي", callback_data="profile_edit")
        ],
        [
            InlineKeyboardButton("📐 قياساتي", callback_data="profile_measurements"),
            InlineKeyboardButton("🎯 تغيير الهدف", callback_data="profile_goal")
        ],
        [
            InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_workout_menu_keyboard() -> InlineKeyboardMarkup:
    """قائمة التمارين"""
    keyboard = [
        [
            InlineKeyboardButton("📋 جدول اليوم", callback_data="workout_today"),
            InlineKeyboardButton("💪 بدء التمرين", callback_data="workout_start")
        ],
        [
            InlineKeyboardButton("📅 جدولي الأسبوعي", callback_data="workout_schedule"),
            InlineKeyboardButton("🔄 تحديث الجدول", callback_data="workout_refresh")
        ],
        [
            InlineKeyboardButton("➕ إضافة تمرين", callback_data="workout_add"),
            InlineKeyboardButton("📜 تاريخ التمارين", callback_data="workout_history")
        ],
        [
            InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_muscle_group_keyboard() -> InlineKeyboardMarkup:
    """أزرار مجموعات العضلات"""
    keyboard = [
        [
            InlineKeyboardButton("💪 صدر", callback_data="muscle_chest"),
            InlineKeyboardButton("🔙 ظهر", callback_data="muscle_back")
        ],
        [
            InlineKeyboardButton("🎯 أكتاف", callback_data="muscle_shoulders"),
            InlineKeyboardButton("💪 عضلات الذراع", callback_data="muscle_arms")
        ],
        [
            InlineKeyboardButton("🦵 ساقيك", callback_data="muscle_legs"),
            InlineKeyboardButton("🎯 بطن", callback_data="muscle_abs")
        ],
        [
            InlineKeyboardButton("🔙 رجوع", callback_data="workout_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_nutrition_menu_keyboard() -> InlineKeyboardMarkup:
    """قائمة التغذية"""
    keyboard = [
        [
            InlineKeyboardButton("🍳 إضافة وجبة", callback_data="nutrition_add"),
            InlineKeyboardButton("📋 وجبات اليوم", callback_data="nutrition_today")
        ],
        [
            InlineKeyboardButton("📊 ملخص التغذية", callback_data="nutrition_summary"),
            InlineKeyboardButton("🎯 أهدافي الغذائية", callback_data="nutrition_goals")
        ],
        [
            InlineKeyboardButton("🍽️ اقتراح وجبات", callback_data="nutrition_suggest"),
            InlineKeyboardButton("📖 قاعدة الوجبات", callback_data="nutrition_database")
        ],
        [
            InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_meal_type_keyboard() -> InlineKeyboardMarkup:
    """أزرار نوع الوجبة"""
    keyboard = [
        [
            InlineKeyboardButton("🍳 إفطار", callback_data="meal_breakfast"),
            InlineKeyboardButton("🥗 غداء", callback_data="meal_lunch")
        ],
        [
            InlineKeyboardButton("🍽️ عشاء", callback_data="meal_dinner"),
            InlineKeyboardButton("🍼 وجبة خفيفة", callback_data="meal_snack")
        ],
        [
            InlineKeyboardButton("🔙 رجوع", callback_data="nutrition_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_tracking_menu_keyboard() -> InlineKeyboardMarkup:
    """قائمة التتبع"""
    keyboard = [
        [
            InlineKeyboardButton("⚖️ تسجيل الوزن", callback_data="track_weight"),
            InlineKeyboardButton("💧 تسجيل الماء", callback_data="track_water")
        ],
        [
            InlineKeyboardButton("😴 تسجيل النوم", callback_data="track_sleep"),
            InlineKeyboardButton("📊 تتبع اليوم", callback_data="track_today")
        ],
        [
            InlineKeyboardButton("📈 تقدمي", callback_data="track_progress"),
            InlineKeyboardButton("📉Charts", callback_data="track_charts")
        ],
        [
            InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_reports_menu_keyboard() -> InlineKeyboardMarkup:
    """قائمة التقارير"""
    keyboard = [
        [
            InlineKeyboardButton("📅 التقرير اليومي", callback_data="report_daily"),
            InlineKeyboardButton("📆 التقرير الأسبوعي", callback_data="report_weekly")
        ],
        [
            InlineKeyboardButton("📆 التقرير الشهري", callback_data="report_monthly"),
            InlineKeyboardButton("📊 مقارنة", callback_data="report_compare")
        ],
        [
            InlineKeyboardButton("📈 إحصائياتي", callback_data="report_stats"),
            InlineKeyboardButton("🏆 إنجازاتي", callback_data="report_achievements")
        ],
        [
            InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_settings_menu_keyboard() -> InlineKeyboardMarkup:
    """قائمة الإعدادات"""
    keyboard = [
        [
            InlineKeyboardButton("🔔 التنبيهات", callback_data="settings_notifications"),
            InlineKeyboardButton("⏰ أوقات التذكير", callback_data="settings_reminders")
        ],
        [
            InlineKeyboardButton("🌐 اللغة", callback_data="settings_language"),
            InlineKeyboardButton("📏 نظام الوحدات", callback_data="settings_units")
        ],
        [
            InlineKeyboardButton("👤 حسابي", callback_data="settings_account"),
            InlineKeyboardButton("ℹ️ مساعدة", callback_data="settings_help")
        ],
        [
            InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_experience_level_keyboard() -> InlineKeyboardMarkup:
    """أزرار مستوى الخبرة"""
    keyboard = [
        [
            InlineKeyboardButton("🌱 مبتدئ", callback_data="exp_beginner"),
            InlineKeyboardButton("🏃 متوسط", callback_data="exp_intermediate")
        ],
        [
            InlineKeyboardButton("💪 متقدم", callback_data="exp_advanced")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_goal_type_keyboard() -> InlineKeyboardMarkup:
    """أزرار نوع الهدف"""
    keyboard = [
        [
            InlineKeyboardButton("🔥 ضخامة عضلية", callback_data="goal_bulking"),
            InlineKeyboardButton("❄️ تنشيف", callback_data="goal_cutting")
        ],
        [
            InlineKeyboardButton("🔄 إعادة تركيب", callback_data="goal_recomp")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_activity_level_keyboard() -> InlineKeyboardMarkup:
    """أزرار مستوى النشاط"""
    keyboard = [
        [
            InlineKeyboardButton("🛋️ خامل", callback_data="activity_sedentary"),
            InlineKeyboardButton("🚶 نشاط خفيف", callback_data="activity_light")
        ],
        [
            InlineKeyboardButton("🏃 نشاط متوسط", callback_data="activity_moderate"),
            InlineKeyboardButton("🔥 نشط جداً", callback_data="activity_active")
        ],
        [
            InlineKeyboardButton("🏆 رياضي محترف", callback_data="activity_athlete")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_confirmation_keyboard(confirm_data: str, cancel_data: str = "cancel") -> InlineKeyboardMarkup:
    """أزرار التأكيد والإلغاء"""
    keyboard = [
        [
            InlineKeyboardButton("✅ تأكيد", callback_data=confirm_data),
            InlineKeyboardButton("❌ إلغاء", callback_data=cancel_data)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_yes_no_keyboard(yes_data: str, no_data: str) -> InlineKeyboardMarkup:
    """أزرار نعم/لا"""
    keyboard = [
        [
            InlineKeyboardButton("✅ نعم", callback_data=yes_data),
            InlineKeyboardButton("❌ لا", callback_data=no_data)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_water_unit_keyboard() -> InlineKeyboardMarkup:
    """أزرار وحدات الماء"""
    keyboard = [
        [
            InlineKeyboardButton("🥤 كوب (250 مل)", callback_data="water_250"),
            InlineKeyboardButton("🍶 زجاجة (500 مل)", callback_data="water_500")
        ],
        [
            InlineKeyboardButton("🫗 لتر كامل", callback_data="water_1000"),
            InlineKeyboardButton("✏️ أدخل كمية", callback_data="water_custom")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_dashboard_keyboard() -> InlineKeyboardMarkup:
    """أزرار لوحة التحكم"""
    keyboard = [
        [
            InlineKeyboardButton("🍽️ وجباتي", callback_data="dashboard_meals"),
            InlineKeyboardButton("🏋️ تماريني", callback_data="dashboard_workouts")
        ],
        [
            InlineKeyboardButton("💧 مياهي", callback_data="dashboard_water"),
            InlineKeyboardButton("😴 نومي", callback_data="dashboard_sleep")
        ],
        [
            InlineKeyboardButton("⚖️ وزنـي", callback_data="dashboard_weight"),
            InlineKeyboardButton("📈 تقدمي", callback_data="dashboard_progress")
        ],
        [
            InlineKeyboardButton("🔙 رجوع", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_workout_exercise_keyboard(exercises: list, page: int = 0) -> InlineKeyboardMarkup:
    """أزرار التمارين مع التصفح"""
    keyboard = []
    per_page = 6

    start = page * per_page
    end = start + per_page
    page_exercises = exercises[start:end]

    for ex in page_exercises:
        keyboard.append([
            InlineKeyboardButton(
                f"💪 {ex.name_ar}",
                callback_data=f"exercise_{ex.id}"
            )
        ])

    # أزرار التنقل
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ السابق", callback_data=f"exercises_page_{page-1}"))

    if end < len(exercises):
        nav_buttons.append(InlineKeyboardButton("التالي ➡️", callback_data=f"exercises_page_{page+1}"))

    if nav_buttons:
        keyboard.append(nav_buttons)

    keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data="workout_menu")])
    return InlineKeyboardMarkup(keyboard)


def get_workout_sets_reps_keyboard() -> InlineKeyboardMarkup:
    """أزرار المجموعات والتكرارات"""
    keyboard = [
        [
            InlineKeyboardButton("3 × 12", callback_data="workout_3x12"),
            InlineKeyboardButton("4 × 10", callback_data="workout_4x10")
        ],
        [
            InlineKeyboardButton("4 × 8", callback_data="workout_4x8"),
            InlineKeyboardButton("5 × 5", callback_data="workout_5x5")
        ],
        [
            InlineKeyboardButton("✏️ مخصص", callback_data="workout_custom_sr")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_notification_toggle_keyboard(current_state: bool) -> InlineKeyboardMarkup:
    """أزرار تفعيل/إلغاء التنبيهات"""
    keyboard = [
        [
            InlineKeyboardButton(
                f"🔔 تذكير الماء: {'مفعل' if current_state else 'معطل'}",
                callback_data="toggle_water_reminder"
            ),
            InlineKeyboardButton(
                f"🍽️ تذكير الوجبات: {'مفعل' if current_state else 'معطل'}",
                callback_data="toggle_meal_reminder"
            )
        ],
        [
            InlineKeyboardButton(
                f"🏋️ تذكير التمرين: {'مفعل' if current_state else 'معطل'}",
                callback_data="toggle_workout_reminder"
            )
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_language_keyboard() -> InlineKeyboardMarkup:
    """أزرار اللغات"""
    keyboard = [
        [
            InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_profile_edit_keyboard() -> InlineKeyboardMarkup:
    """أزرار تعديل الملف الشخصي"""
    keyboard = [
        [
            InlineKeyboardButton("🎂 العمر", callback_data="edit_age"),
            InlineKeyboardButton("📏 الطول", callback_data="edit_height")
        ],
        [
            InlineKeyboardButton("⚖️ الوزن", callback_data="edit_weight"),
            InlineKeyboardButton("📐 نسبة الدهون", callback_data="edit_bodyfat")
        ],
        [
            InlineKeyboardButton("⭐ مستوى الخبرة", callback_data="edit_experience"),
            InlineKeyboardButton("📅 أيام التمرين", callback_data="edit_workout_days")
        ],
        [
            InlineKeyboardButton("🔙 رجوع", callback_data="profile_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

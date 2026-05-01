"""
أدوات مساعدة
"""
from datetime import datetime


def format_date(date_obj, format_string='%Y-%m-%d') -> str:
    """تنسيق التاريخ"""
    return date_obj.strftime(format_string)


def format_time(time_obj, format_string='%H:%M') -> str:
    """تنسيق الوقت"""
    return time_obj.strftime(format_string)


def progress_bar(percentage: float, length: int = 10) -> str:
    """إنشاء شريط تقدم نصي"""
    filled = min(length, max(0, int(percentage / (100 / length))))
    empty = length - filled
    return "█" * filled + "░" * empty


def calculate_bmi(weight: float, height: float) -> float:
    """حساب مؤشر كتلة الجسم"""
    height_m = height / 100
    return weight / (height_m ** 2)


def get_bmi_category(bmi: float) -> str:
    """الحصول على تصنيف BMI"""
    if bmi < 18.5:
        return "نقص في الوزن"
    elif 18.5 <= bmi < 25:
        return "طبيعي"
    elif 25 <= bmi < 30:
        return "زيادة في الوزن"
    else:
        return "سمنة"


def calculate_lean_mass(weight: float, body_fat: float) -> float:
    """حساب الكتلة الخالية من الدهون"""
    return weight * (1 - body_fat / 100)


def calculate_fat_mass(weight: float, body_fat: float) -> float:
    """حساب كتلة الدهون"""
    return weight * (body_fat / 100)


def safe_divide(a, b, default=0):
    """قسمة آمنة"""
    try:
        return a / b if b != 0 else default
    except:
        return default


def format_number(num: float, decimals: int = 1) -> str:
    """تنسيق الأرقام"""
    return f"{num:.{decimals}f}"


def emoji_number(num: int) -> str:
    """تحويل الرقم إلى رموز تعبيرية"""
    digits = {
        '0': '0️⃣', '1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣',
        '5': '5️⃣', '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣'
    }
    return ''.join([digits.get(d, d) for d in str(num)])

"""
قاعدة بيانات التمارين - FitCoach Bot
تحتوي على قائمة شاملة من التمارين مع البدائل
"""
from typing import List, Dict

# قائمة التمارين الرئيسية
EXERCISES = [
    # ===== صدر =====
    {
        "id": 1,
        "name_ar": "بنش بريس",
        "name_en": "Bench Press",
        "muscle_group": "chest",
        "equipment": "free_weights",
        "difficulty": "intermediate",
        "description": "تمرين أساسي لبناء عضلات الصدر",
        "instructions": "1. استلق على المقعد\n2. امسك البار بمسافة أوسع من الكتفين\n3. أنزل البار حتى منتصف الصدر\n4. ارفعه ببطء",
        "video_url": "https://www.youtube.com/watch?v=SCVCLChPQFY",
        "calories_per_minute": 6.0,
        "alternatives": [2, 3, 4]
    },
    {
        "id": 2,
        "name_ar": "بنش بريس مائل",
        "name_en": "Incline Bench Press",
        "muscle_group": "chest",
        "equipment": "free_weights",
        "difficulty": "intermediate",
        "description": "يركز على الصدر العلوي",
        "instructions": "1. اضبط المقعد بزاوية 30-45 درجة\n2. امسك البار\n3. أنزله لأعلى الصدر\n4. ارفعه ببطء",
        "video_url": "https://www.youtube.com/watch?v=DbFgADa2PL8",
        "calories_per_minute": 6.0,
        "alternatives": [1, 3, 4]
    },
    {
        "id": 3,
        "name_ar": "دمبل فلاي",
        "name_en": "Dumbbell Fly",
        "muscle_group": "chest",
        "equipment": "free_weights",
        "difficulty": "beginner",
        "description": "تمرين إيزوليشن للصدر",
        "instructions": "1. استلق على المقعد مع دمبلز\n2. افرد ذراعيك\n3. اخفضهما ببطء في شكل قوس\n4. ارجع للوضع الأول",
        "video_url": "https://www.youtube.com/watch?v=Iwe6AmxVf7o",
        "calories_per_minute": 5.0,
        "alternatives": [1, 2, 4]
    },
    {
        "id": 4,
        "name_ar": "كبل فلاي",
        "name_en": "Cable Fly",
        "muscle_group": "chest",
        "equipment": "cable",
        "difficulty": "beginner",
        "description": "تمرين كابل لإحساس أفضل",
        "instructions": "1. قف أمام جهاز الكابل\n2. امسك المقابض\n3. أحضر يديك للأمام\n4. ارجع ببطء",
        "video_url": "https://www.youtube.com/watch?v=Iwe6AmxVf7o",
        "calories_per_minute": 5.0,
        "alternatives": [1, 2, 3]
    },
    {
        "id": 5,
        "name_ar": "تمارين الضغط",
        "name_en": "Push-ups",
        "muscle_group": "chest",
        "equipment": "bodyweight",
        "difficulty": "beginner",
        "description": "تمرين وزن الجسم الكلاسيكي",
        "instructions": "1. اقبل على وضعية الضغط\n2. أنزل صدرك للأرض\n3. ادفع نفسك للأعلى\n4. كرر",
        "video_url": "https://www.youtube.com/watch?v=IODxDxXJJoc",
        "calories_per_minute": 7.0,
        "alternatives": [1, 2]
    },

    # ===== ظهر =====
    {
        "id": 6,
        "name_ar": "ديدليفت",
        "name_en": "Deadlift",
        "muscle_group": "back",
        "equipment": "free_weights",
        "difficulty": "advanced",
        "description": "تمرين متكامل للظهر والساقين",
        "instructions": "1. قف أمام البار\n2. انحنِ وأمسك البار\n3. ارفع البار مع الحفاظ على استقامة الظهر\n4. أنزله ببطء",
        "video_url": "https://www.youtube.com/watch?v=op9kVnSso6Q",
        "calories_per_minute": 8.0,
        "alternatives": [7, 8]
    },
    {
        "id": 7,
        "name_ar": "بول أب",
        "name_en": "Pull-ups",
        "muscle_group": "back",
        "equipment": "bodyweight",
        "difficulty": "intermediate",
        "description": "تمرين ممتاز للظهر العلوي",
        "instructions": "1. تعلق على البار\n2. اسحب نفسك للأعلى\n3. اقترب ذقنك من البار\n4. أنزل نفسك ببطء",
        "video_url": "https://www.youtube.com/watch?v=eGo4IY1E5AU",
        "calories_per_minute": 7.0,
        "alternatives": [8, 9]
    },
    {
        "id": 8,
        "name_ar": "لات بول",
        "name_en": "Lat Pulldown",
        "muscle_group": "back",
        "equipment": "machine",
        "difficulty": "beginner",
        "description": "بديل للبول أب",
        "instructions": "1. اجلس واضبط الفخذ\n2. امسك البار العريض\n3. اسحب البار لصدرك\n4. ارجع ببطء",
        "video_url": "https://www.youtube.com/watch?v=CAO27URmWyg",
        "calories_per_minute": 5.0,
        "alternatives": [6, 7, 9]
    },
    {
        "id": 9,
        "name_ar": "صف واحديت",
        "name_en": "Barbell Row",
        "muscle_group": "back",
        "equipment": "free_weights",
        "difficulty": "intermediate",
        "description": "تمرين للظهر العلوي",
        "instructions": "1. انحنِ للأمام مع إبقاء الظهر مستقيم\n2. امسك البار\n3. اسحب البار لبطنك\n4. ارجع ببطء",
        "video_url": "https://www.youtube.com/watch?v=FImkeTByc38",
        "calories_per_minute": 6.0,
        "alternatives": [6, 7, 8]
    },
    {
        "id": 10,
        "name_ar": "سيتد روز",
        "name_en": "Seated Cable Row",
        "muscle_group": "back",
        "equipment": "cable",
        "difficulty": "beginner",
        "description": "تمرين كابل للظهر",
        "instructions": "1. اجلس على الجهاز\n2. امسك المقبض\n3. اسحب نحو بطنك\n4. ارجع ببطء",
        "video_url": "https://www.youtube.com/watch?v=GZbfZ033f74",
        "calories_per_minute": 5.0,
        "alternatives": [8, 9]
    },

    # ===== أكتاف =====
    {
        "id": 11,
        "name_ar": "أوفرهيد بريس",
        "name_en": "Overhead Press",
        "muscle_group": "shoulders",
        "equipment": "free_weights",
        "difficulty": "intermediate",
        "description": "تمرين رئيسي للأكتاف",
        "instructions": "1. امسك البار عند الكتفين\n2. اضغط البار للأعلى\n3. اقترب ذراعيك من أذنيك\n4. أنزله ببطء",
        "video_url": "https://www.youtube.com/watch?v=2yjwXT8nA4s",
        "calories_per_minute": 6.0,
        "alternatives": [12, 13]
    },
    {
        "id": 12,
        "name_ar": "دمبل شولدر بريس",
        "name_en": "Dumbbell Shoulder Press",
        "muscle_group": "shoulders",
        "equipment": "free_weights",
        "difficulty": "beginner",
        "description": "تمرين أكتاف بالدمبل",
        "instructions": "1. اجلس أو قف بدمبلز عند الكتفين\n2. اضغطهما للأعلى\n3. اقتربهما من بعض\n4. أنزلهما ببطء",
        "video_url": "https://www.youtube.com/watch?v=qEwKCR5JCog",
        "calories_per_minute": 5.0,
        "alternatives": [11, 13]
    },
    {
        "id": 13,
        "name_ar": "لاترال ريز",
        "name_en": "Lateral Raise",
        "muscle_group": "shoulders",
        "equipment": "free_weights",
        "difficulty": "beginner",
        "description": "تمرين للجانب الجانبي من الأكتاف",
        "instructions": "1. قف بدمبلز بجانبك\n2. ارفعهما للأطراف\n3. حافظ على ثني خفيف في المرفقين\n4. أنزلهما ببطء",
        "video_url": "https://www.youtube.com/watch?v=3VcKaXpzqDa",
        "calories_per_minute": 4.0,
        "alternatives": [11, 12]
    },
    {
        "id": 14,
        "name_ar": "فرونت ريز",
        "name_en": "Front Raise",
        "muscle_group": "shoulders",
        "equipment": "free_weights",
        "difficulty": "beginner",
        "description": "تمرين للأمام الجانبي من الأكتاف",
        "instructions": "1. قف بدمبلز أمامك\n2. ارفع إحداهما للأمام\n3. حافظ على استقامة الذراع\n4. أنزلها ببطء",
        "video_url": "https://www.youtube.com/watch?v=3VcKaXpzqDa",
        "calories_per_minute": 4.0,
        "alternatives": [11, 12, 13]
    },
    {
        "id": 15,
        "name_ar": "فيس ريز",
        "name_en": "Face Pull",
        "muscle_group": "shoulders",
        "equipment": "cable",
        "difficulty": "beginner",
        "description": "تمرين للخلف الجانبي والأكتاف",
        "instructions": "1. اضبط الكابل عند الوجه\n2. اسحب للخلف\n3. افرقع مرفقيك\n4. ارجع ببطء",
        "video_url": "https://www.youtube.com/watch?v=rep-ugpYlJw",
        "calories_per_minute": 4.0,
        "alternatives": [13, 14]
    },

    # ===== بايسبس =====
    {
        "id": 16,
        "name_ar": "كورل باربل",
        "name_en": "Barbell Curl",
        "muscle_group": "biceps",
        "equipment": "free_weights",
        "difficulty": "beginner",
        "description": "تمرين أساسي للبايسبس",
        "instructions": "1. امسك البار بمسافة الكتفين\n2. اثني الكوعين\n3. ارفع البار للكتفين\n4. أنزله ببطء",
        "video_url": "https://www.youtube.com/watch?v=ykJmrZ5v0Oo",
        "calories_per_minute": 4.0,
        "alternatives": [17, 18]
    },
    {
        "id": 17,
        "name_ar": "دمبل كورل",
        "name_en": "Dumbbell Curl",
        "muscle_group": "biceps",
        "equipment": "free_weights",
        "difficulty": "beginner",
        "description": "تمرين بايسبس بالدمبل",
        "instructions": "1. قف بدمبلز بأذرع ممدودة\n2. اثني الكوع\n3. ارفع الدمبل للكتف\n4. أنزله ببطء",
        "video_url": "https://www.youtube.com/watch?v=ykJmrZ5v0Oo",
        "calories_per_minute": 4.0,
        "alternatives": [16, 18]
    },
    {
        "id": 18,
        "name_ar": "هامر كورل",
        "name_en": "Hammer Curl",
        "muscle_group": "biceps",
        "equipment": "free_weights",
        "difficulty": "beginner",
        "description": "تمرين البايسبس مع براسيس",
        "instructions": "1. قف بدمبلز موجه للأمام\n2. اثني الكوع\n3. ارفع الدمبل\n4. أنزله ببطء",
        "video_url": "https://www.youtube.com/watch?v=ykJmrZ5v0Oo",
        "calories_per_minute": 4.0,
        "alternatives": [16, 17]
    },
    {
        "id": 19,
        "name_ar": "بريتشر كورل",
        "name_en": "Preacher Curl",
        "muscle_group": "biceps",
        "equipment": "machine",
        "difficulty": "intermediate",
        "description": "تركيز على البايسبس الطويل",
        "instructions": "1. ضع ذراعيك على الوسادة\n2. اثني الكوع\n3. ارفع الوزن\n4. أنزله ببطء",
        "video_url": "https://www.youtube.com/watch?v=ykJmrZ5v0Oo",
        "calories_per_minute": 4.0,
        "alternatives": [16, 17]
    },

    # ===== ترايسبس =====
    {
        "id": 20,
        "name_ar": "كلوز جريب",
        "name_en": "Close Grip Bench Press",
        "muscle_group": "triceps",
        "equipment": "free_weights",
        "difficulty": "intermediate",
        "description": "تمرين مركب للترايسبس",
        "instructions": "1. استلق على المقعد\n2. امسك البار بمسافة ضيقة\n3. أنزل البار للصدر\n4. ارفعه",
        "video_url": "https://www.youtube.com/watch?v=nF9AoN2eYOA",
        "calories_per_minute": 6.0,
        "alternatives": [21, 22]
    },
    {
        "id": 21,
        "name_ar": "ترايست ديب",
        "name_en": "Tricep Dips",
        "muscle_group": "triceps",
        "equipment": "bodyweight",
        "difficulty": "intermediate",
        "description": "تمرين وزن الجسم للترايسبس",
        "instructions": "1. ضع يديك على مقعد خلفك\n2. أنزل جسمك\n3. اثني كوعيك\n4. ادفع نفسك للأعلى",
        "video_url": "https://www.youtube.com/watch?v=nF9AoN2eYOA",
        "calories_per_minute": 6.0,
        "alternatives": [20, 22]
    },
    {
        "id": 22,
        "name_ar": "ترايست بوز داون",
        "name_en": "Tricep Pushdown",
        "muscle_group": "triceps",
        "equipment": "cable",
        "difficulty": "beginner",
        "description": "تمرين كابل للترايسبس",
        "instructions": "1. قف أمام الكابل\n2. امسك المقبض\n3. اثني الكوع\n4. مدد ذراعيك",
        "video_url": "https://www.youtube.com/watch?v=nF9AoN2eYOA",
        "calories_per_minute": 4.0,
        "alternatives": [20, 21]
    },
    {
        "id": 23,
        "name_ar": "سكيولز",
        "name_en": "Skull Crushers",
        "muscle_group": "triceps",
        "equipment": "free_weights",
        "difficulty": "advanced",
        "description": "تمرين متقدم للترايسبس",
        "instructions": "1. استلق وأمسك البار فوق صدرك\n2. أنزل البار نحو جبهتك\n3. اثني كوعيك\n4. ارفعه",
        "video_url": "https://www.youtube.com/watch?v=nF9AoN2eYOA",
        "calories_per_minute": 5.0,
        "alternatives": [20, 22]
    },

    # ===== ساقيك =====
    {
        "id": 24,
        "name_ar": "سكوات",
        "name_en": "Barbell Squat",
        "muscle_group": "legs",
        "equipment": "free_weights",
        "difficulty": "intermediate",
        "description": "الملك - تمرين متكامل للساقين",
        "instructions": "1. ضع البار على كتفيك\n2. انزل للأمام والرجل\n3. حافظ على استقامة الظهر\n4. قف",
        "video_url": "https://www.youtube.com/watch?v=ultWZbUMPL8",
        "calories_per_minute": 8.0,
        "alternatives": [25, 26]
    },
    {
        "id": 25,
        "name_ar": "ليج بريس",
        "name_en": "Leg Press",
        "muscle_group": "legs",
        "equipment": "machine",
        "difficulty": "beginner",
        "description": "بديل آمن للسكوات",
        "instructions": "1. اجلس في الجهاز\n2. ضع قدميك على القاعدة\n3. أنزل الوزن\n4. ارفعه",
        "video_url": "https://www.youtube.com/watch?v=IZxyjW7MPJQ",
        "calories_per_minute": 6.0,
        "alternatives": [24, 26]
    },
    {
        "id": 26,
        "name_ar": "ليج اكستنشن",
        "name_en": "Leg Extension",
        "muscle_group": "legs",
        "equipment": "machine",
        "difficulty": "beginner",
        "description": "تمرين لعظمة الفخذ الرباعية",
        "instructions": "1. اجلس في الجهاز\n2. علق قدميك\n3. مد ساقيك\n4. ارجع ببطء",
        "video_url": "https://www.youtube.com/watch?v=ELDK1mQ4GFI",
        "calories_per_minute": 4.0,
        "alternatives": [24, 25, 27]
    },
    {
        "id": 27,
        "name_ar": "ليج كيرل",
        "name_en": "Leg Curl",
        "muscle_group": "legs",
        "equipment": "machine",
        "difficulty": "beginner",
        "description": "تمرين لأوتار الركبة",
        "instructions": "1. استلق على المعدة\n2. ضع كعبيك تحت الوسادة\n3. اثني ركبتيك\n4. ارجع ببطء",
        "video_url": "https://www.youtube.com/watch?v=ELDK1mQ4GFI",
        "calories_per_minute": 4.0,
        "alternatives": [24, 25, 26]
    },
    {
        "id": 28,
        "name_ar": "كالم ريس",
        "name_en": "Calf Raise",
        "muscle_group": "legs",
        "equipment": "machine",
        "difficulty": "beginner",
        "description": "تمرين لعضلات الساق",
        "instructions": "1. قف على الجهاز\n2. ارفع كعبيك\n3. توقف قليلاً\n4. أنزلهما ببطء",
        "video_url": "https://www.youtube.com/watch?v=gwLzBJYoWlI",
        "calories_per_minute": 3.0,
        "alternatives": [26, 27]
    },
    {
        "id": 29,
        "name_ar": "لونج",
        "name_en": "Lunges",
        "muscle_group": "legs",
        "equipment": "bodyweight",
        "difficulty": "beginner",
        "description": "تمرين للساقين بوزن الجسم",
        "instructions": "1. قف بشكل مستقيم\n2. خطوطة كبيرة للأمام\n3. أنزل ركبتيك\n4. ارجع وكرر",
        "video_url": "https://www.youtube.com/watch?v=D7KaRcUTQeE",
        "calories_per_minute": 6.0,
        "alternatives": [24, 25]
    },

    # ===== بطن =====
    {
        "id": 30,
        "name_ar": "كرانش",
        "name_en": "Crunches",
        "muscle_group": "abs",
        "equipment": "bodyweight",
        "difficulty": "beginner",
        "description": "تمرين أساسي للبطن",
        "instructions": "1. استلق على ظهرك\n2. ضع يديك خلف رأسك\n3. ارفع كتفك للأعلى\n4. أنزله ببطء",
        "video_url": "https://www.youtube.com/watch?v=Xyd_fa5zoEU",
        "calories_per_minute": 4.0,
        "alternatives": [31, 32]
    },
    {
        "id": 31,
        "name_ar": "بلانك",
        "name_en": "Plank",
        "muscle_group": "abs",
        "equipment": "bodyweight",
        "difficulty": "beginner",
        "description": "تمرين متساوي القياس للبطن",
        "instructions": "1. اقبل على ساعدين ورجولن\n2. حافظ على خط مستقيم\n3. شد بطنك\n4. انتظر",
        "video_url": "https://www.youtube.com/watch?v=ASdvN_XEl_c",
        "calories_per_minute": 5.0,
        "alternatives": [30, 32]
    },
    {
        "id": 32,
        "name_ar": "ليج ريز",
        "name_en": "Leg Raise",
        "muscle_group": "abs",
        "equipment": "bodyweight",
        "difficulty": "intermediate",
        "description": "تمرين للبطن السفلي",
        "instructions": "1. استلق على ظهرك\n2. ارفع رجولك للأعلى\n3. أنزلهما ببطء\n4. لا تلمس الأرض",
        "video_url": "https://www.youtube.com/watch?v=l4kQ4uNj6sQ",
        "calories_per_minute": 5.0,
        "alternatives": [30, 31]
    },
    {
        "id": 33,
        "name_ar": "ماونتن كلمبر",
        "name_en": "Mountain Climbers",
        "muscle_group": "abs",
        "equipment": "bodyweight",
        "difficulty": "intermediate",
        "description": "تمرين ديناميكي للبطن",
        "instructions": "1. وضعية دفع\n2. أحضر ركبتك للصدر\n3. بدل بين الساقين\n4.كرر",
        "video_url": "https://www.youtube.com/watch?v=nmwgirgXTSU",
        "calories_per_minute": 10.0,
        "alternatives": [30, 31, 32]
    },
    {
        "id": 34,
        "name_ar": "اب دومينو",
        "name_en": "Ab Wheel Rollout",
        "muscle_group": "abs",
        "equipment": "machine",
        "difficulty": "advanced",
        "description": "تمرين متقدم للبطن",
        "instructions": "1. اركع مع عجلة البطن\n2. ادفع العجلة للأمام\n3. حافظ على استقامة جسمك\n4. ارجع",
        "video_url": "https://www.youtube.com/watch?v=xd-UJyBsuXI",
        "calories_per_minute": 7.0,
        "alternatives": [31, 32]
    }
]


def get_exercise_by_id(exercise_id: int) -> Dict:
    """الحصول على تمرين بالمعرف"""
    for ex in EXERCISES:
        if ex["id"] == exercise_id:
            return ex
    return None


def get_exercises_by_muscle(muscle_group: str) -> List[Dict]:
    """الحصول على التمارين حسب مجموعة العضلات"""
    return [ex for ex in EXERCISES if ex["muscle_group"] == muscle_group]


def get_exercises_by_equipment(equipment: str) -> List[Dict]:
    """الحصول على التمارين حسب نوع المعدات"""
    return [ex for ex in EXERCISES if ex["equipment"] == equipment]


def get_exercises_by_difficulty(difficulty: str) -> List[Dict]:
    """الحصول على التمارين حسب الصعوبة"""
    return [ex for ex in EXERCISES if ex["difficulty"] == difficulty]


def search_exercises(query: str) -> List[Dict]:
    """البحث عن تمارين"""
    query_lower = query.lower()
    results = []
    for ex in EXERCISES:
        if query_lower in ex["name_ar"].lower() or query_lower in ex["name_en"].lower():
            results.append(ex)
    return results


def get_alternative_exercises(exercise_id: int) -> List[Dict]:
    """الحصول على التمارين البديلة"""
    exercise = get_exercise_by_id(exercise_id)
    if not exercise or "alternatives" not in exercise:
        return []

    alternatives = []
    for alt_id in exercise["alternatives"]:
        alt = get_exercise_by_id(alt_id)
        if alt:
            alternatives.append(alt)
    return alternatives


def get_muscle_group_name(muscle_group: str) -> str:
    """الحصول على اسم مجموعة العضلات بالعربية"""
    names = {
        "chest": "صدر",
        "back": "ظهر",
        "shoulders": "أكتاف",
        "biceps": "بايسبس",
        "triceps": "ترايسبس",
        "legs": "ساقيك",
        "abs": "بطن"
    }
    return names.get(muscle_group, muscle_group)


def get_workout_template(user_level: str, goal: str, workout_days: int) -> Dict:
    """إنشاء قالب جدول تدريب"""
    templates = {
        3: {  # 3 أيام
            "beginner": {
                "day_1": ["chest", "triceps"],
                "day_2": ["back", "biceps"],
                "day_3": ["legs", "abs"]
            },
            "intermediate": {
                "day_1": ["chest", "shoulders", "triceps"],
                "day_2": ["back", "biceps"],
                "day_3": ["legs", "abs"]
            },
            "advanced": {
                "day_1": ["chest", "shoulders"],
                "day_2": ["back", "biceps"],
                "day_3": ["legs", "abs"],
                "day_4": ["chest", "triceps"],
                "day_5": ["back", "shoulders"]
            }
        },
        4: {
            "beginner": {
                "day_1": ["chest", "back"],
                "day_2": ["shoulders", "biceps"],
                "day_3": ["legs", "triceps"],
                "day_4": ["abs", "cardio"]
            },
            "intermediate": {
                "day_1": ["chest", "triceps"],
                "day_2": ["back", "biceps"],
                "day_3": ["shoulders", "legs"],
                "day_4": ["abs", "cardio"]
            }
        },
        5: {
            "beginner": {
                "day_1": ["chest"],
                "day_2": ["back"],
                "day_3": ["shoulders"],
                "day_4": ["legs"],
                "day_5": ["biceps", "triceps", "abs"]
            },
            "intermediate": {
                "day_1": ["chest", "triceps"],
                "day_2": ["back", "biceps"],
                "day_3": ["legs"],
                "day_4": ["shoulders", "abs"],
                "day_5": ["chest", "back"]
            },
            "advanced": {
                "day_1": ["chest"],
                "day_2": ["back"],
                "day_3": ["legs"],
                "day_4": ["shoulders"],
                "day_5": ["biceps", "triceps"],
                "day_6": ["abs", "cardio"]
            }
        }
    }

    # اختيار القالب المناسب
    day_key = min(workout_days, 5)
    level_key = user_level if user_level in templates[day_key] else "beginner"

    return templates[day_key].get(level_key, templates[day_key]["beginner"])


def format_exercise_text(exercise: Dict) -> str:
    """تنسيق نص التمرين"""
    text = f"💪 <b>{exercise['name_ar']}</b>\n"
    text += f"   ({exercise['name_en']})\n\n"
    text += f"📍 <b>العضلة:</b> {get_muscle_group_name(exercise['muscle_group'])}\n"
    text += f"🏷️ <b>المعدات:</b> {get_equipment_name(exercise['equipment'])}\n"
    text += f"⭐ <b>الصعوبة:</b> {get_difficulty_name(exercise['difficulty'])}\n\n"
    text += f"📝 <b>التعليمات:</b>\n{exercise['instructions']}"

    if exercise.get('video_url'):
        text += f"\n\n🎬 <a href='{exercise['video_url']}'>شاهد الفيديو</a>"

    return text


def get_equipment_name(equipment: str) -> str:
    """الحصول على اسم المعدات بالعربية"""
    names = {
        "free_weights": "أوزان حرة",
        "machine": "آلة",
        "bodyweight": "وزن الجسم",
        "cable": "كابل"
    }
    return names.get(equipment, equipment)


def get_difficulty_name(difficulty: str) -> str:
    """الحصول على اسم الصعوبة بالعربية"""
    names = {
        "beginner": "مبتدئ",
        "intermediate": "متوسط",
        "advanced": "متقدم"
    }
    return names.get(difficulty, difficulty)

# FitCoach Bot - بوت المدرب الذكي لكمال الأجسام 🏋️

<div align="center">

![FitCoach Banner](https://img.shields.io/badge/FitCoach-مدربك_الشخصiني-gold?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5B4?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</div>

---

## 📖 نظرة عامة

**FitCoach** هو بوت تلجرام ذكي ومتطور يعمل كمدرب شخصي رقمي لاحترافي لكمال الأجسام وبناء الكتلة العضلية. يراقب تطورك الجسدي يوميًا ويقودك خطوة بخطوة نحو تحقيق أهدافك.

---

## ✨ الميزات الرئيسية

### 🎯 إدارة الملف الشخصي
- تتبع البيانات الأساسية (العمر، الطول، الوزن، نسبة الدهون)
- تحديد مستوى الخبرة والهدف
- حساب الاحتياج اليومي من السعرات والمغذيات

### 🍽️ نظام التغذية الذكي
- تتبع الوجبات اليومية
- حساب السعرات الحرارية والمغذيات
- اقتراح وجبات حسب الهدف والميزانية
- بدائل غذائية اقتصادية

### 🏋️ نظام التدريب المتكامل
- قاعدة بيانات تضم 35+ تمرين
- جداول مخصصة حسب الخبرة والهدف
- تسجيل الأوزان والتكرارات
- تمارين بديلة عند عدم توفر المعدات

### 📊 تحليل الأداء
- تقارير يومية وأسبوعية وشهرية
- تتبع تغير الوزن
- حساب سلسلة الالتزام
- إنجازات ومكافآت

### 🤖 ذكاء تكيفي
- يتعلم من بياناتك مع الوقت
- اقتراحات ذكية للتعديل
- تنبيهات وتحفيز مستمر

---

## 🛠️ التثبيت

### المتطلبات
- Python 3.10 أو أعلى
- حساب Telegram
- Token بوت من @BotFather

### الخطوات

1. **استنساخ المشروع:**
```bash
git clone https://github.com/your-repo/fitness-coach-bot.git
cd fitness-coach-bot
```

2. **إنشاء بيئة افتراضية:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. **تثبيت المتطلبات:**
```bash
pip install -r requirements.txt
```

4. **إنشاء ملف البيئة:**
```bash
cp config/.env.example config/.env
```

5. **إضافة Bot Token:**
   - افتح Telegram وابحث عن @BotFather
   - أرسل `/newbot` واتبع الخطوات
   - انسخ Token وأنشئه في ملف `.env`:
   ```
   BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

6. **تشغيل البوت:**
```bash
python bot/main.py
```

---

## 📁 هيكل المشروع

```
fitness_bot/
├── bot/
│   ├── __init__.py
│   ├── main.py              # نقطة الدخول
│   ├── config.py             # الإعدادات
│   ├── database.py          # عمليات قاعدة البيانات
│   ├── models.py            # نماذج البيانات
│   ├── handlers/            # معالجات الأوامر
│   │   ├── start.py
│   │   ├── profile.py
│   │   ├── nutrition.py
│   │   ├── workout.py
│   │   ├── tracking.py
│   │   └── reports.py
│   ├── keyboards/           # لوحات المفاتيح
│   │   └── main_menu.py
│   ├── services/            # الخدمات
│   │   └── nutrition_service.py
│   └── data/                # البيانات
│       └── exercises.py
├── data/                    # مجلد البيانات
│   └── fitness.db
├── logs/                    # مجلد السجلات
├── config/
│   └── .env.example
├── requirements.txt
├── README.md
├── SPEC.md
└── .gitignore
```

---

## 📱 أوامر البوت

| الأمر | الوصف |
|-------|-------|
| `/start` | بدء البوت |
| `/menu` | القائمة الرئيسية |
| `/profile` | عرض الملف الشخصي |
| `/today` | ملخص اليوم |
| `/help` | المساعدة |

---

## 🎯 الأهداف المدعومة

| الهدف | الوصف | البروتين |
|-------|-------|---------|
| 🔥 **ضخامة** | بناء الكتلة العضلية | 2 غ/كغ |
| ❄️ **تنشيف** | حرق الدهون | 2.5 غ/كغ |
| 🔄 **إعادة تركيب** | بناء عضلي مع حرق دهون | 2.2 غ/كغ |

---

## 📊 التقنيات المستخدمة

- **Python 3.10+**
- **python-telegram-bot v20** - مكتبة بوت تلجرام
- **SQLAlchemy** - ORM لقاعدة البيانات
- **SQLite** - قاعدة بيانات خفيفة
- **matplotlib** - للرسوم البيانية

---

## 🔬 المصادر العلمية

البوت يعتمد على مصادر علمية موثوقة:

- **ACSM** - American College of Sports Medicine
- **ISSN** - International Society of Sports Nutrition
- **PubMed** - لأبحاث التغذية والتدريب
- مبدأ التحميل التدريجي (Progressive Overload)
- مبدأ التخصيص (Specificity Principle)

---

## 🐳 التشغيل بواسطة Docker (اختياري)

```bash
# بناء الصورة
docker build -t fitness-coach-bot .

# تشغيل
docker run -d \
  --name fitness-coach \
  -e BOT_TOKEN=your_token \
  fitness-coach-bot
```

---

## 📝 الترخيص

هذا المشروع مرخص تحت [MIT License](LICENSE).

---

## 🤝 المساهمة

نرحب بمساهماتكم! يرجى:
1. Fork المشروع
2. إنشاء فرع جديد (`git checkout -b feature/AmazingFeature`)
3. Commit التغييرات (`git commit -m 'Add AmazingFeature'`)
4. Push للفرع (`git push origin feature/AmazingFeature`)
5. فتح Pull Request

---

## 📧 التواصل

للمساعدة أو الاستفسارات:
- افتح Issue على GitHub
- تواصل مع المطور

---

<div align="center">

🏋️ **FitCoach - مدربك الشخصي الذكي** 🏋️

</div>

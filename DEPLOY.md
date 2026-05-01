# FitCoach Bot - Render Deployment Guide

## 🚀 النشر على Render.com (تلقائي)

### الخطوة 1: ربط GitHub مع Render
1. اذهب إلى [dashboard.render.com](https://dashboard.render.com)
2. سجّل الدخول بحساب GitHub
3. اضغط **New** → **Blueprint**

### الخطوة 2: ربط المستودع
1. اختر **`fitness-bot`** من قائمة المستودعات
2. اضغط **Connect**

### الخطوة 3: إضافة المفاتيح السرية
أضف المتغيرات البيئية التالية في Render:

| المتغير | القيمة |
|---------|--------|
| `BOT_TOKEN` | 🔒 أدخل Token البوت من @BotFather |
| `AZURE_OPENAI_KEY` | 🔒 أدخل مفتاح Azure |
| `AZURE_OPENAI_ENDPOINT` | 🔒 أدخل رابط Azure |
| `AZURE_OPENAI_DEPLOYMENT` | `gpt-4o-mini` |
| `AZURE_OPENAI_API_VERSION` | `2024-02-15` |
| `GITHUB_TOKEN` | 🔒 أدخل GitHub Token |

### الخطوة 4: النشر
1. اختر الخطة **Free**
2. اختر المنطقة **Oregon**
3. اضغط **Create Blueprint**

### ✅ ما سيحدث تلقائياً:
- Render سيقرأ `render.yaml`
- سيثبت المتطلبات
- سيشغّل البوت مباشرة

---

## 🎯 للتأكد من عمل البوت:
1. افتح Telegram
2. ابحث عن **@MutazF_Bot**
3. أرسل `/start`

---

## 🔧 إذا احتجت إعادة التشغيل:
اذهب إلى Render Dashboard → fitness-bot → **Manual Deploy** → **Deploy latest**

---

## 📊 الملفات المطلوبة:
- `render.yaml` - إعدادات النشر
- `Dockerfile` - لبناء الحاوية
- `requirements.txt` - المتطلبات

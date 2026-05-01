#!/bin/bash
# FitCoach Bot - سكريبت التشغيل السريع

echo "========================================="
echo "   FitCoach Bot - بوت المدرب الذكي 💪"
echo "========================================="

# التحقق من Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 غير مثبت!"
    echo "تثبيت Python3..."
    apt update && apt install python3 python3-pip -y
fi

# التحقق من المتطلبات
echo ""
echo "📦 التحقق من المتطلبات..."

cd "$(dirname "$0")"

if [ ! -f "requirements.txt" ]; then
    echo "❌ ملف requirements.txt غير موجود!"
    exit 1
fi

# تثبيت المتطلبات
pip3 install -r requirements.txt --quiet

# إنشاء المجلدات
mkdir -p data logs config

# التحقق من ملف الإعدادات
if [ ! -f "config/.env" ]; then
    echo "⚠️ ملف .env غير موجود!"
    echo "سيتم نسخ الملف من .env.example..."
    cp config/.env.example config/.env
    echo ""
    echo "⚠️ يرجى إضافة المفاتيح في config/.env"
    echo "==================================="
    cat config/.env
    echo "==================================="
    exit 1
fi

# التحقق من Bot Token
source config/.env
if [ -z "$BOT_TOKEN" ] || [ "$BOT_TOKEN" == "your_bot_token_here" ]; then
    echo "❌ BOT_TOKEN غير مضاف في config/.env"
    echo "يرجى إضافة Token من @BotFather"
    exit 1
fi

echo ""
echo "✅ جميع الإعدادات جاهزة!"
echo ""
echo "🚀 بدء تشغيل البوت..."
echo ""

# تشغيل البوت
python3 bot/main.py

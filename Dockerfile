# FitCoach Bot - Dockerfile
FROM python:3.10-slim

# إعداد العمل
WORKDIR /app

# نسخ المتطلبات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود
COPY bot/ ./bot/
COPY config/ ./config/
COPY data/ ./data/
RUN mkdir -p logs

# إنشاء ملف البيئة إذا لم يكن موجوداً
RUN if [ ! -f config/.env ]; then cp config/.env.example config/.env; fi

# كشف المنفذ
EXPOSE 8000

# الأمر الافتراضي
CMD ["python", "bot/main.py"]

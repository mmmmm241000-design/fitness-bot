"""
خدمة الذكاء الاصطناعي - FitCoach Bot
تكامل مع Azure OpenAI للردود الذكية
"""
import os
import logging
from typing import Optional, Dict, List
from dataclasses import dataclass

try:
    from openai import AzureOpenAI
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False
    logging.warning("Azure OpenAI SDK not installed. AI features will be limited.")

from bot.config import config

logger = logging.getLogger(__name__)


@dataclass
class AIResponse:
    """استجابة الذكاء الاصطناعي"""
    text: str
    success: bool
    error: Optional[str] = None


class AICoach:
    """
    مدرب ذكي يعمل بالذكاء الاصطناعي
    يستخدم Azure OpenAI لفهم سياق المستخدم وتقديم ردود مخصصة
    """

    SYSTEM_PROMPT = """أنت FitCoach، مدرب شخصي رقمي محترف في كمال الأجسام والتغذية.
لديك خبرة واسعة في:
- بناء الكتلة العضلية
- التغذية الرياضية
- التخطيط التدريبي
- تحليل الأداء

مهمتك:
1. تقديم نصائح مبنية على العلم
2. تحفيز المستخدمين
3. الإجابة على أسئلتهم
4. تقديم اقتراحات مخصصة

القواعد:
- كن داعمًا وحازمًا
- اعتمد على المصادر العلمية
- لا تقدم تشخيصات طبية
- شجع الالتزام والانضباط
- تحدث بأسلوب عربي واضح"""

    def __init__(self):
        self.client = None
        self.enabled = False

        if AZURE_AVAILABLE and os.getenv("AZURE_OPENAI_KEY"):
            try:
                self.client = AzureOpenAI(
                    api_key=os.getenv("AZURE_OPENAI_KEY"),
                    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15"),
                    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
                )
                self.deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
                self.enabled = True
                logger.info("✅ Azure OpenAI configured successfully")
            except Exception as e:
                logger.error(f"❌ Failed to configure Azure OpenAI: {e}")

    def is_available(self) -> bool:
        """التحقق من توفر خدمة الذكاء الاصطناعي"""
        return self.enabled

    async def chat(self, user_message: str, context: Optional[Dict] = None) -> AIResponse:
        """
        المحادثة مع المستخدم
        """
        if not self.enabled:
            return AIResponse(
                text="🤖 ميزة الذكاء الاصطناعي غير متاحة حالياً.\n"
                     "يمكنك استخدام الأوامر اليدوية للبوت.",
                success=False,
                error="AI not configured"
            )

        try:
            # بناء السياق
            messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]

            # إضافة سياق المستخدم إن وُجد
            if context:
                context_text = self._build_context(context)
                if context_text:
                    messages.append({
                        "role": "system",
                        "content": f"معلومات المستخدم:\n{context_text}"
                    })

            # إضافة رسالة المستخدم
            messages.append({"role": "user", "content": user_message})

            # إرسال الطلب
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )

            return AIResponse(
                text=response.choices[0].message.content,
                success=True
            )

        except Exception as e:
            logger.error(f"AI Chat Error: {e}")
            return AIResponse(
                text="❌ حدث خطأ في معالجة طلبك.\n"
                     "💡 حاول مرة أخرى لاحقاً.",
                success=False,
                error=str(e)
            )

    def _build_context(self, context: Dict) -> str:
        """بناء نص السياق من بيانات المستخدم"""
        parts = []

        if context.get("name"):
            parts.append(f"الاسم: {context['name']}")

        if context.get("weight"):
            parts.append(f"الوزن الحالي: {context['weight']} كجم")

        if context.get("goal"):
            goal_names = {
                "bulking": "ضخامة عضلية",
                "cutting": "تنشيف",
                "recomp": "إعادة تركيب"
            }
            parts.append(f"الهدف: {goal_names.get(context['goal'], context['goal'])}")

        if context.get("experience"):
            exp_names = {
                "beginner": "مبتدئ",
                "intermediate": "متوسط",
                "advanced": "متقدم"
            }
            parts.append(f"مستوى الخبرة: {exp_names.get(context['experience'], context['experience'])}")

        if context.get("workout_days"):
            parts.append(f"أيام التمرين: {context['workout_days']} أيام/أسبوع")

        if context.get("today_summary"):
            parts.append(f"ملخص اليوم: {context['today_summary']}")

        return "\n".join(parts)

    async def analyze_food(self, food_description: str) -> AIResponse:
        """تحليل الطعام وتقديم اقتراحات"""
        if not self.enabled:
            return AIResponse(
                text="⚠️ هذه الميزة تتطلب تفعيل الذكاء الاصطناعي.",
                success=False
            )

        prompt = f"""تحليل غذائي:

الطعام: {food_description}

قدم تحليلاً شاملاً يتضمن:
1. القيم الغذائية التقريبية (سعرات، بروتين، كارب، دهون)
2. هل يناسب هدف [بناء عضلات/تنشيف]؟
3. بدائل صحية أفضل إن وجدت
4. اقتراحات للكمية المثالية"""

        return await self.chat(prompt)

    async def generate_meal_plan(self, preferences: Dict) -> AIResponse:
        """إنشاء خطة وجبات مخصصة"""
        if not self.enabled:
            return AIResponse(
                text="⚠️ هذه الميزة تتطلب تفعيل الذكاء الاصطناعي.",
                success=False
            )

        prompt = f"""إنشاء خطة وجبات مخصصة:

التفضيلات:
- الميزانية: {preferences.get('budget', 'متوسطة')}
- تفضيلات الطعام: {preferences.get('food_preferences', 'غير محدد')}
- عدد الوجبات: {preferences.get('meals_count', 4)}
- الحساسية الغذائية: {preferences.get('allergies', 'لا توجد')}

قدم خطة وجبات يومية كاملة مع:
1. أسماء الوجبات
2. القيم الغذائية
3. طرق التحضير البسيطة
4. بدائل اقتصادية"""

        return await self.chat(prompt)

    async def analyze_progress(self, progress_data: Dict) -> AIResponse:
        """تحليل تقدم المستخدم"""
        if not self.enabled:
            return AIResponse(
                text="⚠️ هذه الميزة تتطلب تفعيل الذكاء الاصطناعي.",
                success=False
            )

        prompt = f"""تحليل تقدم المستخدم:

البيانات:
{self._build_context(progress_data)}

قدم تحليلاً شاملاً يتضمن:
1. تقييم الأداء العام
2. نقاط القوة
3. نقاط تحتاج تحسين
4. توصيات محددة للتغيير
5. تشجيع وتحفيز"""

        return await self.chat(prompt)

    async def answer_fitness_question(self, question: str) -> AIResponse:
        """الإجابة على سؤال في كمال الأجسام"""
        if not self.enabled:
            return AIResponse(
                text="⚠️ هذه الميزة تتطلب تفعيل الذكاء الاصطناعي.",
                success=False
            )

        prompt = f"""سؤال في كمال الأجسام/التغذية:

{question}

أجب بشكل:
1. علمي ودقيق
2. عملي وقابل للتطبيق
3. مع أمثلة عند الحاجة
4. مع ذكر المصادر إن أمكن"""

        return await self.chat(prompt)


# إنشاء كائن وحيد للخدمة
ai_coach = AICoach()


def get_ai_coach() -> AICoach:
    """الحصول على مثيل خدمة الذكاء الاصطناعي"""
    return ai_coach

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from google import genai

TELEGRAM_TOKEN = "8888302838:AAFuZ0AOQj-fqHZBzA0BAz-mRkoW0imtPNs"
GEMINI_API_KEY = "AQ.Ab8RN6JB_VSpepVYxImSvUKGYEyonB-fjkCorKfx"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()
ai_client = genai.Client(api_key=GEMINI_API_KEY)

user_chats = {}

SYSTEM_INSTRUCTION = (
    "Ты вежливый, умный и полезный ассистент. "
    "Отвечай четко, емко и по существу на русском языке."
)

@dp.message(CommandStart())
async def handle_start(message: types.Message):
    user_chats[message.from_user.id] = ai_client.chats.create(
        model="gemini-2.5-flash",
        config=genai.types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION
        )
    )
    await message.answer("Здравствуйте! Я готов к работе. Задайте любой вопрос.")

@dp.message(Command("clear"))
async def handle_clear(message: types.Message):
    user_chats.pop(message.from_user.id, None)
    await message.answer("История диалога очищена! Можем начать заново.")

@dp.message()
async def handle_text(message: types.Message):
    if not message.text:
        return

    user_id = message.from_user.id

    if user_id not in user_chats:
        user_chats[user_id] = ai_client.chats.create(
            model="gemini-2.5-flash",
            config=genai.types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION
            )
        )

    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    try:
        response = user_chats[user_id].send_message(message.text)
        await message.answer(response.text)
    except Exception as e:
        print(f"Ошибка API: {e}")
        await message.answer("Произошла ошибка при обработке запроса.")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "help"])
async def cmd_start(message: types.Message):
    await message.reply(
        "пожалуйста, напишите ваш вопрос."
    )


@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_text(message: types.Message):
    # Forward the message text only — no user info
    anonymized = (
        "📨 <b>New Anonymous Message</b>\n\n"
        f"{message.text}"
    )

    await bot.send_message(
        ADMIN_CHAT_ID,
        anonymized,
        parse_mode="HTML"
    )

    await message.reply('''вопрос получен, в порядке очереди я отвечу на него в рамках рубрики в телеграм-канале @obozreniepsy

если вы хотите написать еще один вопрос — отправьте его здесь же.''')


# Ignore all other content types
@dp.message_handler()
async def unsupported(message: types.Message):
    await message.reply("Only text messages are supported for anonymity.")


if __name__ == "__main__":
    executor.start_polling(dp)

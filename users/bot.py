import django
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, BotCommand, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, \
    ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import asyncio
import random
import os
import sys
from asgiref.sync import sync_to_async
from uuid import uuid4
import environ
from pathlib import Path

env = environ.Env()
environ.Env.read_env()
BASE_DIR = Path(__file__).resolve().parent.parent


environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Django Setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Adjust path for Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import TelegramOTP

# Telegram Bot Token
TOKEN = env('BOT_TOKEN')

dp = Dispatcher()
router = Router()


async def start_command_response(message: Message, bot: Bot):
    bot_info = await bot.me()
    bot_username = bot_info.username

    text = (f"Hi {message.from_user.first_name} 👋\n"
            f"Welcome to the official bot of the real-time chat app @{bot_username}\n\n"
            f"You can get your login code here: /login")

    await message.answer(text)


@sync_to_async
def create_user_otp(telegram_user_id, first_name, username=None, last_name=None):
    user, _ = User.objects.get_or_create(
        username=str(username if username else telegram_user_id),
        defaults={
            'password': str(uuid4()),
            'first_name': first_name,
            'last_name': last_name if last_name else ""
        }
    )


    if hasattr(user, 'telegramotp') and user.telegramotp:
        message1 = f"🔒 You have active login code. <code>{user.telegramotp.otp}</code>"
        return user, message1

    code = "".join([str(random.randint(0, 9)) for _ in range(6)])
    message2 = f"🔒 Your one-time login code is <code>{code}</code>"
    otp_obj = TelegramOTP.objects.create(
        telegram_user_id=telegram_user_id,
        user=user,
        otp=code
    )

    return user, message2


async def login_command_response(message: Message, bot: Bot):

    user, text = await create_user_otp(message.from_user.id, message.from_user.first_name, message.from_user.username, message.from_user.last_name)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Renew code", callback_data='renew_code')]
    ])

    await message.answer(text, parse_mode='HTML', reply_markup=keyboard)


@router.callback_query(lambda c: c.data == 'renew_code')
async def renew_code(callback: CallbackQuery, bot: Bot):
    user, text = await create_user_otp(callback.message.from_user.id, callback.message.from_user.first_name)

    await callback.message.edit_text(text, parse_mode='HTML', reply_markup=callback.message.reply_markup)


async def start():
    bot = Bot(token=TOKEN)

    dp.include_router(router)
    dp.message.register(start_command_response, Command('start'))
    dp.message.register(login_command_response, Command('login'))

    await bot.set_my_commands([
        BotCommand(command='/login', description='Get a 6-digit login code'),
        BotCommand(command='/start', description='Start the bot')
    ])

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start())

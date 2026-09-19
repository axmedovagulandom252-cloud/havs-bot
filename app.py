import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart

# =========================
# SOZLAMALAR
# =========================

BOT_TOKEN = "8852503216:AAFm-XPhElVgHDtSwtCJ-L0MkDVL3LW8xj0"

# Telegramdan olgan video file_id larini shu yerga qo'yasiz
BRON_VIDEO = "BAACAgIAAxkBAAMrapbF85hm7ufID98YFytgX55KBS4AArmkAAIHarBIERK6oCJ2bvw9BA"
LOCATION_VIDEO = "BAACAgIAAxkBAAMsapbF883AOKSnhMZD8Dq7QZrDj04AArukAAIHarBIBkl5wzX9XIc9BA"
CHECK_VIDEO = ""


# =========================
# BOT
# =========================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# =========================
# ASOSIY MENYU
# =========================
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Havas Bot ishlayapti!")

    def log_message(self, format, *args):
        pass


def run_web():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"Web server {port} portda ishga tushdi")
    server.serve_forever()
def main_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📅 Bron qilish",
                    callback_data="bron"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📍 Lokatsiyani ko‘rish",
                    callback_data="location"
                )
            ]
        ]
    )


# =========================
# QAYTISH TUGMASI
# =========================

def back_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Qaytish",
                    callback_data="back"
                )
            ]
        ]
    )


# =========================
# START
# =========================

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "Assalomu alaykum! 👋\n\n"
        "Sizga qanday yordam kerak?",
        reply_markup=main_menu()
    )


# =========================
# BRON QILISH
# =========================

@dp.callback_query(F.data == "bron")
async def bron(callback: CallbackQuery):

    await callback.message.delete()

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=BRON_VIDEO,
        caption="📅 Bron qilish bo‘yicha video",
        reply_markup=back_button()
    )

    await callback.answer()


# =========================
# LOKATSIYA
# =========================

@dp.callback_query(F.data == "location")
async def location(callback: CallbackQuery):

    await callback.message.delete()

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=LOCATION_VIDEO,
        caption="📍 Lokatsiyani ko‘rish bo‘yicha video",
        reply_markup=back_button()
    )

    await callback.answer()


# =========================
# CHEK
# =========================

@dp.callback_query(F.data == "check")
async def check(callback: CallbackQuery):

    await callback.message.delete()

    await bot.send_video(
        chat_id=callback.from_user.id,
        video=CHECK_VIDEO,
        caption="🧾 Chek rasmini qayerga tashlash bo‘yicha video",
        reply_markup=back_button()
    )

    await callback.answer()


# =========================
# QAYTISH
# =========================

@dp.callback_query(F.data == "back")
async def back(callback: CallbackQuery):

    await callback.message.delete()

    await bot.send_message(
        chat_id=callback.from_user.id,
        text="Assalomu alaykum! 👋\n\n"
             "Sizga qanday yordam kerak?",
        reply_markup=main_menu()
    )

    await callback.answer()


# =========================
# ISHGA TUSHIRISH
# =========================

async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

    if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    asyncio.run(main())
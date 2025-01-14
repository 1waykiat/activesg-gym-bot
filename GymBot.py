import asyncio
import os
from dotenv import load_dotenv

from GymDataManager import GymDataManager
from QueryHandler import QueryHandler

from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()

bot = AsyncTeleBot(os.environ.get('TELEBOT_TOKEN'))
gdm = GymDataManager()
qh = QueryHandler(gdm)

gyms = gdm.get_all_gyms()

# Command Handlers
@bot.message_handler(commands=['start'])
async def send_welcome(message):
    chat_dest = message.chat.id
    
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="🔍 Current Gym Capacities", callback_data="start:current"))
    keyboard.add(InlineKeyboardButton(text="📊 Average Gym Crowd Trends", callback_data="start:average"))
    
    await bot.send_message(chat_dest, qh.start(), reply_markup=keyboard)

@bot.message_handler(commands=['help'])
async def send_help(message):
    chat_dest = message.chat.id
    await bot.send_message(chat_dest, qh.help())
    
@bot.message_handler(commands=['info'])
async def send_info(message):
    chat_dest = message.chat.id
    await bot.send_message(
        chat_id=chat_dest,
        text=qh.info(),
        parse_mode="HTML"
    )
    
@bot.message_handler(commands=['current'])
async def handle_current(message):
    chat_dest = message.chat.id
    await bot.send_message(
        chat_id=chat_dest,
        text=qh.current_cap(),
        parse_mode="HTML"
    )

@bot.message_handler(commands=['average'])
async def handle_average(message):
    chat_dest = message.chat.id
    
    keyboard = InlineKeyboardMarkup()
    
    for gym in gyms:
        keyboard.add(InlineKeyboardButton(text=gym, callback_data=f"average:{gym}"))
    
    await bot.send_message(chat_dest, "Select a gym to view its average capacity trends: ", reply_markup=keyboard)
    
# Callback Query Handlers
@bot.callback_query_handler(func=lambda call: call.data.startswith("start:"))
async def handle_start_callback(call):
    command = call.data.split(":", 1)[1]
    if command == 'current':
        await handle_current(call.message)
    elif command == 'average':
        await handle_average(call.message)

@bot.callback_query_handler(func=lambda call: call.data.startswith("average:"))
async def handle_avg_callback(call):
    chat_dest = call.message.chat.id
    gym_name = call.data.split(":", 1)[1]
    response = qh.avg_cap_for_gym(gym_name)
    
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=response,
        parse_mode="HTML"
    )
    await bot.answer_callback_query(call.id)
    
    
# Main function
async def main():    
    asyncio.create_task(gdm.refresh_session_periodically())
    await bot.polling(interval=1)

asyncio.run(main())

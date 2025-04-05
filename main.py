
from aiogram import Bot, Dispatcher, types, executor
import random, sqlite3
from datetime import datetime

TOKEN = "7598583818:AAEz3Hogf3NtfqZKwPD8mGqnBt9UOb47wu4"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

conn = sqlite3.connect('rpgbot.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, xp INTEGER, level INTEGER, gold INTEGER)")
conn.commit()

def get_user(user_id, username):
    c.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = c.fetchone()
    if not user:
        c.execute("INSERT INTO users (id, username, xp, level, gold) VALUES (?, ?, 0, 1, 100)", (user_id, username))
        conn.commit()
        return (user_id, username, 0, 1, 100)
    return user

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = get_user(message.from_user.id, message.from_user.username)
    await message.reply(f"""Welcome {user[1]}! Your journey begins now!
Level: {user[3]} | XP: {user[2]} | Gold: {user[4]}""")

@dp.message_handler(commands=['daily'])
async def daily(message: types.Message):
    user = get_user(message.from_user.id, message.from_user.username)
    gold = random.randint(20, 100)
    c.execute("UPDATE users SET gold = gold + ? WHERE id = ?", (gold, user[0]))
    conn.commit()
    await message.reply(f"You claimed your daily reward: {gold} gold!")

@dp.message_handler(commands=['duel'])
async def duel(message: types.Message):
    user = get_user(message.from_user.id, message.from_user.username)
    xp_gain = random.randint(10, 30)
    c.execute("UPDATE users SET xp = xp + ? WHERE id = ?", (xp_gain, user[0]))
    conn.commit()
    await message.reply(f"You fought bravely and earned {xp_gain} XP!")

@dp.message_handler(commands=['profile'])
async def profile(message: types.Message):
    user = get_user(message.from_user.id, message.from_user.username)
    await message.reply(f"Profile:
Level: {user[3]}
XP: {user[2]}
Gold: {user[4]}
Avatar: https://avatars.dicebear.com/api/adventurer/{user[1]}.svg")

@dp.message_handler(commands=['leaderboard'])
async def leaderboard(message: types.Message):
    c.execute("SELECT username, level, xp FROM users ORDER BY level DESC, xp DESC LIMIT 5")
    top = c.fetchall()
    text = "**Top Adventurers:**\n"
    for i, row in enumerate(top):
        text += f"{i+1}. {row[0]} - Lvl {row[1]} ({row[2]} XP)\n"
    await message.reply(text)

if __name__ == '__main__':
    executor.start_polling(dp)

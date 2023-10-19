import telebot
import datetime
from datetime import timedelta

TOKEN = "PASTE UR BOT TOKEN HERE"
bot = telebot.TeleBot(TOKEN)

ratings = {
    "UR USERS HERE": 0,
}

def get_current_date():
    return (datetime.datetime.now() + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")

def create_keyboard(names):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = []
    for name in names:
        buttons.append(telebot.types.KeyboardButton(name))
    keyboard.add(*buttons)
    keyboard.row(telebot.types.KeyboardButton("Overall rating"))
    return keyboard

#StartKomanda

@bot.message_handler(commands=['start'])
def start(message):
    names = list(ratings.keys())
    keyboard = create_keyboard(names)
    bot.send_message(message.chat.id, "Select a participant:", reply_markup=keyboard)

chosen_name = None

#Knopachki

@bot.message_handler(func=lambda message: message.text in ratings.keys())
def handle_name_choice(message):
    global chosen_name
    chosen_name = message.text
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(telebot.types.KeyboardButton("+"), telebot.types.KeyboardButton("-"))
    markup.row(telebot.types.KeyboardButton("Personal rating"), telebot.types.KeyboardButton("back"))
    bot.send_message(message.chat.id, f"choosed {chosen_name}. choose action:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "+")
def increment_rating(message):
    ratings[chosen_name] += 1
    current_date = get_current_date()
    bot.send_message(message.chat.id, f"\n\nadded point for : {chosen_name}. Current rating: {ratings[chosen_name]}.\n\Date: {current_date}")

@bot.message_handler(func=lambda message: message.text == "-")
def decrement_rating(message):
    ratings[chosen_name] -= 1
    current_date = get_current_date()
    bot.send_message(message.chat.id, f"\n\nPoint taken of:  {chosen_name}. Current Rating: {ratings[chosen_name]}.\n\nDate: {current_date}")

@bot.message_handler(func=lambda message: message.text == "Personal Rating")
def show_user_rating(message):
    bot.send_message(message.chat.id, f"Current Rating {chosen_name}: {ratings[chosen_name]}.")

@bot.message_handler(func=lambda message: message.text == "Overall Rating")
def show_total_rating(message):
    sorted_ratings = sorted(ratings.items(), key=lambda x: x[1], reverse=True)
    current_date = get_current_date()
    rating_text = "\n".join([f"{name}: {rating}" for name, rating in sorted_ratings])
    rating_text = f"Overral Rating:\n\n{rating_text}\n\nDate:\n{current_date}"
    bot.send_message(message.chat.id, rating_text)

@bot.message_handler(func=lambda message: message.text == "Back")
def go_back(message):
    global chosen_name
    chosen_name = None
    start(message)

bot.polling()




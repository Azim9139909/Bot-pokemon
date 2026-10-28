import telebot 
from config import token
from random import randint

from logic import Pokemon, Wizard, Fighter

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['go'])
def start(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        chance = randint(1,3)
        if chance == 1:
            pokemon = Pokemon(message.from_user.username)
        elif chance == 2:
            pokemon = Wizard(message.from_user.username)
        elif chance == 3:
            pokemon = Fighter(message.from_user.username)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['attack'])
def attack_pok(message):
    if message.reply_to_message:
        if message.reply_to_message.from_user.username in Pokemon.pokemons.keys() and message.from_user.username in Pokemon.pokemons.keys():
            enemy = Pokemon.pokemons[message.reply_to_message.from_user.username]
            pokemon = Pokemon.pokemons[message.from_user.username]
            result = pokemon.attack(enemy)
            bot.send_message(message.chat.id, result)
            result = pokemon.info()
            bot.send_message(message.chat.id, result)
        else:
            bot.send_message(message.chat.id, "Сражаться можно только с покемонами (/go)")
    else:
            bot.send_message(message.chat.id, "Чтобы атаковать, нужно ответить на сообщения того, кого хочешь атаковать")

@bot.message_handler(commands=['feed'])
def feed_pok(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pok = Pokemon.pokemons[message.from_user.username]
        response = pok.feed()
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "У вас нет покемона!")

bot.infinity_polling(none_stop=True)


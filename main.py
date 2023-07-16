import time
import telebot
from telebot import types
import threading
from datetime import datetime
import database
import parsing
import config

bot = telebot.TeleBot(config.TOKEN)

try:

    while True:
        def notes():
            data = database.get_all_info()
            if data is not None:
                for i in data:
                    buf = i[3].split(' ')
                    if buf[0] == str(datetime.now().hour) + ":" + str(datetime.now().minute) or buf[1] == \
                            str(datetime.now().hour) + ":" + str(datetime.now().minute):
                        bot.send_message(i[0], text=parsing.parsing())
            time.sleep(60)


        threading.Thread(target=notes).start()


        @bot.message_handler(commands=['start'])
        def timetable(message):
            markup = types.ReplyKeyboardMarkup()
            button_reg = types.KeyboardButton("/registration")
            markup.add(button_reg)
            bot.send_message(message.chat.id, text="Нужно зарегистрироваться", reply_markup=markup)


        @bot.message_handler(commands=['registration'])
        def registration_start(message):
            bot.send_message(message.chat.id, text="Введите email и пароль от AlphaCRM [email_password]")


        @bot.message_handler(content_types=['text'])
        def registration_validation(message):
            if '@' in message.text and '_' in message.text:
                buffer_data = message.text.split("_")
                if parsing.test_request(buffer_data[0], buffer_data[1]):
                    if database.add_user(str(message.chat.id), buffer_data[0], buffer_data[1]):
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        button_reminder = types.KeyboardButton("Напоминания")
                        button_timetable = types.KeyboardButton("Расписание")
                        markup.add(button_reminder, button_timetable)
                        bot.send_message(message.chat.id, text="Вы успешно зарегистрированны", reply_markup=markup)
                    else:
                        bot.send_message(message.chat.id, text="Ошибка на стороне сервера, попробуйте позже")
                else:
                    bot.send_message(message.chat.id, text="Неверный e-mail или пароль")

            if message.text == "Расписание":
                udata = database.get_info(message.chat.id)
                if udata is not None:
                    days = parsing.parsing(udata[0][1], udata[0][2])
                    bot.send_message(message.chat.id, text=days)

            if message.text == "Напоминания":
                bot.send_message(message.chat.id, "Введите два значения. Первое напоминание на завтра, второе - на сегодня [чч:мм чч:мм]")

            if ':' in message.text:
                if database.add_data(message.chat.id, message.text):
                    bot.send_message(message.chat.id, "Напоминания установлены")


        bot.polling(none_stop=True, interval=0)


except Exception as ex:
    print(ex)

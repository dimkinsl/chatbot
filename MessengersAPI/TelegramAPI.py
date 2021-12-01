"""Модуль чат-бота через Телеграм"""
import logging

import telebot
import config

from Models import lump, machine

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(config.TOKEN_TELEGRAM)


@bot.message_handler(commands=['start'])
def start_message(message):
    # Обрабатываем кнопку старт. Если состояние 'finish', меняем его на 'start'
    if lump.state == 'finish':
        machine.set_state('start')

    bot.send_message(message.chat.id, 'Какую вы хотите пиццу? Большую или маленькую?')


@bot.message_handler(func=lambda message: True)
def choice_message(message):
    # Логика обработки диалога при помощи стейт-машины
    # Выбираем размер
    if message.text.lower() == 'большую' or message.text.lower() == 'маленькую':
        lump.trigger('choice_pizza')
        lump.size = message.text
        bot.send_message(message.chat.id, 'Как вы будете платить?')

    # Способ оплаты
    elif lump.state == 'pay':
        lump.trigger('choice_pay')
        lump.pay_options = message.text
        bot.send_message(message.chat.id, f'Вы хотите {lump.get_environments()[0]} пиццу, '
                                          f'оплата - {lump.get_environments()[1]}?')

    elif message.text.lower() == 'да':
        lump.trigger('final_question')
        bot.send_message(message.chat.id, 'Спасибо за заказ')
        bot.send_message(message.chat.id, 'Отправьте /start для нового заказа')

    elif message.text.lower() == 'нет':
        machine.set_state('start')
        bot.send_message(message.chat.id, 'Начните заново. Какую вы хотите пиццу? Большую или маленькую?')

    # Если мы не получили размер пиццы, переспрашиваем
    elif lump.state == 'start':
        bot.send_message(message.chat.id, 'Я не понял, повторите пожалуйста!')


# Главная функция запуска
def start_programm():
    bot.infinity_polling()


if __name__ == '__main__':
    start_programm()

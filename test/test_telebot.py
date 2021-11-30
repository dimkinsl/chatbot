# -*- coding: utf-8 -*-
import sys

sys.path.append('../')

import time
import pytest
import os

import telebot
from telebot import types
from telebot import util

from Models import lump, machine

should_skip = 'TOKEN' and 'CHAT_ID' not in os.environ

if not should_skip:
    TOKEN = os.environ['TOKEN']
    CHAT_ID = os.environ['CHAT_ID']


@pytest.mark.skipif(should_skip, reason="No environment variables configured")
class TestTeleBot:
    def test_message_listener(self):
        msg_list = []
        for x in range(100):
            msg_list.append(self.create_text_message('Message ' + str(x)))

        def listener(messages):
            assert len(messages) == 100

        tb = telebot.TeleBot('')
        tb.set_update_listener(listener)

    def test_message_handler(self):
        tb = telebot.TeleBot('')
        msg = self.create_text_message('/start')

        @tb.message_handler(commands=['start'])
        def command_handler(message):
            message.text = 'got'

        tb.process_new_messages([msg])
        time.sleep(1)
        assert msg.text == 'got'

    def test_state_machine_lump_size(self):
        lump.size = 'Большую'
        assert lump.get_environments()[0] == 'Большую'

    def test_state_machine_lump_pay_options(self):
        lump.pay_options = 'Наличкой'
        assert lump.get_environments()[1] == 'Наличкой'

    def test_send_message(self):
        text = 'Какую вы хотите пиццу? Большую или маленькую?'
        tb = telebot.TeleBot(TOKEN)
        ret_msg = tb.send_message(CHAT_ID, text)
        assert ret_msg.message_id

    def test_state_machine_big_or_small_question(self):
        text = f'Как вы будете платить?'
        lump.trigger('choice_pizza')
        tb = telebot.TeleBot(TOKEN)
        ret_msg = tb.send_message(CHAT_ID, text)
        assert ret_msg.message_id
        assert lump.state == 'pay'

    def test_state_machine_final_question(self):
        size = lump.get_environments()[0]
        pay = lump.get_environments()[1]
        text = f'Вы хотите {size} пиццу, оплата - {pay}?'
        lump.trigger('choice_pay')
        tb = telebot.TeleBot(TOKEN)
        ret_msg = tb.send_message(CHAT_ID, text)
        assert ret_msg.message_id
        assert lump.state == 'yes_no'

    def test_state_machine_final_answer_yes(self):
        lump.trigger('final_question')
        text = f'Спасибо за заказ!'
        tb = telebot.TeleBot(TOKEN)
        ret_msg = tb.send_message(CHAT_ID, text)
        assert ret_msg.message_id
        assert lump.state == 'finish'

    def test_state_machine_final_answer_no(self):
        machine.set_state('start')
        text = f'Начните заново. Какую вы хотите пиццу? Большую или маленькую?!'
        tb = telebot.TeleBot(TOKEN)
        ret_msg = tb.send_message(CHAT_ID, text)
        assert ret_msg.message_id
        assert lump.state == 'start'

    def test_Chat(self):
        tb = telebot.TeleBot(TOKEN)
        me = tb.get_me()
        msg = tb.send_message(CHAT_ID, 'Test')
        assert me.id == msg.from_user.id
        assert msg.chat.id == int(CHAT_ID)

    def test_antiflood(self):
        text = "Flooding"
        tb = telebot.TeleBot(TOKEN)
        for _ in range(0, 100):
            util.antiflood(tb.send_message, CHAT_ID, text)
        assert _

    @staticmethod
    def create_text_message(text):
        params = {'text': text}
        chat = types.User(11, False, 'test')
        return types.Message(1, None, None, chat, 'text', params, "")

    def test_is_string_unicode(self):
        s1 = u'string'
        assert util.is_string(s1)

    def test_is_string_string(self):
        s1 = 'string'
        assert util.is_string(s1)

    def test_not_string(self):
        i1 = 10
        assert not util.is_string(i1)

# Старт прграммы в зависимости от подключаемого модуля средства коммуникации

import os
import MessengersAPI.TelegramAPI as TelegramAPI
import MessengersAPI.FBAPI as FBAPI
import MessengersAPI.VKAPI as VKAPI
import MessengersAPI.SkypeAPI as SkypeAPI

# Запускаем прложение через средство коммуникации из os.environ['Method_API']
if __name__ == '__main__':
    API = os.environ['Method_API']
    if API == 'Telegram':
        TelegramAPI.start_programm()
    elif API == 'FACEBOOK':
        FBAPI.start_programm()
    elif API == 'VK':
        VKAPI.start_programm()
    elif API == 'SKYPE':
        SkypeAPI.start_programm()

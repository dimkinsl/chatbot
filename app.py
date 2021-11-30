# Старт прграммы в зависимости от подключаемого модуля средства коммуникации

import sys
import MessengersAPI.TelegramAPI as TelegramAPI
import MessengersAPI.FBAPI as FBAPI
import MessengersAPI.VKAPI as VKAPI
import MessengersAPI.SkypeAPI as SkypeAPI

# Запускаем прложение через номер средство коммуникации
if __name__ == '__main__':
    API = int(sys.argv[1])
    if API == 0:
        TelegramAPI.start_programm()
    elif API == 1:
        FBAPI.start_programm()
    elif API == 2:
        VKAPI.start_programm()
    elif API == 3:
        SkypeAPI.start_programm()

## Тема оформления
init -20 python:

    class Palette(object):
        """Цвета интерфейса (тёмная тема мессенджера)."""
        BG = "#0e1621"            # основной фон
        PANEL = "#17212b"         # боковая панель, шапка, меню
        PANEL_LIGHT = "#202b36"   # выделенная строка
        BUBBLE_IN = "#182533"     # входящее сообщение
        BUBBLE_OUT = "#2b5278"    # исходящее сообщение
        ACCENT = "#5eb5f7"        # акцент: ссылки, кнопки, бейджи
        TEXT = "#ffffff"
        TEXT_MUTED = "#8b9bab"
        TEXT_DIM = "#5b6b7b"
        DANGER = "#e5575f"
        SUCCESS = "#6fcf97"

    class Layout(object):
        """Координаты мессенджера на экране 1280x720."""
        SIDEBAR_W = 320
        HEADER_H = 64
        CHAT_X = 320
        CHAT_W = 960
        MESSAGES_X = 340          # область сообщений
        MESSAGES_Y = 74
        MESSAGES_W = 920
        MESSAGES_H = 556
        INPUT_Y = 646             # строка ввода
        BUBBLE_MAX_W = 560
        THOUGHT_RESERVE = 150     # место под «мысли», когда они на экране
        REPLY_ROW_H = 58          # высота одного варианта ответа

    FONT = "fonts/Nunito-SemiBold.ttf"

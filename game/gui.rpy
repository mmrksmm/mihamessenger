## Базовая настройка GUI

init offset = -2

init python:
    gui.init(1280, 720)

## Язык переноса строк
define gui.language = "unicode"

## Какие теги разрешены в экране истории
define gui.history_allow_tags = {"alt", "noalt", "rt", "rb", "art"}

## Сколько слотов сохранения на странице
define gui.file_slot_cols = 3
define gui.file_slot_rows = 2

define config.thumbnail_width = 256
define config.thumbnail_height = 144

## Длина истории диалогов
define config.history_length = 250

## Базовый стиль текста: шрифт и цвета темы
style default:
    font FONT
    size 20
    color Palette.TEXT
    outlines []
    language gui.language

style button_text is default

define config.check_conflicting_properties = True

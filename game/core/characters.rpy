init -5 python:

    def chat_character(contact):
        """Персонаж-собеседник: его строки — это входящие сообщения."""
        return Character(contact.nickname, kind=nvl, who_color=contact.color)


## Влад: сообщения в чат и мысли
define me = Character(HERO_NICK, kind=nvl, who_color=HERO_COLOR)
define think = Character(THOUGHT_NAME, kind=nvl, who_color=HERO_COLOR)

## Рассказчик и системные уведомления
define narrator = Character(None, kind=nvl)
define system = Character(SYSTEM_NAME, kind=nvl)

## Собеседники
define yora = chat_character(CONTACT["yora"])
define yana = chat_character(CONTACT["yana"])
define rimma = chat_character(CONTACT["rimma"])
define sofa = chat_character(CONTACT["sofa"])
define devyat = chat_character(CONTACT["devyat"])
define sglypa = chat_character(CONTACT["sglypa"])

## Меню выбора тоже показываются внутри мессенджера
define menu = nvl_menu

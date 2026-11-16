init -10 python:

    class Contact(object):
        """Собеседник Влада в MIHA Messenger.

        id        — короткий ключ; по нему ищутся метки сюжета
                    (<id>_day1, <id>_day2, <id>_final, <id>_good, <id>_bad)
        name      — настоящее имя персонажа
        nickname  — ник в мессенджере, его видит игрок
        color     — цвет ника и аватарки
        status    — подпись в шапке чата
        archetype — короткая характеристика (для меню выбора и README)
        """

        def __init__(self, id, name, nickname, color, status, archetype):
            self.id = id
            self.name = name
            self.nickname = nickname
            self.color = color
            self.status = status
            self.archetype = archetype

        @property
        def initial(self):
            return self.name[0].upper()

        def __repr__(self):
            return "<Contact {}>".format(self.id)


    class GroupChat(object):
        """Групповой чат. Ведёт себя как Contact там, где это нужно интерфейсу."""

        id = "group"

        def __init__(self, name, status, color):
            self.name = name
            self.nickname = name
            self.status = status
            self.color = color
            self.initial = name[0].upper()


    CONTACTS = (
        Contact("yora",   "Йора",   "Yora_cocoa",    "#f2d16b", "в сети",            "весёлая и шумная"),
        Contact("yana",   "Яна",    "Yana_star777",  "#91a1f0", "печатает…",         "милая и стеснительная"),
        Contact("rimma",  "Римма",  "hau999",        "#e6a98c", "был(а) недавно",    "молчаливая и загадочная"),
        Contact("sofa",   "Софа",   "кшктрикс",      "#a8d98a", "администратор чата", "строгая, но добрая"),
        Contact("devyat", "Девять", "yanepoel",      "#d9b3a6", "был(а) давно",      "спокойный и рассудительный"),
        Contact("sglypa", "Сглыпа", "сглыпа)",       "#7fd6e8", "бот",               "чат-бот со странностями"),
    )

    CONTACT = dict((c.id, c) for c in CONTACTS)
    CONTACT_BY_NICK = dict((c.nickname, c) for c in CONTACTS)

    GROUP = GroupChat("Тёртые калачи", "7 участников", "#5eb5f7")

    HERO_NAME = "Влад"
    HERO_NICK = "WladosAssassin"
    HERO_COLOR = "#5eb5f7"

    THOUGHT_NAME = HERO_NAME     # мысли Влада: плашка внизу экрана
    SYSTEM_NAME = "MIHA"         # уведомления: плашка по центру чата

    # Правила игры
    MAX_AFFECTION = 3            # столько очков нужно для хорошей концовки
    CHATS_PER_DAY = 2            # сколько личных чатов можно открыть за день
    GROUP_READS_PER_DAY = 2      # сколько раз за день можно заглянуть в общий чат


    def chat_info(chat_id):
        """Возвращает объект чата по id или None."""
        if chat_id is None:
            return None
        if chat_id == GROUP.id:
            return GROUP
        return CONTACT.get(chat_id)

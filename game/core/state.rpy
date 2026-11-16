## Состояние игры и функции, которые его меняют
## Очки привязанности к каждому собеседнику
default affection = dict((c.id, 0) for c in CONTACTS)

## Открытый сейчас чат (id собеседника, "group" или None)
default current_chat = None

## Номер текущего дня и с кем уже переписывались сегодня
default day = 0
default chatted_today = set()
default group_reads = 0

## Сквозные флаги сюжета: решение в одном чате влияет на другой
default vlad_threw_out_toy = False      # день 1: совет Девяти → реплика Риммы
default door_choice = None              # день 2: смотрел ли Влад в глазок

init python:

    def like(contact_id, amount=1):
        """Добавляет очки привязанности (не выше MAX_AFFECTION)."""
        value = store.affection[contact_id] + amount
        store.affection[contact_id] = max(0, min(MAX_AFFECTION, value))

    def has_max_affection(contact_id):
        return store.affection[contact_id] >= MAX_AFFECTION

    def open_chat(chat_id):
        """Открывает переписку: очищает ленту и показывает окно мессенджера."""
        store.current_chat = chat_id
        nvl_clear()
        renpy.show_screen("messenger")

    def close_chat():
        """Закрывает мессенджер (например, перед сценой в комнате)."""
        store.current_chat = None
        nvl_clear()
        renpy.hide_screen("messenger")

    def start_day(number):
        store.day = number
        store.chatted_today = set()
        store.group_reads = 0

    def can_open_private_chat(contact_id):
        return (contact_id not in store.chatted_today
                and len(store.chatted_today) < CHATS_PER_DAY)

    def can_open_group_chat():
        return store.group_reads < GROUP_READS_PER_DAY

## Концовки: список, открытие и проверка секретных концовок.
default persistent.endings = set()

init -10 python:

    class Ending(object):
        def __init__(self, id, title, hint, kind):
            self.id = id
            self.title = title    # название на карточке
            self.hint = hint      # подсказка, пока концовка закрыта
            self.kind = kind      # "good", "bad" или "secret"

        @property
        def unlocked(self):
            return self.id in persistent.endings


    ENDINGS = [
        Ending("yora_good",   "Какао на двоих",        "Йора: максимум привязанности",   "good"),
        Ending("yora_bad",    "Абонент вне зоны",      "Йора: не хватило привязанности", "bad"),
        Ending("yana_good",   "Свет в окошке",         "Яна: максимум привязанности",    "good"),
        Ending("yana_bad",    "Прочитано",             "Яна: не хватило привязанности",  "bad"),
        Ending("rimma_good",  "Каменная стена",        "Римма: максимум привязанности",  "good"),
        Ending("rimma_bad",   "Тишина в эфире",        "Римма: не хватило привязанности", "bad"),
        Ending("sofa_good",   "Администратор сердца",  "Софа: максимум привязанности",   "good"),
        Ending("sofa_bad",    "Электричка",            "Софа: не хватило привязанности", "bad"),
        Ending("devyat_good", "Напарники",             "Девять: максимум привязанности", "good"),
        Ending("devyat_bad",  "Правда страшнее",       "Девять: не хватило привязанности", "bad"),
        Ending("sglypa_good", "Человечный бот",        "Сглыпа: максимум привязанности", "good"),
        Ending("sglypa_bad",  "Ошибка 404",            "Сглыпа: не хватило привязанности", "bad"),
        Ending("secret_together", "Все вместе",        "Откройте все хорошие концовки",  "secret"),
        Ending("secret_alone",    "Выйти из сети",     "Откройте все плохие концовки",   "secret"),
    ]

    ENDING = dict((e.id, e) for e in ENDINGS)


    def unlock_ending(ending_id):
        if ending_id not in persistent.endings:
            persistent.endings.add(ending_id)
            renpy.save_persistent()

    def all_unlocked(kind):
        return all(e.unlocked for e in ENDINGS if e.kind == kind)

    def endings_progress():
        opened = sum(1 for e in ENDINGS if e.unlocked)
        return opened, len(ENDINGS)

    def pending_secret_ending():
        """Какую секретную концовку показать после титров (или None)."""
        if all_unlocked("good") and not ENDING["secret_together"].unlocked:
            return "secret_together"
        if all_unlocked("bad") and not ENDING["secret_alone"].unlocked:
            return "secret_alone"
        return None

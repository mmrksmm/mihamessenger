## Основные настройки проекта.

define config.name = _("MIHA Messenger")
define gui.show_name = True
define config.version = "2.0-demo"

define gui.about = _p("""
Короткая визуальная новелла-переписка: герой ставит новый мессенджер, попадает
в странный групповой чат и за три дня решает, кому из собеседников можно доверять.

Это демо-версия для портфолио. Реплики переписаны, сторонняя графика и музыка
удалены. Фоны в демо — простые заглушки с подписью сцены.
""")

define build.name = "miha-messenger"

## Звук

define config.has_sound = True
define config.has_music = True
define config.has_voice = False
define config.main_menu_music = "audio/calm_loop.ogg"

## Переходы

define config.enter_transition = dissolve
define config.exit_transition = dissolve
define config.intra_transition = dissolve
define config.after_load_transition = None
define config.end_game_transition = Dissolve(1.0)

## Окно диалога и скорость текста

define config.window = "auto"
define config.window_show_transition = Dissolve(.2)
define config.window_hide_transition = Dissolve(.2)
default preferences.text_cps = 45
default preferences.afm_time = 15

## Сохранения

define config.save_directory = "miha-messenger-demo"

## Иконка окна

define config.window_icon = "gui/window_icon.png"

## Сборка дистрибутива

init python:
    build.classify("**~", None)
    build.classify("**.bak", None)
    build.classify("**/.**", None)
    build.classify("**/#**", None)
    build.classify("**/thumbs.db", None)
    build.classify("tools/**", None)
    build.classify("docs/**", None)
    build.classify("**.md", None)

    build.documentation("*.html")
    build.documentation("*.txt")

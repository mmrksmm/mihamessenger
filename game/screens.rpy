## Экраны меню и служебные экраны Ren'Py.

init offset = -1


################################################################################
## Общие стили
################################################################################

style gui_text is default

style menu_button is empty:
    xsize 260
    padding (20, 10)
    background None
    hover_background Frame("gui/button_hover.png", 14, 14)
    selected_background Frame("gui/button_selected.png", 14, 14)
    insensitive_background None

style menu_button_text is default:
    size 21
    color Palette.TEXT_MUTED
    hover_color Palette.TEXT
    selected_color Palette.ACCENT
    insensitive_color Palette.TEXT_DIM

style small_button is empty:
    padding (12, 6)
    background None
    hover_background Frame("gui/button_hover.png", 14, 14)
    selected_background Frame("gui/button_selected.png", 14, 14)

style small_button_text is default:
    size 17
    color Palette.TEXT_MUTED
    hover_color Palette.TEXT
    selected_color Palette.ACCENT
    insensitive_color Palette.TEXT_DIM

style section_label_text is default:
    size 18
    bold True
    color Palette.ACCENT

style vscrollbar is empty:
    xsize 12
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", 6, 6)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", 6, 6)
    unscrollable "hide"

style slider is empty:
    ysize 24
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", 12, 12)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"


################################################################################
## Внутриигровые экраны
################################################################################

## Экран разговора (ADV). В игре все реплики идут через NVL-экран
## мессенджера, но Ren'Py требует, чтобы этот экран существовал.

screen say(who, what):
    window:
        style "say_window"
        vbox:
            spacing 4
            if who is not None:
                text who id "who" style "say_label"
            text what id "what" style "say_dialogue"

style say_window is empty:
    xalign 0.5
    yalign 1.0
    yoffset -14
    xsize 1000
    background Frame("gui/thought.png", 24, 24)
    padding (28, 16, 28, 18)

style say_label is default:
    size 16
    bold True
    color Palette.ACCENT

style say_dialogue is default:
    size 21


## Ввод текста

screen input(prompt):
    style_prefix "input"
    window:
        style "say_window"
        vbox:
            spacing 8
            text prompt style "input_prompt"
            input id "input"

style input_prompt is default:
    color Palette.TEXT_MUTED


## Обычное меню выбора (в игре используется nvl_menu, это запасной вариант)

screen choice(items):
    vbox:
        style "reply_vbox"
        xcenter 640
        for i in items:
            textbutton i.caption:
                style "reply_button"
                text_style "reply_button_text"
                action i.action


## Быстрое меню — справа в шапке мессенджера

screen quick_menu():
    zorder 100

    if quick_menu:
        hbox:
            style_prefix "quick"
            xalign 1.0
            ypos 14
            xoffset -16
            spacing 2

            textbutton _("Назад") action Rollback()
            textbutton _("История") action ShowMenu("history")
            textbutton _("Пропуск") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Авто") action Preference("auto-forward", "toggle")
            textbutton _("Сохр.") action ShowMenu("save")
            textbutton _("Меню") action ShowMenu("preferences")

init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_button is small_button
style quick_button_text is small_button_text:
    size 15


################################################################################
## Главное и игровое меню
################################################################################

screen navigation():
    vbox:
        style_prefix "menu"
        spacing 4

        if main_menu:
            textbutton _("Начать") action Start()
        else:
            textbutton _("История") action ShowMenu("history")
            textbutton _("Сохранить") action ShowMenu("save")

        textbutton _("Загрузить") action ShowMenu("load")
        textbutton _("Концовки") action ShowMenu("endings")
        textbutton _("Настройки") action ShowMenu("preferences")

        if _in_replay:
            textbutton _("Завершить повтор") action EndReplay(confirm=True)
        elif not main_menu:
            textbutton _("Главное меню") action MainMenu()

        textbutton _("Об игре") action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):
            textbutton _("Помощь") action ShowMenu("help")

        if renpy.variant("pc"):
            textbutton _("Выход") action Quit(confirm=not main_menu)


screen main_menu():
    tag menu

    add "gui/main_menu_bg.png"

    vbox:
        xpos 90
        yalign 0.5
        spacing 36

        hbox:
            spacing 18
            add Transform("gui/window_icon.png", xysize=(84, 84)) yalign 0.5
            vbox:
                yalign 0.5
                text "MIHA" style "main_menu_title"
                text "messenger" style "main_menu_subtitle"

        use navigation

    hbox:
        xpos 90
        yalign 1.0
        yoffset -28
        spacing 14
        frame:
            style "demo_badge"
            text "DEMO" style "demo_badge_text"
        text "версия [config.version]" style "main_menu_version" yalign 0.5

style main_menu_title is default:
    size 64
    bold True
    kerning 6
    color Palette.TEXT

style main_menu_subtitle is default:
    size 22
    kerning 8
    color Palette.ACCENT

style main_menu_version is default:
    size 15
    color Palette.TEXT_DIM

style demo_badge is empty:
    background Frame("gui/pill.png", 24, 24)
    padding (14, 4)

style demo_badge_text is default:
    size 14
    bold True
    kerning 3
    color Palette.ACCENT


## Каркас всех внутренних меню: слева навигация, справа содержимое

screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):
    tag menu

    add Solid(Palette.BG)

    frame:
        style "game_menu_sidebar"
        fixed:
            vbox:
                spacing 24
                hbox:
                    spacing 12
                    add Transform("gui/window_icon.png", xysize=(40, 40)) yalign 0.5
                    text "MIHA" style "logo_text" yalign 0.5
                use navigation

            textbutton _("Вернуться"):
                style "menu_button"
                yalign 1.0
                action Return()

    frame:
        style "game_menu_content"

        vbox:
            spacing 20
            text title style "game_menu_title"

            if scroll == "viewport":
                viewport:
                    yinitial yinitial
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    pagekeys True
                    side_spacing 12
                    vbox:
                        spacing spacing
                        transclude

            elif scroll == "vpgrid":
                vpgrid:
                    cols 1
                    yinitial yinitial
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    pagekeys True
                    side_spacing 12
                    spacing spacing
                    transclude

            else:
                transclude

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")

style game_menu_sidebar is empty:
    xsize 320
    yfill True
    background Solid(Palette.PANEL)
    padding (30, 34, 30, 30)

style game_menu_content is empty:
    xpos 380
    ypos 40
    xsize 840
    ysize 640

style game_menu_title is default:
    size 34
    bold True
    color Palette.TEXT


## Об игре

screen about():
    tag menu

    use game_menu(_("Об игре"), scroll="viewport"):
        vbox:
            spacing 14
            xsize 800
            text "[config.name!t] · версия [config.version]" style "section_label_text"
            text "[gui.about!t]"
            text _("Сделано на {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].")
            text _("Шрифт Nunito распространяется по лицензии SIL Open Font License 1.1.") style "about_small"

style about_small is default:
    size 16
    color Palette.TEXT_MUTED


## Сохранение и загрузка

screen save():
    tag menu
    use file_slots(_("Сохранить"))

screen load():
    tag menu
    use file_slots(_("Загрузить"))

screen file_slots(title):

    default page_name_value = FilePageNameInputValue(
        pattern=_("Страница {}"), auto=_("Автосохранения"), quick=_("Быстрые сохранения"))

    use game_menu(title):

        vbox:
            spacing 18

            button:
                style "page_label"
                key_events True
                action page_name_value.Toggle()
                input:
                    style "page_label_text"
                    value page_name_value

            grid gui.file_slot_cols gui.file_slot_rows:
                spacing 14

                for i in range(gui.file_slot_cols * gui.file_slot_rows):
                    $ slot = i + 1

                    button:
                        style "slot_button"
                        action FileAction(slot)

                        vbox:
                            spacing 6
                            add FileScreenshot(slot) xalign 0.5
                            text FileTime(slot, format=_("{#file_time}%d.%m.%Y, %H:%M"), empty=_("Пустой слот")):
                                style "slot_text"
                            text FileSaveName(slot) style "slot_text"

                        key "save_delete" action FileDelete(slot)

            hbox:
                style_prefix "small"
                spacing 4
                xalign 0.5

                textbutton _("<") action FilePagePrevious()
                if config.has_autosave:
                    textbutton _("{#auto_page}А") action FilePage("auto")
                if config.has_quicksave:
                    textbutton _("{#quick_page}Б") action FilePage("quick")
                for page in range(1, 10):
                    textbutton "[page]" action FilePage(page)
                textbutton _(">") action FilePageNext()

style page_label is empty:
    xalign 0.5
    padding (20, 4)

style page_label_text is default:
    size 20
    color Palette.TEXT_MUTED
    hover_color Palette.ACCENT
    textalign 0.5

style slot_button is empty:
    xsize 272
    padding (8, 8)
    background Frame("gui/panel.png", 14, 14)
    hover_background Frame("gui/button_hover.png", 14, 14)

style slot_text is default:
    size 14
    color Palette.TEXT_MUTED
    xalign 0.5
    textalign 0.5


## Настройки

screen preferences():
    tag menu

    use game_menu(_("Настройки"), scroll="viewport"):

        vbox:
            spacing 26

            hbox:
                spacing 60

                if renpy.variant("pc") or renpy.variant("web"):
                    vbox:
                        style_prefix "check"
                        text _("Экран") style "section_label_text"
                        textbutton _("Оконный") action Preference("display", "window")
                        textbutton _("Полный") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "check"
                    text _("Пропуск") style "section_label_text"
                    textbutton _("Всего текста") action Preference("skip", "toggle")
                    textbutton _("После выборов") action Preference("after choices", "toggle")
                    textbutton _("Переходов") action InvertSelected(Preference("transitions", "toggle"))

            vbox:
                spacing 10
                text _("Скорость текста") style "section_label_text"
                bar value Preference("text speed") style "slider" xsize 420

                text _("Скорость автопрокрутки") style "section_label_text"
                bar value Preference("auto-forward time") style "slider" xsize 420

                text _("Громкость музыки") style "section_label_text"
                bar value Preference("music volume") style "slider" xsize 420

                text _("Громкость звуков") style "section_label_text"
                bar value Preference("sound volume") style "slider" xsize 420

                null height 6
                textbutton _("Без звука"):
                    style "check_button"
                    text_style "check_button_text"
                    action Preference("all mute", "toggle")

style check_vbox is vbox:
    spacing 4

style check_button is empty:
    padding (34, 6, 10, 6)
    foreground "gui/button/check_[prefix_]foreground.png"
    hover_background Frame("gui/button_selected.png", 14, 14)

style check_button_text is default:
    size 19
    color Palette.TEXT_MUTED
    hover_color Palette.TEXT
    selected_color Palette.TEXT


## История

screen history():
    tag menu
    predict False

    use game_menu(_("История"), scroll="viewport", yinitial=1.0, spacing=14):

        for h in _history_list:
            vbox:
                spacing 2
                if h.who:
                    text h.who style "history_name":
                        substitute False
                        if "color" in h.who_args:
                            color h.who_args["color"]
                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what style "history_text":
                    substitute False

        if not _history_list:
            text _("История диалогов пуста.") style "history_text"

style history_name is default:
    size 16
    bold True
    color Palette.ACCENT

style history_text is default:
    size 19
    xmaximum 780


## Помощь

screen help():
    tag menu

    default device = "keyboard"

    use game_menu(_("Помощь"), scroll="viewport"):

        vbox:
            spacing 18

            hbox:
                style_prefix "small"
                spacing 6
                textbutton _("Клавиатура") action SetScreenVariable("device", "keyboard")
                textbutton _("Мышь") action SetScreenVariable("device", "mouse")

            if device == "keyboard":
                use help_rows([
                    (_("Enter / Пробел"), _("Следующая реплика, выбор варианта.")),
                    (_("Стрелки"), _("Перемещение между вариантами ответа.")),
                    (_("Escape"), _("Игровое меню.")),
                    (_("Ctrl"), _("Пропуск текста, пока клавиша зажата.")),
                    (_("Tab"), _("Включить или выключить пропуск.")),
                    (_("Page Up"), _("Вернуться к предыдущей реплике.")),
                    (_("H"), _("Скрыть интерфейс.")),
                    (_("S"), _("Сделать скриншот.")),
                ])
            else:
                use help_rows([
                    (_("Левый клик"), _("Следующая реплика, выбор варианта.")),
                    (_("Правый клик"), _("Игровое меню.")),
                    (_("Колесо вверх"), _("Вернуться к предыдущей реплике / прокрутить чат.")),
                    (_("Колесо вниз"), _("Вперёд по уже прочитанному.")),
                ])

screen help_rows(rows):
    vbox:
        spacing 10
        for key_name, description in rows:
            hbox:
                text key_name style "help_key"
                text description style "help_text"

style help_key is default:
    xsize 220
    bold True
    color Palette.ACCENT

style help_text is default:
    color Palette.TEXT


################################################################################
## Служебные экраны
################################################################################

## Подтверждение (выход, перезапись сохранения и т. п.)

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200

    add "gui/overlay/confirm.png"

    frame:
        style "confirm_frame"
        vbox:
            spacing 26
            text _(message) style "confirm_text"
            hbox:
                xalign 0.5
                spacing 40
                textbutton _("Да") style "menu_button" action yes_action
                textbutton _("Нет") style "menu_button" action no_action

    key "game_menu" action no_action

style confirm_frame is empty:
    align (0.5, 0.5)
    background Frame("gui/panel_outline.png", 14, 14)
    padding (50, 40)

style confirm_text is default:
    xalign 0.5
    textalign 0.5
    size 22
    xmaximum 600


## Индикатор пропуска

screen skip_indicator():
    zorder 100
    frame:
        style "skip_frame"
        text _("Пропускаю…") style "skip_text"

style skip_frame is empty:
    xpos 340
    ypos 76
    background Frame("gui/pill.png", 24, 24)
    padding (16, 5)

style skip_text is default:
    size 15
    color Palette.ACCENT


## Уведомления (например, о быстром сохранении)

screen notify(message):
    zorder 100
    frame at notify_appear:
        style "skip_frame"
        text "[message!tq]" style "skip_text"
    timer 3.25 action Hide("notify")

transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0

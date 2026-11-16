## Интерфейс мессенджера MIHA.
##
## Окно мессенджера собрано из экранов Ren'Py: боковая панель со списком чатов,
## шапка, лента сообщений «пузырями», строка ввода и варианты ответа.
##
## Как это устроено:
##   * экран messenger — «рамка» приложения, показывается функцией open_chat();
##   * экран nvl — стандартный экран Ren'Py для NVL-режима; здесь он рисует
##     ленту сообщений, мысли Влада и варианты ответа (меню);
##   * экран chat_picker — та же рамка, но строки списка чатов кликабельны,
##     через него игрок выбирает, кому написать.

init -1 python:

    def avatar(chat, size=44):
        """Круглая аватарка из images/avatars/<id>.png нужного размера."""
        return Transform("images/avatars/{}.png".format(chat.id), xysize=(size, size))

    def sidebar_chats():
        return [GROUP] + list(CONTACTS)

    def chat_allowed(chat_id, final=False):
        """Можно ли открыть чат в режиме выбора."""
        if final:
            return chat_id != GROUP.id
        if chat_id == GROUP.id:
            return can_open_group_chat()
        return can_open_private_chat(chat_id)

    def plural_ru(n, one, few, many):
        """Склонение по числу: 1 чат, 2 чата, 5 чатов."""
        if n % 10 == 1 and n % 100 != 11:
            return one
        if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
            return few
        return many

    def chats_left_text():
        left = CHATS_PER_DAY - len(store.chatted_today)
        return "Сегодня можно открыть ещё {} {}".format(
            left, plural_ru(left, "личный чат", "личных чата", "личных чатов"))

    def debug_affection_text():
        return "debug: " + "  ".join(
            "{}{}".format(c.initial, store.affection[c.id]) for c in CONTACTS)

    def is_overlay_line(entry):
        """Мысли Влада и слова рассказчика показываются плашкой, а не в ленте."""
        return entry.who is None or entry.who == THOUGHT_NAME


################################################################################
## Рамка приложения
################################################################################

screen messenger():
    zorder 0
    use messenger_layout(picker=False, final=False)


screen chat_picker(final=False):
    ## Вызывается через call screen: возвращает id выбранного чата.
    modal True
    zorder 5
    use messenger_layout(picker=True, final=final)


screen messenger_layout(picker, final):
    $ chat = None if picker else chat_info(current_chat)

    add Solid(Palette.BG)

    use messenger_sidebar(picker, final)

    ## Шапка чата
    frame:
        style "chat_header"
        if chat is not None:
            hbox:
                spacing 14
                yalign 0.5
                add avatar(chat, 40) yalign 0.5
                vbox:
                    yalign 0.5
                    text chat.nickname style "chat_header_title" color chat.color
                    text chat.status style "chat_header_status"
        else:
            text "MIHA Messenger" style "chat_header_title" yalign 0.5

    ## Строка ввода (декоративная: ответы выбираются вариантами)
    frame:
        style "input_bar"
        hbox:
            yalign 0.5
            xfill True
            text "Написать сообщение…" style "input_placeholder" yalign 0.5
            add Transform("gui/window_icon.png", xysize=(32, 32)):
                xalign 1.0
                yalign 0.5

    if picker:
        vbox:
            xcenter (Layout.CHAT_X + Layout.CHAT_W // 2)
            ycenter 330
            spacing 12
            if final:
                text "Кому ты доверяешь больше всего?" style "picker_title"
                text "Этот выбор нельзя будет изменить." style "picker_hint"
            else:
                text "Кому написать?" style "picker_title"
                text chats_left_text() style "picker_hint"
                if can_open_group_chat():
                    text "Загляни в «Тёртых калачей» — это не тратит ход." style "picker_hint"


screen messenger_sidebar(picker, final):

    frame:
        style "sidebar"

        vbox:
            spacing 6

            ## Логотип
            hbox:
                spacing 10
                ysize (Layout.HEADER_H - 8)
                add Transform("gui/window_icon.png", xysize=(34, 34)) yalign 0.5
                text "MIHA" style "logo_text" yalign 0.5

            ## Поиск (декорация)
            frame:
                style "search_box"
                text "Поиск" style "input_placeholder"

            null height 4

            for c in sidebar_chats():
                use chat_row(c, picker, final)

    ## Номер дня и (в режиме разработчика) очки привязанности
    vbox:
        xpos 22
        yalign 1.0
        yoffset -16
        spacing 2
        if day:
            text "День [day] из 3" style "sidebar_footer"
        if config.developer:
            ## Видно только при запуске из лаунчера: удобно проверять ветки
            text debug_affection_text() style "sidebar_footer"


screen chat_row(chat, picker, final):
    $ is_open = (not picker) and current_chat == chat.id
    $ allowed = picker and chat_allowed(chat.id, final)
    $ unread = picker and allowed and chat.id != GROUP.id

    button:
        style "chat_row"
        selected is_open
        action If(allowed, Return(chat.id), None)

        hbox:
            spacing 12
            add avatar(chat, 44) yalign 0.5
            vbox:
                yalign 0.5
                xsize 200
                text chat.nickname style "chat_row_title":
                    color (Palette.TEXT_DIM if (picker and not allowed) else Palette.TEXT)
                text chat.status style "chat_row_status"
            if unread:
                frame:
                    style "unread_badge"
                    text "1" style "unread_badge_text"


################################################################################
## Экран NVL: лента сообщений, мысли, варианты ответа
################################################################################

screen nvl(dialogue, items=None):
    zorder 10

    $ chat = chat_info(current_chat)
    $ last = dialogue[-1] if dialogue else None
    $ show_overlay = (not items) and last is not None and is_overlay_line(last)
    $ reserve = (len(items) * Layout.REPLY_ROW_H + 100) if items else (Layout.THOUGHT_RESERVE if show_overlay else 0)

    if chat is not None:

        ## Лента. Пустой блок сверху высотой во всю область гарантирует, что
        ## содержимое всегда «длиннее» окна, а yinitial 1.0 прокручивает его вниз:
        ## новые сообщения прижаты к низу, как в настоящем мессенджере.
        viewport:
            xpos Layout.MESSAGES_X
            ypos Layout.MESSAGES_Y
            xysize (Layout.MESSAGES_W, Layout.MESSAGES_H - reserve)
            yinitial 1.0
            mousewheel True

            vbox:
                xsize (Layout.MESSAGES_W - 20)
                spacing 8
                null height Layout.MESSAGES_H

                for d in dialogue:
                    if d.who == SYSTEM_NAME:
                        use chat_notice(d)
                    elif not is_overlay_line(d):
                        use chat_bubble(d, chat)

                null height 4

    elif last is not None and not show_overlay and not items:
        ## Мессенджер закрыт, но пришло сообщение — показываем всплывашку.
        use toast(last)

    if show_overlay:
        use thought_box(last, chat is not None)

    if items:
        vbox:
            style "reply_vbox"
            if chat is None:
                xcenter 640
            for i in items:
                textbutton i.caption:
                    style "reply_button"
                    text_style "reply_button_text"
                    action i.action


screen chat_bubble(d, chat):
    $ mine = (d.who == HERO_NICK)
    $ sender = CONTACT_BY_NICK.get(d.who)
    $ in_group = (chat.id == GROUP.id)

    hbox:
        xalign (1.0 if mine else 0.0)
        spacing 10

        if in_group and not mine:
            if sender is not None:
                add avatar(sender, 34) yalign 1.0
            else:
                null width 34

        frame:
            style ("bubble_out" if mine else "bubble_in")
            vbox:
                spacing 2
                if in_group and not mine:
                    text d.who id d.who_id style "bubble_name"
                text d.what id d.what_id style "bubble_text"


screen chat_notice(d):
    frame:
        style "notice_frame"
        text d.what id d.what_id style "notice_text"


screen thought_box(d, in_chat):
    frame:
        style "thought_frame"
        if in_chat:
            xcenter (Layout.CHAT_X + Layout.CHAT_W // 2)
            xsize (Layout.MESSAGES_W - 20)
        vbox:
            spacing 4
            if d.who is not None:
                text d.who id d.who_id style "thought_who"
            text d.what id d.what_id style ("thought_text" if d.who is not None else "narration_text")


screen toast(d):
    $ sender = CONTACT_BY_NICK.get(d.who)
    frame:
        style "toast_frame"
        hbox:
            spacing 12
            if sender is not None:
                add avatar(sender, 40) yalign 0.5
            vbox:
                yalign 0.5
                if d.who is not None:
                    text d.who id d.who_id style "bubble_name"
                text d.what id d.what_id style "bubble_text"


################################################################################
## Стили
################################################################################

style sidebar is empty:
    xpos 0
    ypos 0
    xsize Layout.SIDEBAR_W
    ysize 720
    background Solid(Palette.PANEL)
    padding (12, 6, 12, 6)

style logo_text is default:
    size 28
    bold True
    color Palette.TEXT
    kerning 2

style search_box is empty:
    background Frame("gui/pill.png", 24, 24)
    xfill True
    padding (18, 9)

style chat_row is empty:
    xfill True
    padding (10, 8)
    background None
    hover_background Frame("gui/button_selected.png", 14, 14)
    selected_background Frame("gui/button_hover.png", 14, 14)
    selected_insensitive_background Frame("gui/button_hover.png", 14, 14)
    hover_sound None

style chat_row_title is default:
    size 19
    color Palette.TEXT
    bold True

style chat_row_status is default:
    size 15
    color Palette.TEXT_MUTED

style unread_badge is empty:
    background Frame("gui/button_hover.png", 12, 12)
    xysize (24, 24)
    yalign 0.5

style unread_badge_text is default:
    size 14
    bold True
    color Palette.TEXT
    xalign 0.5
    yalign 0.5

style sidebar_footer is default:
    size 14
    color Palette.TEXT_DIM

style chat_header is empty:
    xpos Layout.CHAT_X
    ypos 0
    xsize Layout.CHAT_W
    ysize Layout.HEADER_H
    background Solid(Palette.PANEL)
    padding (22, 0)

style chat_header_title is default:
    size 21
    bold True
    color Palette.TEXT

style chat_header_status is default:
    size 15
    color Palette.TEXT_MUTED

style input_bar is empty:
    xpos Layout.MESSAGES_X
    ypos Layout.INPUT_Y
    xsize Layout.MESSAGES_W
    ysize 54
    background Frame("gui/panel.png", 14, 14)
    padding (20, 0, 12, 0)

style input_placeholder is default:
    size 18
    color Palette.TEXT_DIM

style picker_title is default:
    size 34
    bold True
    color Palette.TEXT
    xalign 0.5

style picker_hint is default:
    size 18
    color Palette.TEXT_MUTED
    xalign 0.5

style bubble_in is empty:
    background Frame("gui/bubble_in.png", 18, 18)
    padding (16, 10, 16, 11)

style bubble_out is bubble_in:
    background Frame("gui/bubble_out.png", 18, 18)

style bubble_name is default:
    size 15
    bold True

style bubble_text is default:
    size 20
    color Palette.TEXT
    xmaximum Layout.BUBBLE_MAX_W
    line_spacing 2

style notice_frame is empty:
    xalign 0.5
    background Frame("gui/pill.png", 24, 24)
    padding (18, 6)

style notice_text is default:
    size 15
    color Palette.TEXT_MUTED
    textalign 0.5

style thought_frame is empty:
    xalign 0.5
    yalign 1.0
    yoffset -14
    xsize 1000
    background Frame("gui/thought.png", 24, 24)
    padding (28, 16, 28, 18)

style thought_who is default:
    size 15
    bold True
    color Palette.ACCENT

style thought_text is default:
    size 21
    color "#e8eef5"
    line_spacing 3

style narration_text is thought_text:
    color "#c9d3dd"

style toast_frame is empty:
    xcenter (Layout.CHAT_X + Layout.CHAT_W // 2)
    ypos 84
    background Frame("gui/panel_outline.png", 14, 14)
    padding (18, 12, 22, 12)

style reply_vbox is vbox:
    xcenter (Layout.CHAT_X + Layout.CHAT_W // 2)
    yalign 1.0
    yoffset -86
    spacing 8

style reply_button is empty:
    xsize (Layout.MESSAGES_W - 60)
    ysize (Layout.REPLY_ROW_H - 8)
    background Frame("gui/reply_idle.png", 16, 16)
    hover_background Frame("gui/reply_hover.png", 16, 16)
    padding (22, 0)

style reply_button_text is default:
    size 19
    yalign 0.5
    color Palette.TEXT
    hover_color Palette.TEXT

## Особые экраны: заставка дня, «подстроенный» выбор, галерея концовок, титры.

################################################################################
## Заставка нового дня
################################################################################

screen day_card(date, subtitle):
    zorder 20
    vbox:
        align (0.5, 0.45)
        spacing 6
        text date style "day_card_date"
        text subtitle style "day_card_subtitle"

style day_card_date is default:
    size 56
    bold True
    color Palette.TEXT
    xalign 0.5

style day_card_subtitle is default:
    size 20
    color Palette.TEXT_MUTED
    kerning 4
    xalign 0.5


################################################################################
## Подстроенный выбор
##
## Игроку предлагают два варианта, но курсор сам «притягивается» к одному из
## них. Кнопки стоят в фиксированных точках, поэтому координаты цели известны
## заранее (в первой версии они были подобраны вручную под конкретный фон).
################################################################################

define RIGGED_TARGET = (640, 350)

init python:

    def pull_mouse_to(x, y):
        """Плавно переводит курсор в точку (x, y), если он ушёл в сторону."""
        if renpy.variant("touch") or renpy.variant("web"):
            return
        mx, my = renpy.get_mouse_pos()
        if abs(mx - x) > 6 or abs(my - y) > 6:
            renpy.set_mouse_pos(x, y, 0.12)


screen rigged_choice(question, forced, other):
    modal True
    zorder 20

    add Solid("#000000f5")

    text question style "picker_title":
        xalign 0.5
        ycenter 260

    textbutton forced:
        style "reply_button"
        text_style "rigged_button_text"
        xsize 420
        xcenter RIGGED_TARGET[0]
        ycenter RIGGED_TARGET[1]
        action Return("forced")

    textbutton other:
        style "reply_button"
        text_style "rigged_button_text"
        xsize 420
        xcenter RIGGED_TARGET[0]
        ycenter (RIGGED_TARGET[1] + 70)
        action Return("other")

    timer 0.05 repeat True action Function(pull_mouse_to, RIGGED_TARGET[0], RIGGED_TARGET[1])

style rigged_button_text is reply_button_text:
    xalign 0.5


################################################################################
## Галерея концовок (кнопка «Концовки» в главном меню)
################################################################################

screen endings():
    tag menu

    use game_menu(_("Концовки"), scroll="viewport"):

        vbox:
            spacing 14

            $ opened, total = endings_progress()
            text _("Открыто концовок: [opened] из [total]") style "endings_progress"

            for c in CONTACTS:
                hbox:
                    spacing 14
                    add avatar(c, 52) yalign 0.5
                    use ending_tile(ENDING[c.id + "_good"])
                    use ending_tile(ENDING[c.id + "_bad"])

            null height 6
            hbox:
                spacing 14
                null width 52
                use ending_tile(ENDING["secret_together"])
                use ending_tile(ENDING["secret_alone"])


screen ending_tile(e):
    frame:
        style "ending_tile"
        vbox:
            yalign 0.5
            spacing 2
            if e.unlocked:
                text e.title style "ending_title"
                text ENDING_KIND_LABEL[e.kind] style "ending_kind"
            else:
                text "???" style "ending_title" color Palette.TEXT_DIM
                text e.hint style "ending_kind"

define ENDING_KIND_LABEL = {
    "good": "хорошая концовка",
    "bad": "плохая концовка",
    "secret": "секретная концовка",
}

style endings_progress is default:
    size 18
    color Palette.TEXT_MUTED

style ending_tile is empty:
    xsize 330
    ysize 72
    background Frame("gui/panel.png", 14, 14)
    padding (18, 8)

style ending_title is default:
    size 19
    bold True
    color Palette.TEXT

style ending_kind is default:
    size 14
    color Palette.TEXT_MUTED


################################################################################
## Титры
################################################################################

transform credits_scroll(duration=26.0):
    xalign 0.5
    ypos 1.0 yanchor 0.0
    linear duration ypos 0.0 yanchor 1.0

screen credits_roll():
    zorder 20
    vbox at credits_scroll:
        spacing 10
        text "MIHA Messenger" style "credits_title"
        text "демо-версия" style "credits_role"
        null height 50
        for role, people in CREDITS:
            text role style "credits_role"
            text people style "credits_name"
            null height 26
        null height 30
        text "Спасибо, что поиграли!" style "credits_title"

define CREDITS = [
    ("Программирование, интерфейс, геймдизайн", "Яна"),
    ("Сюжет и персонажи", "Яна и друзья"),
    ("Шрифт", "Nunito — SIL Open Font License 1.1"),
    ("Движок", "Ren'Py"),
]

style credits_title is default:
    size 44
    bold True
    color Palette.TEXT
    xalign 0.5

style credits_role is default:
    size 17
    color Palette.TEXT_MUTED
    kerning 2
    xalign 0.5

style credits_name is default:
    size 26
    color Palette.TEXT
    xalign 0.5
    textalign 0.5

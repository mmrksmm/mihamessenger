## Фоны и картинки для сцен вне мессенджера.
##
## В демо-версии вместо иллюстраций — простые фоны-заглушки с подписью сцены.
## Чтобы заменить их на свои арты, достаточно положить новый файл с тем же именем.

image bg black = Solid("#000")
image bg room = "images/bg/room.png"
image bg room_night = "images/bg/room_night.png"
image bg doorstep = "images/bg/doorstep.png"
image bg street = "images/bg/street.png"
image bg peephole = "images/bg/peephole.png"
image bg news = "images/bg/news.png"

image phone apps_down = "images/phone/apps_down.png"
image phone store = "images/phone/store.png"
image phone permissions = "images/phone/permissions.png"

image note = "images/note.png"

## Карточки концовок: images/endings/<id концовки>.png
image ending yora_good = "images/endings/yora_good.png"
image ending yora_bad = "images/endings/yora_bad.png"
image ending yana_good = "images/endings/yana_good.png"
image ending yana_bad = "images/endings/yana_bad.png"
image ending rimma_good = "images/endings/rimma_good.png"
image ending rimma_bad = "images/endings/rimma_bad.png"
image ending sofa_good = "images/endings/sofa_good.png"
image ending sofa_bad = "images/endings/sofa_bad.png"
image ending devyat_good = "images/endings/devyat_good.png"
image ending devyat_bad = "images/endings/devyat_bad.png"
image ending sglypa_good = "images/endings/sglypa_good.png"
image ending sglypa_bad = "images/endings/sglypa_bad.png"
image ending secret_together = "images/endings/secret_together.png"
image ending secret_alone = "images/endings/secret_alone.png"


## --- Анимации ------------------------------------------------------------------

## Лёгкое «дыхание» экрана в напряжённые моменты (было leap2 в первой версии)
transform shiver(amount=0.004, period=0.12):
    yzoom 1.0
    easein (period * 0.5) yzoom (1.0 + amount) xzoom (1.0 - amount)
    easeout (period * 0.5) yzoom 1.0 xzoom 1.0
    repeat

## Глазок: камера медленно «плывёт»
transform peephole_drift:
    zoom 1.05 xalign 0.5 yalign 0.5
    ease 3.0 zoom 1.1 xalign 0.45
    ease 3.0 zoom 1.05 xalign 0.55
    repeat

transform note_appear:
    alpha 0.0
    easein 0.6 alpha 1.0

define flash = Fade(0.1, 0.0, 0.5, color="#fff")


## --- Стикеры для переписки: {image=sticker_heart} и т. д. ----------------------

image sticker_heart = Transform("images/stickers/heart.png", zoom=0.55)
image sticker_star = Transform("images/stickers/star.png", zoom=0.55)
image sticker_cookie = Transform("images/stickers/cookie.png", zoom=0.55)
image sticker_question = Transform("images/stickers/question.png", zoom=0.55)
image sticker_smile = Transform("images/stickers/smile.png", zoom=0.55)

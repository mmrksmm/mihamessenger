## Секретные концовки. Показываются после титров один раз — когда открыты
## все хорошие или все плохие концовки (см. pending_secret_ending()).

label secret_together:
    scene ending secret_together with Dissolve(2.0)
    pause 2.0
    "Прошло несколько дней с тех пор, как я установил MIHA."

    play music calm fadein 2.0
    $ open_chat(GROUP.id)
    with Dissolve(0.5)
    system "сглыпа) снова в чате"
    sglypa "всем привет. я вернулся. теперь без камеры"
    sofa "Внимание! Внеплановый опрос!"
    sofa "Какое сегодня число?"
    yana "21 ноября!!"
    yora "А что у нас 21 ноября?)"
    rimma "у кого-то день рождения"
    devyat "с днём рождения, влад"
    play sound notify
    yana "С днём рождения, Владик!! ^_^"
    yora "С днюхой! Какао с меня)"
    rimma "{image=sticker_heart}"
    sofa "Ну… с днём рождения. Н-не то чтобы мне было не всё равно!"
    sglypa "с днём владик, мальчик"
    me "Вы… вы что, всё это время готовили сюрприз?"
    devyat "ну, не всё время. но большую часть"
    think "Странная у меня компания."
    think "Но это моя компания."

    $ close_chat()
    scene bg black with Dissolve(2.0)
    show screen day_card("Все вместе", "С Е К Р Е Т Н А Я   К О Н Ц О В К А")
    with Dissolve(1.5)
    pause 3.0
    hide screen day_card
    with Dissolve(1.5)
    stop music fadeout 2.0
    return


label secret_alone:
    scene ending secret_alone with Dissolve(2.0)
    pause 2.0
    think "Очередной провал."
    think "Я больше так не могу."
    "Я удалил MIHA. Насовсем."
    "Впервые за неделю я вышел на улицу."

    play music calm fadein 3.0
    scene bg street with Dissolve(1.5)
    "У подъезда стоял парень с коробкой плюшевых игрушек."
    think "Не может быть… Девять?"
    "Он поднял голову и кивнул мне: «Привет, Влад. Я же говорил — будь осторожен»."
    "Оказалось, он живёт в соседнем дворе и тоже удалил приложение."
    "До вечера мы гуляли и говорили обо всём. Вживую, без камер и ботов."
    think "Иногда, чтобы найти друзей, нужно просто выйти из сети."

    scene bg black with Dissolve(2.0)
    show screen day_card("Выйти из сети", "С Е К Р Е Т Н А Я   К О Н Ц О В К А")
    with Dissolve(1.5)
    pause 3.0
    hide screen day_card
    with Dissolve(1.5)
    stop music fadeout 2.0
    return

## Общие механики сюжета, которые используются в каждом дне

## Заставка нового дня: дата и подзаголовок на чёрном фоне
label day_title(date, subtitle):
    $ close_chat()
    scene bg black with Dissolve(1.0)
    show screen day_card(date, subtitle)
    with Dissolve(1.5)
    pause 2.5
    hide screen day_card
    with Dissolve(1.5)
    return


## Затемнение в конце переписки: мессенджер закрывается, дальше — мысли Влада
label fade_out_chat:
    $ close_chat()
    scene bg black
    with Dissolve(1.2)
    return


## Уведомление о новом сообщении
label new_message(contact_id):
    $ sender_nick = CONTACT[contact_id].nickname
    play sound notify
    system "Новое сообщение от [sender_nick]"
    return


label free_chats:
    while len(chatted_today) < CHATS_PER_DAY:
        $ close_chat()
        call screen chat_picker
        $ chosen = _return

        if chosen == GROUP.id:
            $ group_reads += 1
            $ open_chat(GROUP.id)
            with Dissolve(0.3)
            call expression "group_day{}_{}".format(day, group_reads) from _call_expression_1
        else:
            $ chatted_today.add(chosen)
            $ open_chat(chosen)
            with Dissolve(0.3)
            call expression "{}_day{}".format(chosen, day) from _call_expression_2

    $ close_chat()
    return


label final_choice:
    $ close_chat()
    call screen chat_picker(final=True)
    $ chosen = _return

    $ like(chosen)
    $ open_chat(chosen)
    with Dissolve(0.5)
    call expression chosen + "_final" from _call_expression_3

    $ ending = chosen + ("_good" if has_max_affection(chosen) else "_bad")
    $ close_chat()
    call expression ending from _call_expression_4
    $ unlock_ending(ending)
    $ renpy.notify("Открыта концовка: «{}»".format(ENDING[ending].title))
    return


## Титры
label credits:
    $ close_chat()
    scene bg black with Dissolve(2.0)
    play music calm fadein 2.0
    show screen credits_roll
    $ renpy.pause(27.0)
    hide screen credits_roll
    with Dissolve(1.0)
    stop music fadeout 2.0
    return

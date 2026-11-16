## Точка входа. Здесь только «скелет» сюжета — что за чем идёт.
## Сами сцены лежат в папке story/:
##   story/common.rpy       — общие механики: свободный выбор чатов, финал, титры
##   story/prologue.rpy     — пролог и три дня основной истории
##   story/characters/*.rpy — личные переписки с каждым персонажем
##   story/secret.rpy       — секретные концовки

label start:

    call prologue from _call_prologue
    call day_one from _call_day_one
    call day_two from _call_day_two
    call day_three from _call_day_three      # заканчивается финальным выбором и концовкой

    call credits from _call_credits

    ## Секретная концовка открывается, когда собраны все хорошие
    ## или все плохие концовки
    $ secret = pending_secret_ending()
    if secret:
        call expression secret from _call_expression
        $ unlock_ending(secret)

    return

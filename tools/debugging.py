import time

start_time = time.time()


def timer(text: str, timer_on=True) -> None:
    """
    Timer zum debugging mit Textinhalt
    :param text: Textstring der in der Konsole mit der vergangenen Zeit dargestellt wird
    :param timer_on: Schalter zum deaktivieren des Timers
    :return:
    """
    if timer_on:
        print("--- %s seconds ---" % round(time.time() - start_time, 1), text)


def function_counter() -> None:
    """
    Innerhalb einer Funktion ausführen, zeigt im Terminal wie oft die Funktion im Programmlauf aufgerufen wird
    :return:
    """
    function_counter.counter += 1
    print(function_counter.counter)


function_counter.counter = 0

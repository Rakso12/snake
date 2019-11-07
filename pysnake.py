import curses, random
from curses import KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN

#TODO make func out of rave or at least make use of it in powerup powerup

przegrana_text = 'Przegrałeś!'
wygrana_text = 'Wygrałeś!'

scr = curses.initscr()
curses.start_color()

# badamy wielkość terminala
wysokosc, szerokosc = scr.getmaxyx()

if wysokosc < 10 or szerokosc < len(przegrana_text) + 2:
    print('Zbyt mało miejsca, aby rozpocząć grę.')
    exit()

# wymiary planszy
# szerokosc
wysokosc -= 3
pole = (wysokosc - 2) * (szerokosc - 2)

win = curses.newwin(wysokosc, szerokosc, 0, 0)
stats = curses.newwin(3, szerokosc, wysokosc, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(curses.ACS_CKBOARD, curses.ACS_CKBOARD,
           curses.ACS_CKBOARD, curses.ACS_CKBOARD,
           curses.ACS_CKBOARD, curses.ACS_CKBOARD,
           curses.ACS_CKBOARD, curses.ACS_CKBOARD,)
stats.border(0)
win.nodelay(1)

# dobranie kolorów
COLORS = [curses.COLOR_BLUE, curses.COLOR_CYAN,
          curses.COLOR_GREEN, curses.COLOR_MAGENTA,
          curses.COLOR_RED, curses.COLOR_WHITE,
          curses.COLOR_YELLOW]
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)


# opcje startowe
key = KEY_RIGHT
snake = [[5, 5]]
x = 5
y = 5
jablko = [5, 6]
powerup = []
len_add = 0
wygrana = 0
score = 0
speed = 175
ordinary_speed = 175
rave_speed = 125
rave_range = 5
rave_time = 0
przegrana_text = 'Przegrałeś! :<'
wygrana_text = 'Wygrałeś! :>'

# opcje dodatkowe
rave = 0
diamond_blink = 0

# ustalanie koordynatów pierwszego jabłka
win.addch(jablko[0], jablko[1], curses.ACS_DIAMOND, curses.A_STANDOUT)

while key != 27:

    shallgen = random.randint(1, 100)
    #200

    # migające zdobycze
    if diamond_blink:
        col1 = random.randint(0, len(COLORS) - 1)
        curses.init_pair(1, COLORS[col1], curses.COLOR_BLACK)

    # ravesnake
    if rave:
        col1 = random.randint(0, len(COLORS) - 1)
        col2 = random.randint(0, len(COLORS) - 1)
        col3 = random.randint(0, len(COLORS) - 1)

        curses.init_pair(1, COLORS[col2], COLORS[col1])
        curses.init_pair(2, COLORS[col1], COLORS[col2])
        curses.init_pair(3, COLORS[col3], COLORS[col3])
        curses.init_pair(4, COLORS[col3], curses.COLOR_BLACK)

        speed = rave_speed

    # zbieramy przyciski
    prevKey = key
    event = win.getch()

    # definiujemy, co program ma robić w razie wciśnięcia przycisku
    # oslo rozwiązanie problemu cofania się węża
    if event == -1:
        key = key
    elif key == KEY_RIGHT and event == KEY_LEFT:
        key = key
    elif key == KEY_LEFT and event == KEY_RIGHT:
        key = key
    elif key == KEY_UP and event == KEY_DOWN:
        key = key
    elif key == KEY_DOWN and event == KEY_UP:
        key = key
    else:
        key = event

    if event not in (KEY_LEFT, KEY_DOWN, KEY_RIGHT, KEY_UP, -1, 27):
        key = prevKey

    # zmienianie koordynatów głowy węża
    if key == KEY_RIGHT:
        y += 1
    elif key == KEY_LEFT:
        y -= 1
    elif key == KEY_UP:
        x -= 1
    elif key == KEY_DOWN:
        x += 1


    # granice planszy
    if x == 0 or x == wysokosc - 1 or y == 0 or y == szerokosc - 1:
        wygrana = -1
        break

    # wchodzenie węża w samego siebie
    if [x, y] in snake:
        wygrana = -1
        break

    # debug
    #stats.clear()
    #stats.addstr(1, 1, str(powerup) + ' ' + str(rave_time) + ' ' + str(speed) + ' ' + str(shallgen) + ' ' + str(event))
    #stats.addstr(1, 1, str(snake))
    #stats.refresh()

    # generowanie powerupa
    if len(powerup) == 0 and shallgen > 99:
        while True:
            powerup.append(random.randint(1, wysokosc - 2))
            powerup.append(random.randint(1, szerokosc - 2))

            # TODO przepisać to wszystko bo ten kod to śmietink a do tego wolny
            if powerup in snake:
                powerup.pop()
                powerup.pop()
                continue

            if powerup not in snake and powerup not in jablko:
                break
        # rysowanie powerupa
        win.addch(powerup[0], powerup[1], curses.ACS_DEGREE, curses.color_pair(4))
        # stats.clear()

    # gdy snejk wejdzie w powerupa, który nie zdążył się jeszcze zepsuć xD( if len powerup == 2 )
    if len(powerup) == 2 and x == powerup[0] and y == powerup[1]:
        powerup.pop()
        powerup.pop()
        # stats.clear()
        rave = 1
        len_add = 1

    # jeżeli powerup jest aktywny, zwieksz czas
    if rave == 1:
        rave_time += 1

    # jezeli czas aktywnego powerupa równa się max zasięgowi czasu, zresetuj ustawienia
    if rave_time > rave_range:
        # restart ustawień zwykłych, poza rave
        rave_time = 0
        rave = 0
        len_add = 0

        score += 5
        stats.addstr(1, 1, 'Wynik:' + str(score))
        stats.refresh()

        speed = ordinary_speed
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # rysowanie węza na planszy,teraz z kolorkami xD
    win.addch(x, y, curses.ACS_BOARD, curses.color_pair(3),)
    if len(snake) > 1:
        win.addch(snake[0][0], snake[0][1], curses.ACS_BOARD, curses.color_pair(2),)

    # dodawanie kolejnego koordynatu (głowy węża) do listy wszystkich punktów
    # w których wąż się znajduje
    snake.insert(0, [x, y])

    # wynik/wydłużanie węża
    if x == jablko[0] and y == jablko[1]:
        score += 1
        stats.addstr(1, 1, 'Wynik:' + str(score))
        stats.refresh()
        # tworzenie nowych koordynatów jabłka
        while True:
            jablko[0] = random.randint(1, wysokosc - 2)
            jablko[1] = random.randint(1, szerokosc - 2)

            if jablko not in snake and jablko not in powerup:
                break

        # dodawanie jabłka
        win.addch(jablko[0], jablko[1], curses.ACS_DIAMOND, curses.color_pair(1))

    # jeżeli jabłko nie zostało zebrane, usuń ostatni koordynat węża z listy
    # (długość węża pozostaje taka sama)
    elif len_add == 0:
        win.addch(snake[-1][0], snake[-1][1], ' ')
        snake.pop()

    if score >= pole - 1:
        wygrana = 1
        break

    # opóźnienie, dwie opcje, z czego druga bardziej responsywna
    # curses.napms(speed)
    win.timeout(speed)

if wygrana == -1:
    win.addstr(int(wysokosc/2), int(szerokosc/2) - int(len(przegrana_text) / 2), przegrana_text)

if wygrana == 1:
    win.addstr(int(wysokosc/2), int(szerokosc/2) - int(len(wygrana_text) / 2), wygrana_text)

win.refresh()
while True:
    if win.getch() != -1:
        break

curses.nocbreak()
win.keypad(False)
curses.echo()
curses.endwin()

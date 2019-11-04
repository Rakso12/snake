import curses, random
from curses import KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN


scr = curses.initscr()
curses.start_color()

# badamy wielkość terminala
wysokosc, szerokosc = scr.getmaxyx()

if wysokosc < 10 or szerokosc < 8:
    print('Zbyt mało miejsca, aby rozpocząć grę.')
    exit()

# wymiary planszy
# szerokosc
wysokosc -= 3

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


# opcje startowe
key = KEY_RIGHT
snake = [[5, 5]]
x = 5
y = 5
jablko = [5, 6]
score = 0
time = 250

# opcje dodatkowe
rave = 0
diamond_blink = 1

# ustalanie koordynatów pierwszego jabłka
win.addch(jablko[0], jablko[1], curses.ACS_DIAMOND, curses.A_STANDOUT)

while key != 27:

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

        time = 150

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

    # basically zmienianie koordynatów głowy węża
    if key == KEY_RIGHT:
        y += 1
    if key == KEY_LEFT:
        y -= 1
    if key == KEY_UP:
        x -= 1
    if key == KEY_DOWN:
        x += 1

    # granice planszy
    if x == 0 or x == wysokosc - 1 or y == 0 or y == szerokosc - 1:
        break

    # wchodzenie węża w samego siebie
    if [x, y] in snake:
        break

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

            if jablko not in snake:
                break

        # dodawanie jabłka
        win.addch(jablko[0], jablko[1], curses.ACS_DIAMOND, curses.color_pair(1))

    # jeżeli jabłko nie zostało zebrane, usuń ostatni koordynat węża z listy
    # (długość węża pozostaje taka sama)
    else:
        win.addch(snake[-1][0], snake[-1][1], ' ')
        snake.pop()

    # opóźnienie, dwie opcje, z czego druga bardziej responsywna
    # curses.napms(time)
    win.timeout(time)

curses.nocbreak()
win.keypad(False)
curses.echo()
curses.endwin()

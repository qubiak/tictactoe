import pygame
import sys
import random
from pygame.locals import * 

pygame.init()

GAME_WINDOW = pygame.display.set_mode((150, 150), 0, 32)

pygame.display.set_caption('Tic Tac Toe')

# lista opisująca stan pola gry, 0 - pole puste, 1 - gracz, 2 - komputer
PLAYING_FIELD = [0, 0, 0,
            0, 0, 0,
            0, 0, 0]

MOVE = 1  # do kogo należy ruch: 1 – gracz, 2 – komputer
WINER = 0  # wynik gry: 0 - nikt, 1 - gracz, 2 - komputer, 3 - remis
WIN = False

# --------------------------- rysowanie planszy -----------------------------------

def draw_game_window():
    for i in range(0, 3):  # x
        for j in range(0, 3):  # y
            # argumenty: powierzchnia, kolor, x,y, w,h, grubość linii
            pygame.draw.rect(GAME_WINDOW, (255, 255, 255),
                             Rect((j * 50, i * 50), (50, 50)), 1)

# narysuj kółka

def draw_playing_game():
    for i in range(0, 3):
        for j in range(0, 3):
            field = i * 3 + j  # zmienna pole przyjmuje wartości od 0-8
            x = j * 50 + 25
            y = i * 50 + 25

            if PLAYING_FIELD[field] == 1:
                # rysuj kółko gracza
                pygame.draw.circle(GAME_WINDOW, (0, 0, 255), (x, y), 10)
            elif PLAYING_FIELD[field] == 2:
                # rysuj kółko komputera
                pygame.draw.circle(GAME_WINDOW, (255, 0, 0), (x, y), 10)

                # postaw kółko lub kółko inngo koloru


def put_a_sing(field, MOVE):
    if PLAYING_FIELD[field] == 0:
        if MOVE == 1:  # ruch gracza
            PLAYING_FIELD[field] = 1
            return 2
        elif MOVE == 2:  # ruch komputera
            PLAYING_FIELD[field] = 2
            return 1

    return MOVE

#Funkcja sprawdzająca czy komputer
# może wygrać
# musi blokować

def check_the_fields(uklad, winer=None):
    value = None
    # lista wielowymiarowa, której elementami są inne listy zagnieżdżone
    FIELDS_INDEX = [  # trójki pól planszy do sprawdzania
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # indeksy pól w poziomie (wiersze)
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # indeksy pól w pionie (kolumny)
        [0, 4, 8], [2, 4, 6]  # indeksy pól na skos (przekątne)
    ]

    for list in FIELDS_INDEX:
        li = []  # lista pomocnicza
        for ind in list:
            li.append(PLAYING_FIELD[ind])  # zapisz wartość odczytaną z PLAYING_FIELD
        if (li in uklad):  # jeżeli znalazłeś układ wygrywający lub blokujący
            # zwróć wygranego (1,2) lub indeks pola do zaznaczenia
            value = winer if winer else list[li.index(0)]

    return value

# ruchy komputera

def ai_move(MOVE):
    field = None  # które pole powinien zaznaczyć komputer

    # listy wielowymiarowe, których elementami są inne listy zagnieżdżone
    winning_hands = [[2, 2, 0], [2, 0, 2], [0, 2, 2]]
    locking_hands = [[1, 1, 0], [1, 0, 1], [0, 1, 1]]

    # sprawdź, czy komputer może wygrać
    field = check_the_fields(winning_hands)
    if field is not None:
        return put_a_sing(field, MOVE)

    # jeżeli komputer nie może wygrać, blokuj gracza
    field = check_the_fields(locking_hands)
    if field is not None:
        return put_a_sing(field, MOVE)

    # jeżeli nie można wygrać i gracza nie trzeba blokować, wylosuj pole
    while field is None:
        pos = random.randrange(0, 9)  # wylosuj wartość od 0 do 8
        if PLAYING_FIELD[pos] == 0:
            field = pos

    return put_a_sing(field, MOVE)

# sprawdzanie wyniku

def who_win():
    # układy wygrywające dla gracza i komputera
    player_layout = [[1, 1, 1]]
    computer_layout = [[2, 2, 2]]

    WINER = check_the_fields(player_layout, 1)  # czy wygrał gracz?
    if not WINER:  # jeżeli gracz nie wygrywa
        WINER = check_the_fields(computer_layout, 2)  # czy wygrał komputer?

    # sprawdź remis
    if 0 not in PLAYING_FIELD and WINER not in [1, 2]:
        WINER = 3

    return WINER
    
# rysowanie tesktu z wynikiem

def print_result(WINER):
    fontObj = pygame.font.Font('freesansbold.ttf', 16)
    if WINER == 1:
        text = u'BRAWO, Wygrałeś'
    elif WINER == 2:
        text = u'Niestey przegrana :( '
    elif WINER == 3:
        text = 'Remis!'
    text_ob = fontObj.render(text, True, (20, 255, 20))
    text_pr = text_ob.get_rect()
    text_pr.center = (75, 75)
    GAME_WINDOW.blit(text_ob, text_pr)


# pętla główna programu
while True:
    # obsługa zdarzeń generowanych przez gracza
    for event in pygame.event.get():
        # przechwyć zamknięcie okna
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if WIN is False:
            if MOVE == 1:
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:  # jeżeli naciśnięto 1. przycisk
                        mouseX, mouseY = event.pos  # rozpakowanie tupli
                        # wylicz indeks klikniętego pola
                        field = (int(mouseY / 50) * 3) + int(mouseX / 50)
                        MOVE = put_a_sing(field, MOVE)
            elif MOVE == 2:
                MOVE = ai_move(MOVE)

            WINER = who_win()
            if WINER is not None:
                WIN = True

    GAME_WINDOW.fill((0, 0, 0))  # definicja koloru powierzchni w RGB
    draw_game_window()
    draw_playing_game()
    if WIN:
        print_result(WIN)
    pygame.display.update()

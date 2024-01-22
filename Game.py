import cv2
import numpy as np
import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Ukuran layar Pygame
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Game Kartu Bridge')

#Music
music_file = ('konoha.mp3')
pygame.mixer.music.load(music_file)
pygame.mixer.music.play(-1)

# Warna
white = (255, 255, 255)
black = (0, 0, 0)

# Font
font = pygame.font.Font(None, 36)

# Kartu Remi
suits = ['H', 'D', 'S', 'C']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
cards = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]
#Cards_name

# List pemain
players = ['Komputer', 'Pemain']
player_hands = {player: [] for player in players}

# Kartu yang sudah dimainkan
played_cards = {'Komputer': [], 'Pemain': []}

# Fungsi untuk membagi kartu ke pemain
def deal_cards():
    #Open Camera
    #Model.predict(cards)
    #Append giliran, pertama ke player kedua ke CPU
    random.shuffle(cards)
    # for i in range(0, len(cards), len(players)):
    #     for j, player in enumerate(players):
    #         player_hands[player].append(cards[i + j])
    player_hands['Komputer'] = cards[:6]  # Memilih 3 kartu pertama untuk Komputer
    player_hands['Pemain'] = cards[6:12]


# Fungsi untuk menampilkan tangan pemain
def display_player_hand(player):
    hand = player_hands[player]
    for i, card in enumerate(hand):
        card_text = font.render(f"{card['rank']} {card['suit']}", True, black)
        screen.blit(card_text, (20 + i * 60, 20 if player == 'Komputer' else screen_height - 60))

# Fungsi untuk menampilkan kartu yang dimainkan
def display_played_cards():
    for player, cards in played_cards.items():
        for i, card in enumerate(cards):
            card_text = font.render(f"{card['rank']} {card['suit']}", True, black)
            screen.blit(card_text, (20 + i * 60, 150 if player == 'Komputer' else screen_height - 200))

# Fungsi untuk memilih kartu oleh pemain CPU
def select_card_cpu(current_card):
    if current_card is None:
        return random.choice(player_hands['Komputer'])

    playable_cards = [card for card in player_hands['Komputer'] if card['suit'] == current_card['suit']]

    #Jika tidak ada kartu yang sesuai maka CPU akan mengambil kartu dari cards
    if len(playable_cards) == 0:
        while len(playable_cards) == 0 and len(player_hands['Komputer']) > 0:
            player_hands['Komputer'].append(cards.pop(0))
            playable_cards = [card for card in player_hands['Komputer'] if card['suit'] == current_card['suit']]

    #jika ada kartu yang sesuai, keluarkan sesuai dengan index kartu
    if len(playable_cards) > 0:
        return playable_cards[0]
    else:
        return None  # Jika tidak ada kartu yang sesuai

# Fungsi untuk menentukan pemenang setiap putaran
def determine_winner():
    Komputer_card = played_cards['Komputer'][-1]
    Pemain_card = played_cards['Pemain'][-1]

    if Komputer_card['suit'] == Pemain_card['suit']:
        Komputer_rank_index = ranks.index(Komputer_card['rank'])
        Pemain_rank_index = ranks.index(Pemain_card['rank'])

        if Komputer_rank_index > Pemain_rank_index:
            return 'Komputer'
        elif Pemain_rank_index > Komputer_rank_index:
            return 'Pemain'
    else:
        return 'Komputer'  # Jika suit-nya berbeda, pemain Komputer yang menang


# Fungsi untuk memulai permainan
def start_game():
    deal_cards()
    currentPlayer = random.choice(players)  # Pemain yang akan memulai pertama kali
    winner = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and currentPlayer == 'Pemain':
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, card in enumerate(player_hands['Pemain']):
                    if 20 + i * 60 < mouse_x < 80 + i * 60 and screen_height - 60 < mouse_y < screen_height - 20:
                        #Jika player tidak mempunyai kartu, minum dari cards
                        selected_card = player_hands['Pemain'].pop(i)
                        print(f"Pemain plays: {selected_card['rank']} {selected_card['suit']}")
                        played_cards['Pemain'].append(selected_card)
                        currentPlayer = 'Komputer'  # Ganti giliran ke pemain Komputer

        if currentPlayer == 'Komputer':
            current_card = played_cards['Pemain'][-1] if len(played_cards['Pemain']) > 0 else None
            selected_card = select_card_cpu(current_card)
            try:
                player_hands['Komputer'].remove(selected_card)
                print(f"Komputer plays: {selected_card['rank']} {selected_card['suit']}")
                played_cards['Komputer'].append(selected_card)
                currentPlayer = 'Pemain'  # Ganti giliran ke pemain Pemain
            except ValueError:
                pass  # Jika selected_card tidak ada dalam tangan Komputer, lakukan langkah berikutnya

    #Error disini
        #jika played_cards['Pemain'][-1] and played_cards['Komputer'][-1] and winner is None:
        if len(player_hands['Komputer']) == 0 and len(player_hands['Pemain']) == 0 and winner is None:
            winner = determine_winner()
            # if winner != 'Tie':
            print(f"{winner} wins!")
            currentPlayer = winner  # Pemenang mendapat giliran tambahan

            # Pemenang mengeluarkan satu kartu lagi jika masih punya kartu
            if len(player_hands[winner]) > 0:
                played_cards[winner].append(player_hands[winner].pop(0))  # Mengeluarkan satu kartu
                print(f"{winner} plays: {played_cards[winner][-1]['rank']} {played_cards[winner][-1]['suit']}")

            # else:
            #     currentPlayer = 'Pemain'  # Jika terjadi tie, giliran kembali ke pemain Pemain

        # if currentPlayer == 'Pemain':
        #     current_card = played_cards['Komputer'][-1] if len(played_cards['Komputer']) > 0 else None
        #     selected_card = select_card_cpu(current_card)
        #     try:
        #         player_hands['Pemain'].remove(selected_card)
        #         print(f"Pemain plays: {selected_card['rank']} {selected_card['suit']}")
        #         played_cards['Pemain'].append(selected_card)
        #         currentPlayer = 'Komputer'  # Ganti giliran ke pemain Komputer
        #     except ValueError:
        #         pass  # Jika selected_card tidak ada dalam tangan Pemain, lakukan langkah berikutnya

        screen.fill(white)
        display_player_hand('Komputer')
        display_player_hand('Pemain')
        display_played_cards()
        pygame.display.update()

    pygame.mixer.music.stop()
    pygame.quit()

camera_index = 0
cap = cv2.VideoCapture(camera_index)
if not cap.isOpened():
    print("Tidak dapat membuka kamera")
    exit()

start_game()

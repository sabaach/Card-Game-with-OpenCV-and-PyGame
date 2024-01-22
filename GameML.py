import cv2
import numpy as np
import pygame
import random
from keras.models import load_model

model = load_model('trained_model.h5')

# Inisialisasi Pygame
pygame.init()

# Ukuran layar Pygame
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Game Kartu Bridge')

# Warna
white = (255, 255, 255)
black = (0, 0, 0)

# Font
font = pygame.font.Font(None, 36)

# List pemain
players = ['Komputer', 'Pemain']
player_hands = {player: [] for player in players}

# Kartu yang sudah dimainkan
played_cards = {'Komputer': [], 'Pemain': []}
ranks = ['Dua', 'Tiga', 'Empat', 'Lima', 'Enam', 'Tujuh', 'Delapan', 'Sembilan', 'Sepuluh', 'Jack', 'Queen', 'King', 'Ace']

def detect_cards(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    predicted_card_name = None

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 5000:  # Menentukan ambang batas area untuk deteksi kartu
            x, y, w, h = cv2.boundingRect(contour)
            card = image[y:y + h, x:x + w]
            card = cv2.resize(card, (128, 128))  # Pra-pemrosesan gambar
            #card = cv2.cvtColor(card, cv2.COLOR_BGR2GRAY)  # Konversi ke grayscale
            card = np.expand_dims(card, axis=-1)  # Menambahkan dimensi channel
            card = card / 255.0  # Normalisasi
            card = np.expand_dims(card, axis=0)  # Menambahkan dimensi batch
            prediction = model.predict(card)
            predicted_class = np.argmax(prediction)
            card_names = ['Hati Ace', 'Hati Dua', 'Hati Tiga', 'Hati Empat', 'Hati Lima', 'Hati Enam', 'Hati Tujuh', 'Hati Delapan', 'Hati Sembilan',
                          'Hati Sepuluh', 'Hati Jack', 'Hati Queen', 'Hati King',
                          'Keriting Ace','Keriting Dua', 'Keriting Tiga', 'Keriting Empat', 'Keriting Lima', 'Keriting Enam', 'Keriting Tujuh',
                          'Keriting Delapan', 'Keriting Sembilan', 'Keriting Sepuluh', 'Keriting Jack', 'Keriting Queen', 'Keriting King',
                          'Sekop Ace', 'Sekop Dua', 'Sekop Tiga', 'Sekop Empat', 'Sekop Lima', 'Sekop Enam', 'Sekop Tujuh', 'Sekop Delapan',
                          'Sekop Sembilan', 'Sekop Sepuluh', 'Sekop Jack', 'Sekop Queen', 'Sekop King',
                          'Wajik Ace', 'Wajik Dua', 'Wajik Tiga', 'Wajik Empat', 'Wajik Lima', 'Wajik Enam', 'Wajik Tujuh', 'Wajik Delapan',
                          'Wajik Sembilan', 'Wajik Sepuluh', 'Wajik Jack', 'Wajik Queen', 'Wajik King']
            predicted_card_name = card_names[predicted_class]
            accuracy = np.max(prediction) * 100
            cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
            cv2.putText(image, f'{predicted_card_name} ({accuracy:.2f}%)', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

    return image, predicted_card_name


# LoadModelCNN dan Lakukan Predict
# Fungsi untuk mendeteksi kartu dari kamera dan mengembalikan teks kartu sebagai font Pygame
def detect_and_add_card(player):
    global cards

    cap = cv2.VideoCapture(1)

    while True:
        ret, frame = cap.read()  # Membaca frame dari kamera
        resized_frame = cv2.resize(frame, (640, 640))
        # Lakukan deteksi kartu menggunakan model CNN pengguna di sini
        # Misalnya, panggil fungsi deteksi kartu dan dapatkan hasilnya

        # Simpan hasil deteksi kartu, misalnya jenis dan nilai kartu
        # Contoh sementara menggunakan deteksi acak (ganti dengan hasil deteksi sebenarnya)
        processed_frame, name = detect_cards(resized_frame)
        print("hasil detek",name)
        cv2.imshow("kartu kedetek", processed_frame)

        # Ubah hasil deteksi kartu ke format teks yang akan ditampilkan pada layar
        card_text = f"{name}"

        key = cv2.waitKey(1)

        # Tambahkan kartu yang terdeteksi ke tangan pemain yang sesuai
        # jika kartu yang dideteksi merupakan kartu misal keriting ace, keriting dua,... maka suit keriting
        if name not in player_hands[player]:
            if key == ord('q'):
                player_hands[player].append(name)
                print("kartu player",player_hands[player])
                # Array awal
                array_awal = player_hands[player]
                # Mengambil 'keriting' dari setiap elemen dalam array
                suits = [kata.split()[0] for kata in array_awal]
                ranks = [kata.split()[1] for kata in array_awal]

                cards = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]

                print(cards)
                
                return name, cards  # Kembalikan teks kartu untuk ditampilkan pada layar
        if key == ord('x'):
            break
        # cv2.waitKey(0)

    cap.release()  # Bebaskan sumber daya kamera setelah selesai
    cv2.destroyAllWindows()

def display_player_hand(player,font,screen,black):
    # cardtext, _ = detect_and_add_card(player)
    hand = player_hands[player]
    for i, card in enumerate(hand):
        # Tampilkan font kartu yang dihasilkan dari fungsi detect_and_add_card
        card_text = font.render(card, True, black)
        screen.blit(card_text, (20 + i * 130, 20 if player == 'Komputer' else screen_height - 60))

#Perbaiki!!!
#Sudah bisa
def display_played_cards(screen,font,black,cards):
    if cards:
        for player, player_cards in played_cards.items():
            for i, card in enumerate(player_cards):
                card_text = font.render(card, True, black)
                screen.blit(card_text, (20 + i * 130, 150 if player == 'Komputer' else screen_height - 200))
    else:
        print("No cards detected!")

#Perbaiki!!!
#Current Card belom diperbaiki sehingga CPU akan mengeluarkan kartu random tidak sesuai jenis kartu yang dimainkan
# Fungsi untuk memilih kartu oleh pemain CPU
def select_card_cpu(current_card):
    if current_card is None:
         return random.choice(player_hands['Komputer'])

    playable_cards = [card for card in player_hands['Komputer'] if card not in played_cards['Komputer']]
    current_card_suit = current_card.split()[0] if current_card else None

    if len(playable_cards) > 0:
        for card in playable_cards:
            card_suit = card.split()[0]
            if card_suit == current_card_suit:
                return card

    return None

#Perbaiki!!!
# Fungsi untuk menentukan pemenang setiap putaran
def determine_winner():
    if len(played_cards['Pemain']) == 0 or len(played_cards['Komputer']) == 0:
        return None

    Komputer_card = played_cards['Komputer'][-1]
    Pemain_card = played_cards['Pemain'][-1]

    Komputer_card_suit, Komputer_card_rank = Komputer_card.split()
    Pemain_card_suit, Pemain_card_rank = Pemain_card.split()

    if Komputer_card_suit == Pemain_card_suit:
        Komputer_rank_index = ranks.index(Komputer_card_rank)
        Pemain_rank_index = ranks.index(Pemain_card_rank)

        if Komputer_rank_index > Pemain_rank_index:
            return 'Komputer'
        elif Pemain_rank_index > Komputer_rank_index:
            return 'Pemain'
    else:
        return 'Komputer'

def display_game_screen():
    # Music
    music_file = ('konoha.mp3')
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(-1)

    winner = None
    #Ketika current player awal komputer algoritma game masih salah
    # currentPlayer = random.choice(players)  # Pemain yang akan memulai pertama kali
    currentPlayer = 'Pemain'

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and currentPlayer == 'Pemain':
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, card in enumerate(player_hands['Pemain']):
                    if 20 + i * 60 < mouse_x < 80 + i * 60 and screen_height - 60 < mouse_y < screen_height - 20:
                        selected_card = player_hands['Pemain'].pop(i)
                        # print(f"Pemain plays: {selected_card['rank']} {selected_card['suit']}")
                        print(f"Pemain plays: {selected_card}")
                        played_cards['Pemain'].append(selected_card)
                        currentPlayer = 'Komputer'  # Ganti giliran ke pemain Komputer

        if currentPlayer == 'Komputer':
            current_card = played_cards['Pemain'][-1] if len(played_cards['Pemain']) > 0 else None
            selected_card = select_card_cpu(current_card)
            try:
                player_hands['Komputer'].remove(selected_card)
                print(f"Komputer plays: {selected_card}")
                played_cards['Komputer'].append(selected_card)
                currentPlayer = 'Pemain'  # Ganti giliran ke pemain Pemain
            except ValueError:
                pass  # Jika selected_card tidak ada dalam tangan Komputer, lakukan langkah berikutnya

        # Error disini
        if len(played_cards['Pemain']) > 0 and len(played_cards['Komputer']) > 0:
            winner = determine_winner()
                # if winner != 'Tie':
            print(f"{winner} wins!")
            currentPlayer = winner  # Pemenang mendapat giliran tambahan

            # if winner == 'Komputer':
            #     # Pemenang mengeluarkan satu kartu lagi jika masih punya kartu
            #     if len(player_hands[winner]) > 0:
            #         played_cards[winner].append(player_hands[winner].pop(0))  # Mengeluarkan satu kartu
            #         print(f"{winner} plays: {played_cards[winner][-1]}")
            #     currentPlayer = 'Pemain'
            # elif winner == 'Pemain':
            #     currentPlayer = 'Pemain'

        if len(player_hands['Komputer']) == 0 and winner == 'Komputer':
            print("Komputer Win the game")
            break
        elif len(player_hands['Pemain']) == 0 and winner == 'Pemain':
            print("Pemain Win the game")
            break
                # else:
                #     currentPlayer = 'Pemain'  # Jika terjadi tie, giliran kembali ke pemain Pemain

        screen.fill(white)
        display_player_hand('Komputer',font, screen, black)
        display_player_hand('Pemain',font, screen, black)
        display_played_cards(screen, font, black, cards)
        pygame.display.update()

    pygame.mixer.music.stop()
    pygame.quit()


# Fungsi untuk membagi kartu ke pemain
def deal_cards():
    #Open Camera
    #Model.predict(cards)
    #Append giliran, pertama ke player kedua ke CPU
    global players

    player_hand_limit = 3  # Batas jumlah kartu untuk setiap pemain
    while len(player_hands['Pemain']) < player_hand_limit or len(player_hands['Komputer']) < player_hand_limit:
        # Jika jumlah kartu pemain belum mencapai batas, lanjutkan giliran pemain
        if len(player_hands['Pemain']) < player_hand_limit:
            print("Giliran Pemain untuk mendeteksi kartu.")
            detect_and_add_card('Pemain')

        # Jika jumlah kartu pemain telah mencapai batas, lanjutkan giliran CPU
        if len(player_hands['Pemain']) == player_hand_limit and len(player_hands['Komputer']) < player_hand_limit:
            print("Giliran Komputer untuk mendeteksi kartu.")
            detect_and_add_card('Komputer')

    # Setelah selesai, mulai permainan
    print("Permainan dimulai...")
    display_game_screen()

# Fungsi untuk memulai permainan
def start_game():
    deal_cards()

start_game()

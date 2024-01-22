import cv2
import numpy as np
import copy
from keras.models import load_model

model = load_model('trained_model.h5')

#Fungsi untuk mendeteksi kartu pada gambar
def detect_cards(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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

    return image

cap = cv2.VideoCapture("test4.mp4")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    resized_frame = cv2.resize(frame, (640, 640))
    processed_frame = detect_cards(resized_frame)

    cv2.imshow('Deteksi Kartu', processed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

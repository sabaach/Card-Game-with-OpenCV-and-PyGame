import cv2
import os
import datetime
import time
import numpy as np

cardName = [ "Keriting Dua", "Keriting Tiga", "Keriting Empat", "Keriting Lima", "Keriting Enam", "Keriting Tujuh", "Keriting Delapan", "Keriting Sembilan",
             "Keriting Sepuluh", "Keriting Jack", "Keriting Queen", "Keriting King", "Keriting Ace",
             "Hati Dua", "Hati Tiga", "Hati Empat", "Hati Lima", "Hati Enam", "Hati Tujuh", "Hati Delapan", "Hati Sembilan", "Hati Sepuluh",
             "Hati Jack", "Hati Queen", "Hati King", "Hati Ace",
             "Wajik Dua", "Wajik Tiga", "Wajik Empat", "Wajik Lima", "Wajik Enam", "Wajik Tujuh", "Wajik Delapan", "Wajik Sembilan", "Wajik Sepuluh",
             "Wajik Jack", "Wajik Queen", "Wajik King", "Wajik Ace",
             "Sekop Dua", "Sekop Tiga","Sekop Empat", "Sekop Lima", "Sekop Enam", "Sekop Tujuh", "Sekop Delapan", "Sekop Sembilan", "Sekop Sepuluh",
             "Sekop Jack", "Sekop Queen", "Sekop King", "Sekop Ace", ]

cardNameIndex = 0

#penamaan file menurut waktu diambil
def GetFileName():
    x = datetime.datetime.now()
    s = x.strftime('%Y-%m-%d-%H%M%S%f')
    return s

# Fungsi menentukan luas area dari 4 titik
def polygon_area(points):
    # 'points' adalah input berupa array yg berisikan 4 titik koordinat kartu
    points = np.vstack((points, points[0]))
    area = 0.5 * np.abs(np.dot(points[:, 0], np.roll(points[:, 1], 1)) - np.dot(points[:, 1], np.roll(points[:, 0], 1)))
    return area

def CreateDir(path):
    ls = []
    head_tail = os.path.split(path)
    ls.append(path)
    while len(head_tail[1]) > 0:
        head_tail = os.path.split(path)
        path = head_tail[0]
        ls.append(path)
        head_tail = os.path.split(path)
    for i in range(len(ls) - 2, -1, -1):
        sf = ls[i]
        isExist = os.path.exists(sf)
        if not isExist:
            os.makedirs(sf)

def CreateDataSet(sDirektoriData, sKelas, NoKamera, FrameRate):
    global cardName, cardNameIndex

    cap = cv2.VideoCapture(NoKamera)
    TimeStart = time.time()

    saveTimeLimit = time.time()

    isSaving = False

    while cap.isOpened():
        success, frame = cap.read()

        sDirektoriKelas = sDirektoriData + "/" + cardName[cardNameIndex]
        CreateDir(sDirektoriKelas)

        if not success:
            print("Ignoring empty camera frame.")
            continue

        isDetected = False

        imGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        imThres = cv2.adaptiveThreshold(imGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 71, 10)
        totalLabels, label_ids, values, centroid = cv2.connectedComponentsWithStats(imThres, 4, cv2.CV_32S)

        bigIndex = []
        for i in range(totalLabels):
            hw = values[i, 2:4]
            if (100 < hw[0] < 300 and 300 < hw[1] < 500):
                bigIndex.append(i)

        for i in bigIndex:
            topLeft = values[i, 0:2]
            bottomRight = values[i, 0:2] + values[i, 2:4]
            frame = cv2.rectangle(frame, topLeft, bottomRight, color=(0, 0, 255), thickness=3)

            break

        cv2.imshow("4. Hasil habis dikotakin", frame)

        for i in bigIndex:
            topLeft = values[i, 0:2]
            bottomRight = values[i, 0:2] + values[i, 2:4]

            cardImage = imThres[topLeft[1]:bottomRight[1], topLeft[0]:bottomRight[0]]

            cv2.imshow('5. Hasil dari cardImage', cardImage)

            break

        TimeNow = time.time()
        if TimeNow - TimeStart > 1 / FrameRate:
            sfFile = sDirektoriKelas + "/" + GetFileName()

            if isSaving and len(bigIndex) > 0:
                cv2.imwrite(sfFile + '.jpg', cardImage)
            TimeStart = TimeNow

        cv2.putText(frame, "Nama Kartu yg direkam:", (0, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        cv2.putText(frame, f"{cardNameIndex + 1}. " + cardName[cardNameIndex], (0, 160), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 0, 255), 2)
        cv2.putText(frame, "Tekan spasi untuk mulai record", (0, 220), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

        # Buat visualisasi record
        if isSaving:
            cv2.putText(frame, "Record", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            saveTimeLimit = time.time()

        cv2.imshow("Tampilan akhir", frame)

        key = cv2.waitKey(5)

        #Tekan spasi untuk mulai menyimpan gambar
        if key == 32:
            isSaving = not isSaving

        # Jika lebih dari 5 detik, penyimpanan foto selesai
        if time.time() - saveTimeLimit >= 5:
            cardNameIndex += 1
            isSaving = False

        if key & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

DirektoriDataSet = "CardDataSet"
CreateDataSet(DirektoriDataSet, " ", NoKamera=0, FrameRate=20)

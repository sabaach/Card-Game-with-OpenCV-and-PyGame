import cv2
import numpy as np
import os

dataset_path = 'CardDataSet'

images = []
labels = []

# Fungsi untuk membaca gambar dari direktori dan memberi label
def load_images_from_folder(folder, label):
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            img = cv2.resize(img, (640, 640))
            # _, thresholded_img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
            # thresholded_img = cv2.resize(thresholded_img, (640, 640))
            # hsvimg = cv2.cvtColor(thresholded_img, cv2.COLOR_BGR2HSV)
            # green_lower = np.array([25, 52, 72], np.uint8)
            # green_upper = np.array([102, 255, 255], np.uint8)
            # green_mask = cv2.inRange(hsvimg, green_lower, green_upper)
            #
            # kernal = np.ones((5, 5), "uint8")
            # green_mask = cv2.dilate(green_mask, kernal)
            # res_green = cv2.bitwise_and(thresholded_img, thresholded_img,
            #                              mask=green_mask)
            # f = thresholded_img - res_green
            # imGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # imThres = cv2.adaptiveThreshold(imGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 71, 10)
            #
            # totalLabels, label_ids, values, centroid = cv2.connectedComponentsWithStats(imThres, 4, cv2.CV_32S)
            # bigIndex = []
            # for i in range(totalLabels):
            #     hw = values[i, 2:4]
            #     if (100 < hw[0] < 300 and 300 < hw[1] < 500):
            #         bigIndex.append(i)
            #
            # for i in bigIndex:
            #     topLeft = values[i, 0:2]
            #     bottomRight = values[i, 0:2] + values[i, 2:4]
            #
            #     cardImage = imThres[topLeft[1]:bottomRight[1], topLeft[0]:bottomRight[0]]
            #     images.append(cardImage)
            # break
            images.append(img)
            labels.append(label)

# Load gambar dari setiap kategori kartu dan beri label
#Hati
load_images_from_folder('CardDataSet/Hati Ace', label=0)
load_images_from_folder('CardDataSet/Hati Dua', label=1)
load_images_from_folder('CardDataSet/Hati Tiga', label=2)
load_images_from_folder('CardDataSet/Hati Empat', label=3)
load_images_from_folder('CardDataSet/Hati Lima', label=4)
load_images_from_folder('CardDataSet/Hati Enam', label=5)
load_images_from_folder('CardDataSet/Hati Tujuh', label=6)
load_images_from_folder('CardDataSet/Hati Delapan', label=7)
load_images_from_folder('CardDataSet/Hati Sembilan', label=8)
load_images_from_folder('CardDataSet/Hati Sepuluh', label=9)
load_images_from_folder('CardDataSet/Hati Jack', label=10)
load_images_from_folder('CardDataSet/Hati Queen', label=11)
load_images_from_folder('CardDataSet/Hati King', label=12)
#Keriting
load_images_from_folder('CardDataSet/Keriting Ace', label=13)
load_images_from_folder('CardDataSet/Keriting Dua', label=14)
load_images_from_folder('CardDataSet/Keriting Tiga', label=15)
load_images_from_folder('CardDataSet/Keriting Empat', label=16)
load_images_from_folder('CardDataSet/Keriting Lima', label=17)
load_images_from_folder('CardDataSet/Keriting Enam', label=18)
load_images_from_folder('CardDataSet/Keriting Tujuh', label=19)
load_images_from_folder('CardDataSet/Keriting Delapan', label=20)
load_images_from_folder('CardDataSet/Keriting Sembilan', label=21)
load_images_from_folder('CardDataSet/Keriting Sepuluh', label=22)
load_images_from_folder('CardDataSet/Keriting Jack', label=23)
load_images_from_folder('CardDataSet/Keriting Queen', label=24)
load_images_from_folder('CardDataSet/Keriting King', label=25)
#Sekop
load_images_from_folder('CardDataSet/Sekop Ace', label=26)
load_images_from_folder('CardDataSet/Sekop Dua', label=27)
load_images_from_folder('CardDataSet/Sekop Tiga', label=28)
load_images_from_folder('CardDataSet/Sekop Empat', label=29)
load_images_from_folder('CardDataSet/Sekop Lima', label=30)
load_images_from_folder('CardDataSet/Sekop Enam', label=31)
load_images_from_folder('CardDataSet/Sekop Tujuh', label=32)
load_images_from_folder('CardDataSet/Sekop Delapan', label=33)
load_images_from_folder('CardDataSet/Sekop Sembilan', label=34)
load_images_from_folder('CardDataSet/Sekop Sepuluh', label=35)
load_images_from_folder('CardDataSet/Sekop Jack', label=36)
load_images_from_folder('CardDataSet/Sekop Queen', label=37)
load_images_from_folder('CardDataSet/Sekop King', label=38)
#Wajik
load_images_from_folder('CardDataSet/Wajik Ace', label=39)
load_images_from_folder('CardDataSet/Wajik Dua', label=40)
load_images_from_folder('CardDataSet/Wajik Tiga', label=41)
load_images_from_folder('CardDataSet/Wajik Empat', label=42)
load_images_from_folder('CardDataSet/Wajik Lima', label=43)
load_images_from_folder('CardDataSet/Wajik Enam', label=44)
load_images_from_folder('CardDataSet/Wajik Tujuh', label=45)
load_images_from_folder('CardDataSet/Wajik Delapan', label=46)
load_images_from_folder('CardDataSet/Wajik Sembilan', label=47)
load_images_from_folder('CardDataSet/Wajik Sepuluh', label=48)
load_images_from_folder('CardDataSet/Wajik Jack', label=49)
load_images_from_folder('CardDataSet/Wajik Queen', label=50)
load_images_from_folder('CardDataSet/Wajik King', label=51)

# Ubah list menjadi numpy array
images = np.array(images)
labels = np.array(labels)

np.save('images.npy', images)
np.save('labels.npy', labels)

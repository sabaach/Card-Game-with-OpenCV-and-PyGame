import random
import cv2
import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.regularizers import l2
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# Pra-pemrosesan Data
images = np.load('images.npy')
labels = np.load('labels.npy')

images = images / 255.0  # Normalisasi
width, height = 128, 128
resized_images = np.array([cv2.resize(image, (width, height)) for image in images])

# label dalam format one-hot encoding
num_classes = 52  # Jumlah kelas kartu dalam set kartu remi
labels_one_hot = to_categorical(labels, num_classes=num_classes)

# Membagi data menjadi data latih dan data validasi
#X_train, X_val, y_train, y_val = train_test_split(resized_images,
# #labels_one_hot, test_size=0.4, random_state=42)

# random.shuffle(X_train)
# random.shuffle(y_train)

# # Menambahkan dimensi channel pada input
# X_train = np.expand_dims(X_train, axis=-1)
# X_val = np.expand_dims(X_val, axis=-1)

# Membuat dan Melatih Model
model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=(width, height, 3), activation='relu'))  # Perubahan di sini
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(Flatten())
model.add(Dense(units=100, activation='relu', kernel_regularizer=l2(0.01)))
model.add(Dropout(0.5))
model.add(Dense(units=num_classes, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(resized_images, labels_one_hot, epochs=30, batch_size=32, shuffle=True) #validation_data=(X_val, y_val)

# Evaluation
# loss, accuracy = model.evaluate(X_val, y_val)
# print(f'Validation accuracy: {accuracy}')

model.save('trained_model.h5')

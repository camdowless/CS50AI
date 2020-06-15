import os
from os import listdir
import cv2

NUM_CATEGORIES = 43
data_dir = "gtsrb"
EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4

for i in range(0, NUM_CATEGORIES):
    path = os.path.join(data_dir, str(i))
    images = listdir(path)
    count = 0
    for p in images:
        im = cv2.imread(os.path.join(path, p))
        resized = cv2.resize(im, (IMG_HEIGHT, IMG_WIDTH))
        print(resized.shape)


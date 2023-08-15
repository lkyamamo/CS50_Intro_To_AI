import cv2
import numpy as np
import os
import sys


EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4

data_dir = 'gtsrb'

current_source_path = os.getcwd()

image_path = os.path.join(current_source_path, data_dir, '0/00000_00005.ppm')

#original image
image = cv2.imread(image_path)
print(image.shape)

cv2.imshow('image', image)

cv2.waitKey(0)




#first convolution
edge_detection_kernel = np.array([[-1,-1,-1],
                                      [-1,8,-1],
                                      [-1,-1,-1]])
    
image = cv2.filter2D(src=image, ddepth=-1, kernel=edge_detection_kernel)
print(image.shape)

cv2.imshow('image', image)

cv2.waitKey(0)

#second convolution
edge_detection_kernel = np.array([[1/16,2/16,1/16],
                                  [2/16,4/16,2/16],
                                  [1/16,2/16,1/16]])
    
image = cv2.filter2D(src=image, ddepth=-1, kernel=edge_detection_kernel)
print(image.shape)

cv2.imshow('image', image)

cv2.waitKey(0)


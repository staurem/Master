"This code runs HOG - Histogram of Orientades Graphics"
"https://www.thepythoncode.com/article/hog-feature-extraction-in-python"



#pip3 install scikit-image matplotlib


"Importing required libraries (for HOG)"
from skimage.io import imread
from skimage.transform import resize
from skimage.feature import hog
#from skimage import exposure
import matplotlib.pyplot as plt
import numpy as np
#import argparse #command lines arguments
import cv2 #openCV  #kommando, hvis feilmelding::: pip install opencv-python

"reading the image"
img = imread('nordlys3.jpg')
plt.axis('off')
plt.imshow(img)
#print('shape of original image:', img.shape)
#plt.show()


"Resizing the image"
resized_img = resize(img, (128*5, 64*5)) #the number you multiply, resizes the shape and HOG detail
plt.axis('off')
plt.imshow(resized_img)
#print('shape of resized image:',resized_img.shape)
#plt.show()


"Creating HOG features"
fd, hog_img = hog(resized_img, orientations=9, pixels_per_cell=(6,6), \
                    cells_per_block=(2,2), visualize=True, multichannel=True)
plt.axis('off')
plt.imshow(hog_img, cmap='gray')
plt.show()



"Using openCV to calculate x and y gradients"
img1 = cv2.imread('nordlys3.jpg')
kernel_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
kernel_x = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
edges_x = cv2.filter2D(img1, cv2.CV_8U, kernel_x)
edges_y = cv2.filter2D(img1, cv2.CV_8U, kernel_y) 

print(edges_x, edges_y)

cv2.imshow('Gradients_X',edges_x)
cv2.imshow('Gradients_Y',edges_y)
cv2.waitKey(0)

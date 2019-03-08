import numpy as np
import cv2
from matplotlib import pyplot as plt
img = cv2.imread('noisyImagePractice.jpg')
dst = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)
plt.imshow(img)
plt.imshow(dst)
plt.show()

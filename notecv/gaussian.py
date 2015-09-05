import cv2
import numpy as np

def gaussian(img):
    return cv2.GaussianBlur(img, (51,51), 50)

if __name__ == '__main__':
    import imstream
    imstream.runStream(gaussian)


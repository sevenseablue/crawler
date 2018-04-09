# coding: utf8
from __future__ import print_function

"""
---------------------------------------------
    File Name: imageUtils
    Description: 
    Author: wangdawei
    date:   2018/4/8
---------------------------------------------
    Change Activity: 
                    2018/4/8
---------------------------------------------    
"""

from PIL import Image
import cv2
import numpy as np
from matplotlib import pyplot as plt

from scipy import ndimage as ndi

from skimage import feature

file = "E:/github/crawler/data/shumei/5da2dfb1b0603ef7718ff3c54f5bba2e_bg.jpg"


def findjing(file):
    im = Image.open(file)

    print(im.format, im.size, im.mode)


def edge_1():
    img = cv2.imread(file, 0)
    # img = ndi.gaussian_filter(img, 3)
    # img = img # * 1.0
    # img += 0.2 * np.random.random(img.shape)
    #
    # # Compute the Canny filter for two values of sigma
    # edges = feature.canny(img)
    # edges = feature.canny(img, low_threshold=20, high_threshold=50)
    # # edges = feature.canny(img, sigma=5)
    #
    # plt.subplot(121), plt.imshow(img, cmap='gray')
    # plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122), plt.imshow(edges, cmap='gray')
    # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    # plt.show()

    for minv, maxv in [(20, 100), (50, 100), (50, 200), (100, 100), (100, 200)]:
        for apertureSize in (3, 5, 7):
            print(minv, maxv)
            edges = cv2.Canny(img, threshold1=minv, threshold2=maxv, apertureSize=apertureSize)

            plt.subplot(121), plt.imshow(img, cmap='gray')
            plt.title('Original Image'), plt.xticks([]), plt.yticks([])
            plt.subplot(122), plt.imshow(edges, cmap='gray')
            plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

            plt.show()

B = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=np.float32)
B = np.zeros((60, 60))
B[[0,59], 0:20] = 1
B[[0,59], 40:60] = 1
B[0:20, [0,59]] = 1
B[40:60, [0,59]] = 1
B[B!=1]=-1
B[0:11,20:40]=1
B[0:6, 24:36]=0
B[50:60,20:40]=1
B[54:60, 24:36]=0

from scipy import signal
import os
dir1 = "E:\github\crawler\data\shumei"
def edge_2():

    for f in os.listdir(dir1):
        print(f)
        if f.find("bg") < 0:
            continue
        img = cv2.imread(dir1+"/"+f, 0)

        edges1 = cv2.Canny(img, threshold1=137, threshold2=173)
        # edges = cv2.Canny(edges, threshold1=83, threshold2=131)
        # print(np.max(edges), np.min(edges))

        edges = signal.convolve2d(edges1, B, mode='same')
        print(edges.shape)
        # edges = cv2.filter2D(edges, -1, B)

        maxv = np.max(edges)
        print(np.where(edges == maxv))
        # plt.subplot(121), plt.imshow(img, cmap='gray')
        # plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        # plt.subplot(122), plt.imshow(edges1, cmap='gray')
        # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

        # plt.show()
    pass

def edge_center(file):
    img = cv2.imread(file, 0)

    edges1 = cv2.Canny(img, threshold1=137, threshold2=173)
    # edges = cv2.Canny(edges, threshold1=83, threshold2=131)
    # print(np.max(edges), np.min(edges))

    edges = signal.convolve2d(edges1, B, mode='same')
    # edges = cv2.filter2D(edges, -1, B)

    maxv = np.max(edges)
    return np.where(edges == maxv)

# findjing()
# edge_1()
# edge_2()
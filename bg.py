# -*- coding: utf-8 -*-
# @Author: lenovouser
# @Date:   2020-10-21 15:45:04
# @Last Modified by:   lenovouser
# @Last Modified time: 2020-10-21 15:45:09
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import math


def gamma(img, g=1.0):
    ig = g
    table = []
    for i in range(256):
        table.append(((i / 255)**ig) * 255)
    table = np.array([table]).astype("uint8")
    return cv.LUT(img, table)


import glob

for fn in glob.glob("res/*"):
    print(fn)
    # image = cv.imread(fn, 1)
    img = cv.imread(fn, 0)

    # image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    # h, s, img = cv.split(image)

    img = cv.bilateralFilter(img, 21, 11, 11)

    # img = cv.equalizeHist(img)
    img = gamma(img, 1.2)
    img = cv.normalize(img, None, 0, 255, cv.NORM_MINMAX)
    # img = gamma(img, 2)
    # k = cv.getStructuringElement(cv.MORPH_ELLIPSE, (9, 9))
    # img = cv.morphologyEx(img, cv.MORPH_CLOSE, k)
    k = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
    img = cv.morphologyEx(img, cv.MORPH_CLOSE, k)

    # img = gamma(img, 6)

    # s = cv.equalizeHist(s)

    # img = cv.merge([h, s, img])

    # img = cv.cvtColor(img, cv.COLOR_HSV2BGR)
    # img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # img = cv.equalizeHist(img)

    # img = gamma(img, 2)

    # k = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    # img = cv.morphologyEx(img, cv.MORPH_OPEN, k)
    # img = gamma(img, 2.8)

    # img = cv.equalizeHist(img)
    # plt.hist(img.ravel(), 256, [0, 256])
    # plt.show()

    img = cv.GaussianBlur(img, (5, 5), 1)

    plt.imshow(img, cmap="gray")
    # plt.show()

    # #

    ret, _ = cv.threshold(img, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)

    # edges = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, 51, 10)
    h, w = img.shape

    # print(ret)

    dc, dr = 250, 250
    std = dc * dr / 100
    mean = ret
    edges = img.copy()
    for row in range(0, h, dr):
        for col in range(0, w, dc):
            roi = edges[row: row + dr, col: col + dc]
            if roi.max() < mean:
                edges[row: row + dr, col: col + dc] = 0
            else:
                if roi.min() > mean:
                    edges[row: row + dr, col: col + dc] = 255
                else:
                    _, edges[row: row + dr,
                             col: col + dc] = cv.threshold(roi, ret, 255,
                                                           cv.THRESH_BINARY | cv.THRESH_OTSU)

    # edges = cv.Canny(img, 50, 310)

    edges = cv.medianBlur(edges, 7)
    # edges = cv.medianBlur(edges, 5)
    # edges = cv.medianBlur(edges, 3)

    k = cv.getStructuringElement(cv.MORPH_CROSS, (11, 11))
    edges = cv.morphologyEx(edges, cv.MORPH_CLOSE, k, iterations=1)
    # edges = cv.medianBlur(edges, 7)

    k = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7, 7))

    edges = cv.dilate(edges, k)
    # edges = cv.medianBlur(edges, 7)
    # edges = cv.medianBlur(edges, 5)

    # edges = cv.erode(edges, k, iterations=1)

    # edges = cv.morphologyEx(edges, cv.MORPH_OPEN, k, iterations=1)
    # cv.imwrite("25.png", edges)
    # h, w = edges.shape

    # res = cv.merge([edges, edges, edges])
    # res = np.zeros((h, w, 3), np.uint8)
    # # res = cv.imread("12.png")

    # # edges = cv.erode(edges, k, iterations=2)

    contours, hierarchy = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    for i in contours:
        # print(i)
        if cv.contourArea(i) < 100:
            cv.fillConvexPoly(edges, i, 0)
    #         for pts in i[0]:
    #             edges[pts[1], pts[0]] = 0
    # #         # cv.drawContours(res, i, -1, (255, 255, 255), 5)
    # cv.imshow("1", res)
    # cv.waitKey()
    plt.imshow(edges, cmap="gray")

    # plt.show()
    # # edges = cv.bitwise_not(edges)

    cv.imwrite("bg/" + fn.split("/")[-1], edges)

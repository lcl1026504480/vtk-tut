import cv2
import cv2 as cv
import glob
import numpy as np
import matplotlib.pyplot as plt
n = len(glob.glob("res/*"))


def gamma(raw, g=1.0):
    ig = g
    table = []
    for i in range(256):
        table.append(((i / 255)**ig) * 255)
    table = np.array([table]).astype("uint8")
    return cv2.LUT(raw, table)


epo = 10
# plt.ion()

for fn in range(1, n + 1):
# for fn in [106, 113]:
    print("------------processing  %d------------" % fn)
    pre = float("inf")

    fg = cv2.imread("fg/%d.png" % fn, 0)
    bg = cv2.imread("bg/%d.png" % fn, 0)
    # mk[mk > 0] = 1
    raw = cv2.imread("res/%d.png" % fn, 0)

    raw = cv.bilateralFilter(raw, 1, 11, 11)
    raw = gamma(raw, 6)
    # raw = cv.normalize(raw, None, 0, 255, cv.NORM_MINMAX)
    raw = cv2.equalizeHist(raw)

    k = cv.getStructuringElement(cv.MORPH_ELLIPSE, (11, 11))
    raw = cv.morphologyEx(raw, cv.MORPH_CLOSE, k)

    # raw = cv.GaussianBlur(raw, (5, 5), 1)
    raw = cv2.merge([raw] * 3)
    h, w = fg.shape
    for i in range(epo):
        plt.clf()
        plt.subplot(221)
        plt.imshow(fg, cmap="gray")

        plt.subplot(222)
        plt.imshow(bg, cmap="gray")

        _, mk = cv2.connectedComponents(fg)
        mk = mk + 1
        unknow = cv2.subtract(bg, fg)
        mk[unknow == 255] = 0
        mk[mk > 1] = 2

        mk = cv2.watershed(raw, mk)
        plt.subplot(223)
        plt.imshow(raw)
        # plt.colorbar()

        mk[mk == -1] = 1

        mk[mk == 1] = 0

        mk[mk == 2] = 255
        plt.subplot(224)
        plt.imshow(mk, cmap="gray")
        # plt.colorbar()
        plt.tight_layout()
        plt.suptitle("%d-%d" % (fn, i))
        # plt.get_current_fig_manager().window.showMaximized()
        # plt.show()
        fg = mk.astype(np.uint8)
    cv2.imwrite("final/%d.png" % fn, fg)

    # con = np.array(np.where(mk == -1)).T
    # # print(con)
    # di = []
    # for c in range(con.shape[0]):
    #     if 0 in con[c]:
    #         di.append(c)
    #         continue
    #     if con[c][0] == h - 1:
    #         di.append(c)
    #         continue
    #     if con[c][1] == w - 1:
    #         di.append(c)
    # con = np.delete(con, di, 0)
    # print(con.shape)

    # con = con[:, np.newaxis, :]
    # con = con[:, :, ::-1]
    # # print(con.shape)
    # fg = np.zeros_like(fg, np.uint8)
    # # raw[0] = 0
    # # raw[:, 0] = 0
    # # # fg[]=0
    # # raw[mk == -1] = [0, 255, 0]
    # # print(con)
    # cv2.drawContours(fg, con, -1, 255)

    # contours, hie = cv2.findContours(fg,
    #                                  cv2.RETR_TREE,
    #                                  cv2.CHAIN_APPROX_NONE)
    # print(hie)
    # print(len(contours))
    # if len(contours) > pre:
    #     break
    # pre = len(contours)
    # outline = []
    # for i in range(len(contours)):
    #     if hie[0][i][-1] == -1:
    #         outline.append(i)
    #     if hie[0][i][-1] in outline:
    #         # print(i)
    #         cv2.drawContours(fg, contours, i, 255, -1)
    #         # cv2.fillConvexPoly(fg, contours[i], 255)
    #     if hie[0][i][-2] == -1:
    #         cv2.drawContours(fg, contours, i, 0, -1)
    #         # cv2.fillConvexPoly(fg, contours[i], 0)
    # plt.subplot(224)
    # plt.imshow(fg, cmap="gray")
    # plt.show()
    # fgp = fg

    # plt.pause(0.01)

    # mk = np.clip(mk, 0, 255)
    # mk = mk.astype(np.uint8)
    # print(mk)
    # raw[mk == -1] = [0, 255, 255]


# cv2.imwrite("j1.png", mk)

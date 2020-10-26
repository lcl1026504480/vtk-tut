import cv2
import glob
import numpy as np
import matplotlib.pyplot as plt
n = len(glob.glob("res/*"))
epo = 5
# plt.ion()
pre = float("inf")
for fn in range(1, n + 1):
    print("------------processing  %d------------" % fn)

    fg = cv2.imread("fg/%d.png" % fn, 0)
    bg = cv2.imread("bg/%d.png" % fn, 0)
    # mk[mk > 0] = 1
    raw = cv2.imread("res/%d.png" % fn, 1)
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

        mk = cv2.watershed(raw, mk)
        plt.subplot(223)
        plt.imshow(mk)
        plt.colorbar()

        con = np.array(np.where(mk == -1)).T
        # print(con)
        di = []
        for c in range(con.shape[0]):
            if 0 in con[c]:
                di.append(c)
                continue
            if con[c][0] == h - 1:
                di.append(c)
                continue
            if con[c][1] == w - 1:
                di.append(c)
        con = np.delete(con, di, 0)
        # print(con.shape)

        con = con[:, np.newaxis, :]
        con = con[:, :, ::-1]
        # print(con.shape)
        fg = np.zeros_like(fg, np.uint8)
        # raw[0] = 0
        # raw[:, 0] = 0
        # # fg[]=0
        # raw[mk == -1] = [0, 255, 0]
        # print(con)
        cv2.drawContours(fg, con, -1, 255)

        contours, hie = cv2.findContours(fg,
                                         cv2.RETR_TREE,
                                         cv2.CHAIN_APPROX_NONE)
        # print(hie)
        # print(len(contours))
        if len(contours) > pre:
            break
        pre = len(contours)
        outline = []
        for i in range(len(contours)):
            if hie[0][i][-1] == -1:
                outline.append(i)
            if hie[0][i][-1] in outline:
                cv2.drawContours(fg, contours, i, 255, -1)
                # cv2.fillConvexPoly(fg, contours[i], 255)
            if hie[0][i][-2] == -1:
                cv2.drawContours(fg, contours, i, 0, -1)
                # cv2.fillConvexPoly(fg, contours[i], 0)
        plt.subplot(224)
        plt.imshow(fg, cmap="gray")
        plt.show()

        # plt.pause(0.01)

    # mk = np.clip(mk, 0, 255)
    # mk = mk.astype(np.uint8)
    # print(mk)
    # raw[mk == -1] = [0, 255, 255]


# cv2.imwrite("j1.png", mk)

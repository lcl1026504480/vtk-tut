import cv2
import cv2 as cv
import matplotlib.pyplot as plt
a = cv2.imread("fg/3.png", 0)
contours, hierarchy = cv2.findContours(a, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
for i in contours:
    # print(i)
    if cv2.contourArea(i) < 500:
        cv2.fillConvexPoly(a, i, 0)
cv2.imwrite("fg/3.png", a)
# plt.imshow(a)
# plt.show()

import time
import cv2
import mss
import numpy
import pyautogui
from math import sqrt


sct = mss.mss()
poplovoc_img = cv2.imread("poplavoc.png", 0)
w, h = poplovoc_img.shape[::-1]


def screen():
    x, y = pyautogui.position()
    mon = {"top": y - 100, "left": x - 100, "width": 200, "height": 200}
    cv2.imwrite("screenshot.png", numpy.asarray(sct.grab(mon)))


def find_poplavok(img):
    res = cv2.matchTemplate(img, poplovoc_img, cv2.TM_SQDIFF_NORMED)
    in_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    return top_left, bottom_right


def slow_click():
    pyautogui.mouseDown()
    time.sleep(0.01)
    pyautogui.mouseUp()
    time.sleep(1)
    pyautogui.mouseDown()
    time.sleep(0.01)
    pyautogui.mouseUp()
    time.sleep(1)


def find_fish(arr):
    arr = list(map(lambda x: sqrt(x[0] ** 2 + x[1] ** 2), arr))
    sred = sum(arr) / len(arr)
    sred_diff = sum(map(lambda x: abs(x - sred) % 10, arr)) / len(arr)
    print(sred_diff)
    return sred_diff > 3


def main():
    title = "Bot_vision"
    different_array = list()
    while True:
        screen()
        img = cv2.imread("screenshot.png", 0)
        img_rgb = cv2.imread("screenshot.png", cv2.COLOR_BGR2GRAY)
        top_left, bottom_right = find_poplavok(img)
        different_array.append(top_left)
        if len(different_array) == 10:
            if find_fish(different_array):
                slow_click()
            different_array = []

        cv2.rectangle(img_rgb, top_left, bottom_right, (0, 0, 255), 2)
        cv2.imshow(title, img_rgb)
        key = cv2.waitKey(100)
        if key == 113:
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    main()
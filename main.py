import time

import cv2
import numpy as np
import os
import pyautogui
import pyperclip
import keyboard


class TimerRecognizer:
    def __init__(self, path):
        templates_path = os.listdir(path)
        self.templates = list()
        for i in range(len(templates_path)):
            self.templates.append(cv2.imread(path + templates_path[i]))

    def process(self, img, template_size, index):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        template = cv2.resize(self.templates[index], (template_size[0], template_size[1]))
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.9
        loc = np.where(res >= threshold)
        counter = 0
        positions = list()
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
            counter += 1
            positions.append(pt[0])
        # img = image_resize(img, height = 600)
        return positions

    def get_time(self, img):
        img = img[24: 37, 920: 1000]
        positions = list()
        for i in range(len(self.templates)):
            position = self.process(img, (7, 9), i)
            positions.extend([(pos, i) for pos in position])

        return tuple(i[1] for i in sorted(positions))


def give_timings():
    tr = TimerRecognizer('./ref/')
    scrn = pyautogui.screenshot()
    scrn = np.array(scrn)
    scrn = cv2.cvtColor(scrn, cv2.COLOR_RGB2BGR)
    time_rosh_down = tr.get_time(scrn)

    if time_rosh_down:
        minutes = int(''.join(map(str, time_rosh_down[0:-2:1])))
        seconds = int(''.join(map(str, time_rosh_down[-2:]))) + (minutes * 60)
        pyperclip.copy(
            f'{(seconds + 300) // 60}.{(seconds + 300) % 60:02}, '
            f'{(seconds + 480) // 60}.{(seconds + 480) % 60:02}, '
            f'{(seconds + 660) // 60}.{(seconds + 660) % 60:02}')
    else:
        pyperclip.copy('пусто')


while True:  # making a loop
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('='):  # if key 'q' is pressed
            give_timings()
            pass  # finishing the loop
        else:
            time.sleep(1)
    except:
        break  # if user pressed a key other than the given key the loop will break
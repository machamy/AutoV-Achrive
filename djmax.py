import win32gui
import numpy as np
import cv2
import pyautogui
import threading, time
import winocr
import asyncio
from pprint import pprint

class CannotFindScreenError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class Screen(threading.Thread):
    def __init__(self, duration, window_name='DJMAX RESPECT V'):
        self.duration = duration
        self.window_name = window_name
        self.loop = asyncio.get_event_loop()
        super().__init__()

    async def run(self):
        print("Screen Started", start_time := time.time())
        idx = 0
        while True:
            time.sleep(self.duration)
            print("Screen Check")
            try:
                shot = self.screenshot()
                filename = f"img0.jpg"
                #cv2.imshow(filename,shot)
                cv2.imwrite(filename,shot)
                original_img = cv2.imread(filename)
                img = self.convert_img(original_img)
                cv2.imwrite('resultimg.png', img)

                result = await (winocr.recognize_cv2(img,'Ko'))
                pprint({
                    'text_angle': result.text_angle,
                    'text': result.text,
                    'lines': [{
                        'text': line.text,
                        'words': [{
                            'bounding_rect': {'x': word.bounding_rect.x, 'y': word.bounding_rect.y,
                                              'width': word.bounding_rect.width, 'height': word.bounding_rect.height},
                            'text': word.text
                        } for word in line.words]
                    } for line in result.lines]
                })

                idx += 1
            except CannotFindScreenError as e:
                print(CannotFindScreenError, e)
                continue

    def screenshot(self):
        hwnd = win32gui.FindWindow(None, self.window_name)
        if not hwnd:
            raise CannotFindScreenError('Window not found: ' + self.window_name)

        left, top, right, bot = win32gui.GetClientRect(hwnd)
        x, y = win32gui.ClientToScreen(hwnd, (left, top))
        return cv2.cvtColor(
            np.asarray(
                pyautogui.screenshot(
                    region=(x, y,
                            *win32gui.ClientToScreen(hwnd, (right - x, bot - y))))), cv2.COLOR_RGB2BGR)

    def convert_img(self, img):
        resized_img = cv2.resize(img,
                                 dsize=(1920, 1080),
                                 interpolation=(cv2.INTER_AREA if img.shape[0] >= 1080 and
                                                                  img.shape[0] >= 1920 else cv2.INTER_LINEAR))
        croped_img = resized_img[:, 10:]
        grey_img = cv2.cvtColor(croped_img, cv2.COLOR_BGR2GRAY)
        thresh,res = cv2.threshold(grey_img,198,255,cv2.THRESH_BINARY)
        return res

    def start(self):
        asyncio.run(self.run())

    def end(self):
        self.loop.close()

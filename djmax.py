import win32gui
import numpy as np
import cv2
import pyautogui
import threading, time
import winocr
import asyncio
import keyboard
from PIL import ImageFont, ImageDraw, Image
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
        self._idx = 0
        super().__init__()

    async def run(self):
        print("Screen Started", start_time := time.time())
        print("Screen Check")

        await self.test()

        while False:
            if not keyboard.is_pressed('n'):
                continue
            time.sleep(self.duration)

            try:
                self.test()
            except CannotFindScreenError as e:
                print(CannotFindScreenError, e)
                continue

    async def test(self):
        self._idx += 1
        tmp = 'open'
        filename = f"test{tmp}.jpg"
        original_img = cv2.imread(filename)

        img, grey = self.convert_img(original_img)
        #self.debug_draw_ct(grey, grey)
        cv2.imwrite('resultimg.png', img)

        result = await (winocr.recognize_cv2(img, 'Ko'))
        self.debug_draw_wd(ocr_result=result,result_img=original_img)
        # pprint({
        #     'text_angle': result.text_angle,
        #     'text': result.text,
        #     'lines': [{
        #         'text': line.text,
        #         'words': [{
        #             'bounding_rect': {'x': word.bounding_rect.x, 'y': word.bounding_rect.y,
        #                               'width': word.bounding_rect.width, 'height': word.bounding_rect.height},
        #             'text': word.text
        #         } for word in line.words]
        #     } for line in result.lines]
        # })



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
        cropped_img = resized_img[:, :]
        grey_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
        thresh, res = cv2.threshold(grey_img, 198, 255, cv2.THRESH_BINARY)
        return res, grey_img

    def debug_draw_wd(self, ocr_result, result_img):
        font = ImageFont.truetype('NanumGothicBold.ttf', 20)
        img_pil = Image.fromarray(result_img)
        draw = ImageDraw.Draw(img_pil)
        for line in ocr_result.lines:
            for word in line.words:
                rect = word.bounding_rect
                draw.rectangle(list(map(int,(rect.x, rect.y, rect.x+rect.width, rect.y+rect.height))),
                              outline = (0, 255, 0), width=1)
                draw.text((rect.x,rect.y+20),word.text,font=font,fill=(0,255,0))
        result = np.array(img_pil)
        cv2.imshow("result_wd", result)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def debug_draw_ct(self, img, result_img):
        contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        res = result_img

        for cnt in contours:
            cv2.drawContours(res, [cnt], 0, (255, 0, 0), 3)
        cv2.imshow("result", res)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return res

    def start(self):
        asyncio.run(self.run())

    def end(self):
        self.loop.close()
        print("Screen end")

from pynput.keyboard import Key, Controller
import keyboard
import time
from PIL import ImageGrab
from screeninfo import get_monitors
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

controller = Controller()


def getScreenInfo():
    for m in get_monitors():
        height = m.height
        width = m.width
        return height, width


def locateTextBox():
    first = True
    height, width = getScreenInfo()
    image = ImageGrab.grab()
    for y in range(0, height, 10):
        for x in range(0, width, 5):
            color = image.getpixel((x, y))
            if color[0] == 246 and color[1] == 251 and color[2] == 255:
                if first:
                    minX = x
                    maxX = x
                    minY = y
                    maxY = y
                    first = False
                if x > maxX:
                    maxX = x
                elif x < minX:
                    minX = x
                if y > maxY:
                    maxY = y
                elif y < minY:
                    y = minY
    if first:
        return 0, 0, 0, 0
    else:
        return minX, minY, maxX, maxY


def analyzeText():
    if locateTextBox() == (0, 0, 0, 0):
        print("Text box was not detected")
    else:
        image = ImageGrab.grab(bbox=(locateTextBox()))
        image.save("text.png")
        img = cv2.imread("text.png")
        text = pytesseract.image_to_string(img)
        text = text.replace("\n", " ")
        parts = text.split("change display format")
        for i in parts[0]:
            if i == "|":
                controller.press("I")
                controller.release("I")
                continue;
            controller.press(i)
            controller.release(i)
            if keyboard.is_pressed("PAGEUP"):
                break;
            time.sleep(0.03)


while True:
    if keyboard.is_pressed("HOME"):
        analyzeText()
        time.sleep(1.0)

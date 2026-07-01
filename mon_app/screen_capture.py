import mss
from PIL import Image


def grab_screenshot():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        w, h = img.size
        img = img.resize((w // 2, h // 2), Image.LANCZOS)
        return img

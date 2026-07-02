import mss
from PIL import Image

_sct = mss.mss()
_primary_monitor = _sct.monitors[1]


def grab_screenshot():
    screenshot = _sct.grab(_primary_monitor)
    img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
    w, h = img.size
    img = img.resize((w // 2, h // 2), Image.LANCZOS)
    return img

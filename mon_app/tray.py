import pystray
from PIL import Image, ImageDraw
import threading
import logging

logger = logging.getLogger(__name__)


def create_icon_image():
    img = Image.new("RGB", (64, 64), color="black")
    draw = ImageDraw.Draw(img)
    draw.rectangle((16, 16, 48, 48), fill="white")
    draw.text((20, 20), "AI", fill="black")
    return img


class SystemTray:
    def __init__(self, on_quit):
        self.icon = pystray.Icon(
            "MonApp",
            create_icon_image(),
            "Screen Scraper AI",
            pystray.Menu(
                pystray.MenuItem("Quitter", on_quit)
            ),
        )

    def run(self):
        self.icon.run()

    def stop(self):
        self.icon.stop()

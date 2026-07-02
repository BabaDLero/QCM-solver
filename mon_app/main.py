import logging
import sys
import time
import threading

from pynput import keyboard

import config
import screen_capture
import api_client
from overlay import Overlay
from tray import SystemTray

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler(sys.stderr),
    ],
)
logging.getLogger("PIL").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

overlay = None
_last_trigger = 0


def handle_request():
    logger.debug(">>> handle_request START")
    try:
        overlay.show_text("Analyse en cours...")
        logger.debug("OCR + API starting")
        img = screen_capture.grab_screenshot()
        logger.debug("Screenshot captured")
        response = api_client.ask_deepseek(img)
        logger.debug(f"API response: {repr(response)[:120]}")
        if not response or not response.strip():
            response = "Aucune reponse de l'API"
        overlay.show_text(response)
        logger.debug("Response displayed")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        overlay.show_text(f"Erreur : {e}", color="#cc0000")
    logger.debug("<<< handle_request END")


def on_press(key):
    global _last_trigger
    try:
        trigger = config.TRIGGER_KEY
        is_match = False
        if len(trigger) == 1:
            if hasattr(key, 'char') and key.char == trigger:
                is_match = True
        else:
            if key == getattr(keyboard.Key, trigger):
                is_match = True

        if is_match:
            now = time.monotonic()
            if now - _last_trigger < config.DEBOUNCE_SECONDS:
                logger.debug(f"* ignored (debounce, {now - _last_trigger:.1f}s)")
                return
            _last_trigger = now

            if overlay.busy:
                logger.debug("* ignored (busy)")
                return

            if overlay.is_visible:
                logger.debug("* overlay visible -> request_hide")
                overlay.request_hide()

            logger.debug("* trigger accepted -> request_capture")
            overlay.request_capture()
    except AttributeError:
        pass


def start_keyboard_listener():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


def on_quit(icon, item):
    logger.info("Application quit requested")
    icon.stop()
    sys.exit(0)


def main():
    global overlay
    overlay = Overlay(capture_callback=handle_request)

    tray = SystemTray(on_quit)
    tray_thread = threading.Thread(target=tray.run, daemon=True)
    tray_thread.start()

    listener_thread = threading.Thread(target=start_keyboard_listener, daemon=True)
    listener_thread.start()

    logger.info("Application started")
    overlay.run()


if __name__ == "__main__":
    main()

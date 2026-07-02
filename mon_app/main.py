import threading
import logging
import sys
import time

from pynput import keyboard

import config
import screen_capture
import api_client
from overlay import Overlay
from tray import SystemTray

logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

overlay = None
_last_trigger = 0
_busy_lock = threading.Lock()
_busy = False


def handle_request():
    global _busy
    with _busy_lock:
        if _busy:
            return
        _busy = True

    try:
        overlay.show_text_safe("Analyse en cours...", color="#888888")
        logger.info("Trigger pressed — capturing screen")
        img = screen_capture.grab_screenshot()
        logger.info("Screenshot captured, calling API")
        response = api_client.ask_deepseek(img)
        logger.info(f"API response received: {response[:100] if response else 'empty'}")
        overlay.show_text_safe(response)
    except Exception as e:
        logger.error(f"Error in handle_request: {e}")
        overlay.show_text_safe(f"Erreur : {e}", color="red")
    finally:
        with _busy_lock:
            _busy = False


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
                return
            _last_trigger = now

            if _busy:
                return

            if overlay.is_visible:
                overlay.hide_safe()

            threading.Thread(target=handle_request, daemon=True).start()
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
    overlay = Overlay()

    tray = SystemTray(on_quit)
    tray_thread = threading.Thread(target=tray.run, daemon=True)
    tray_thread.start()

    listener_thread = threading.Thread(target=start_keyboard_listener, daemon=True)
    listener_thread.start()

    logger.info("Application started")
    overlay.run()


if __name__ == "__main__":
    main()

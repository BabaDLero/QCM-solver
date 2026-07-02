import tkinter as tk
import ctypes
import config
import logging

logger = logging.getLogger(__name__)


class Overlay:
    def __init__(self, capture_callback=None):
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "#f0f0f0")
        self.root.configure(bg="#f0f0f0")

        screen_height = self.root.winfo_screenheight()
        x = 0
        y = screen_height - config.OVERLAY_HEIGHT
        self.root.geometry(f"{config.OVERLAY_WIDTH}x{config.OVERLAY_HEIGHT}+{x}+{y}")

        self.label = tk.Label(
            self.root,
            text="",
            fg="#888888",
            bg="#f0f0f0",
            wraplength=config.OVERLAY_WIDTH - 20,
            font=("Consolas", 12, "bold"),
            justify="left",
            anchor="nw",
            padx=10,
            pady=10,
        )
        self.label.pack(fill="both", expand=True)

        self._hide_from_taskbar()
        self.root.withdraw()
        self._auto_hide_id = None
        self._visible = False

        self._pending_capture = False
        self._pending_hide = False
        self._busy = False
        self._capture_callback = capture_callback

        self._check_pending()

    def _hide_from_taskbar(self):
        try:
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            ctypes.windll.user32.SetWindowLongW(
                hwnd, -20,
                ctypes.windll.user32.GetWindowLongW(hwnd, -20) | 0x80
            )
        except Exception as e:
            logger.warning(f"Could not hide from taskbar: {e}")

    def _check_pending(self):
        try:
            if self._pending_hide and not self._busy:
                self._pending_hide = False
                self.hide()
            if self._pending_capture and not self._busy:
                self._pending_capture = False
                self._busy = True
                if self._capture_callback:
                    self._capture_callback()
                self._busy = False
        except Exception as e:
            logger.error(f"Error in _check_pending: {e}", exc_info=True)
        self.root.after(100, self._check_pending)

    def request_capture(self):
        self._pending_capture = True

    def request_hide(self):
        self._pending_hide = True

    @property
    def busy(self):
        return self._busy

    def show_text(self, text, color="#888888"):
        if self._auto_hide_id:
            self.root.after_cancel(self._auto_hide_id)
            self._auto_hide_id = None
        self.label.config(text=text, fg=color)
        self.root.update_idletasks()
        self.root.deiconify()
        self.root.lift()
        self._visible = True
        self._auto_hide_id = self.root.after(
            config.AUTO_HIDE_SECONDS * 1000, self.hide
        )

    def hide(self):
        self.root.withdraw()
        if self._auto_hide_id:
            self.root.after_cancel(self._auto_hide_id)
            self._auto_hide_id = None
        self._visible = False

    @property
    def is_visible(self):
        return self._visible

    def run(self):
        self.root.mainloop()

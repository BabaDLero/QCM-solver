import tkinter as tk
import ctypes
import config
import logging

logger = logging.getLogger(__name__)


class Overlay:
    def __init__(self):
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
            fg="#1a1a1a",
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

        self._pending_text = ""
        self._pending_color = "#1a1a1a"

        self.root.bind("<<ShowText>>", self._on_show_text)
        self.root.bind("<<Hide>>", self._on_hide)

    def _hide_from_taskbar(self):
        try:
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            ctypes.windll.user32.SetWindowLongW(
                hwnd, -20,
                ctypes.windll.user32.GetWindowLongW(hwnd, -20) | 0x80
            )
        except Exception as e:
            logger.warning(f"Could not hide from taskbar: {e}")

    def _on_show_text(self, event):
        self.show_text(self._pending_text, self._pending_color)

    def _on_hide(self, event):
        self.hide()

    def show_text_safe(self, text, color="#1a1a1a"):
        self._pending_text = text
        self._pending_color = color
        self.root.event_generate("<<ShowText>>", when="tail")

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

    def hide_safe(self):
        self.root.event_generate("<<Hide>>", when="tail")

    def hide(self):
        self.root.withdraw()
        self._auto_hide_id = None
        self._visible = False

    @property
    def is_visible(self):
        return self._visible if hasattr(self, '_visible') else False

    def run(self):
        self.root.mainloop()

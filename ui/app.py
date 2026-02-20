import customtkinter as ctk
import ctypes
from core.config import load_config
from core.language import t
from core.youtube_search import search_youtube
from core.player import Player
from ui.sidebar import Sidebar
from ui.settings_window import SettingsWindow
from ui.login_window import LoginWindow
from ui.animations import fade_in

ctk.set_appearance_mode("dark")

class App:

    def __init__(self):
        self.config = load_config()
        self.player = Player()

        self.root = ctk.CTk()
        self.root.geometry("1200x750")
        self.root.title("Ultimate Downloader V8")

        self.enable_glass()

        self.sidebar = Sidebar(self)
        self.main_area = ctk.CTkFrame(self.root)
        self.main_area.pack(side="right", fill="both", expand=True)

        self.build_main()

        fade_in(self.root)

    def enable_glass(self):
        try:
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, 38,
                ctypes.byref(ctypes.c_int(2)),
                ctypes.sizeof(ctypes.c_int)
            )
        except:
            pass

    def build_main(self):
        self.search_entry = ctk.CTkEntry(
            self.main_area,
            placeholder_text="YouTube / Spotify Search"
        )
        self.search_entry.pack(pady=20, padx=20, fill="x")

        ctk.CTkButton(
            self.main_area,
            text="Search",
            command=self.search
        ).pack()

        self.results_box = ctk.CTkTextbox(
            self.main_area,
            height=300
        )
        self.results_box.pack(pady=20, padx=20, fill="both", expand=True)

        self.progress = ctk.CTkProgressBar(self.main_area)
        self.progress.pack(fill="x", padx=20, pady=10)

    def search(self):
        query = self.search_entry.get()
        results = search_youtube(query)
        self.results_box.delete("1.0", "end")
        for r in results:
            self.results_box.insert("end", f"{r['title']}\n")

    def run(self):
        LoginWindow(self.root)
        self.root.mainloop()
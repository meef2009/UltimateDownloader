import customtkinter as ctk
from core.language import t

class Sidebar(ctk.CTkFrame):
    def __init__(self, app):
        super().__init__(app.root, width=220)
        self.pack(side="left", fill="y")

        ctk.CTkLabel(self, text="V8").pack(pady=20)

        ctk.CTkButton(self, text="Settings",
                      command=lambda:
                      SettingsWindow(app)).pack(pady=10)
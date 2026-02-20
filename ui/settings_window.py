import customtkinter as ctk
from core.config import save_config

class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, app):
        super().__init__(app.root)
        self.app = app
        self.geometry("400x400")

        self.theme_var = ctk.StringVar(value=app.config["theme"])
        ctk.CTkOptionMenu(self,
                          values=["dark", "light"],
                          variable=self.theme_var).pack(pady=10)

        ctk.CTkButton(self,
                      text="Save",
                      command=self.save).pack()

    def save(self):
        self.app.config["theme"] = self.theme_var.get()
        save_config(self.app.config)
        self.destroy()
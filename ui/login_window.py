import customtkinter as ctk
from core.accounts import login, register

class LoginWindow(ctk.CTkToplevel):
    def __init__(self, root):
        super().__init__(root)
        self.geometry("400x300")
        self.title("Login")

        self.user = ctk.CTkEntry(self, placeholder_text="Username")
        self.user.pack(pady=10)

        self.pwd = ctk.CTkEntry(self,
                                placeholder_text="Password",
                                show="*")
        self.pwd.pack(pady=10)

        ctk.CTkButton(self,
                      text="Login",
                      command=self.do_login).pack(pady=5)

        ctk.CTkButton(self,
                      text="Register",
                      command=self.do_register).pack()

    def do_login(self):
        if login(self.user.get(), self.pwd.get()):
            self.destroy()

    def do_register(self):
        register(self.user.get(), self.pwd.get())
import customtkinter as ctk
from app import open
from app1 import app
class root(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        #comonents
        print(self)
        user_name = ctk.CTkEntry(self)
        user_name.grid(row=0, column=0)
        b = ctk.CTkButton(self,text ="login" , command=lambda:self.login(user_name.get()))
        b.grid(row=1, column=0)
        #grid



    def login(self, user):
        open(self, user)
       #self.open_app()
    def open_app(self):
        win =app(self)
        win.mainloop()


if __name__ == "__main__":
    root = root()
    root.mainloop()
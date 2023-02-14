import customtkinter as ctk
from summary import summary
from tkinter import  ttk
import tkinter as tk



class Window(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.geometry('300x300')
        self.title('Toplevel Window')
        S = summary("ma", 51, "today")
        text_box = ctk.CTkTextbox(self,height=250)
        text_box.insert(tk.END, S.summary_report())
        text_box.pack()
        ctk.CTkButton(self,
                text='Close',
                command=self.destroy).pack(expand=True)

'''class Report(ctk.CTkToplevel):
    def __int__(self, app):
        super.__init__(app)
        S = summary("ma", 51, "today")
        report = self(app)
        text_box = ctk.CTkTextbox(self, text=S.summary_report())
        text_box.pack()
        report.mainloop()'''
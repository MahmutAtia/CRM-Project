import tkinter
import tkinter.messagebox as mbox
import customtkinter as ctk
from tkinter import ttk
from SheetFunctıons import  get_all_companies,history,update_c,set_work_sheet,add
from constansts import columns_1, columns_2 ,countries, contacts,results, dates
from helper import send


class app(ctk.CTkToplevel):
    def __int__(self,parent):
        super().__int__(parent)

        self.resizable(width=False, height=False)
        self.geometry("1250x600")
        self.title("Sirma")
        c = ctk.CTkLabel(text="sasdjognöklmdd po")
        c.pack()
        self.mainloop()
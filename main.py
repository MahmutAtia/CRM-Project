import tkinter
import tkinter.messagebox as mbox
import customtkinter as ctk
from tkinter import ttk
# from PIL import Image, ImageTK
from constansts import columns_1, columns_2 ,countries, contacts,results, dates
from ttkwidgets.autocomplete import AutocompleteCombobox
from tip import CreateToolTip
from helper import send
from app import open

root = ctk.CTk()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
def sign_in_ma():
    open(root, "ma")

def sign_in_amir():
    open(root,"amir")

def sign_in_ali():
    open(root,"ali")

b_ma = ctk.CTkButton(root,command=sign_in_ma)
b_ma.pack()
b_amir = ctk.CTkButton(root,command=sign_in_amir)
b_amir.pack()
b_ali = ctk.CTkButton(root,command=sign_in_ali)
b_ali.pack()


root.mainloop()
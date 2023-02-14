import tkinter
import tkinter.messagebox as mbox
import customtkinter as ctk
from tkinter import ttk
from SheetFunctıons import  get_all_companies,history,update_c,set_work_sheet,add
from constansts import columns_1, columns_2 ,countries, contacts,results, dates
from ttkwidgets.autocomplete import AutocompleteCombobox
from tip import CreateToolTip#
from bidi.algorithm import get_display
from helper import send
from report import Window


def open(root,user):
    global history_or_main
    history_or_main = False
    wk = set_work_sheet(user)
    df_company,df_impornot = get_all_companies(wk)
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    # creating the app

    app = ctk.CTkToplevel(root)
    root.withdraw()
    app.resizable(width=False, height=False)
    app.geometry("1250x650")
    app.title("Sirma")

    global selected_index
    global contact_selected_index
    global table
    global company_index
    global filter_used
    filter_used = False
    #add some style
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background = "#D3D3D3",
                    foreground = "black",
                    rowwheight = 25,
                    fieldbackground = '#D3D3D3')
    style.map("Treeview",
              [("selected","#437083")])

    #function
    #update_contacts
    def tag(i):
        if df_impornot.iloc[i,0] == "1":
            return ("notImportant")
        elif df_impornot.iloc[i,1] == "1":
            return ("important")
        elif i%2 == 0:
            return ("evenrow")
        elif i%2 != 0:
            return ("oddrow")
    def search(*args):
        items = tree.get_children()
        for each in items:
            if str(search_by_name.get()).lower() in str(tree.item(each)["values"][1]).lower():
                search_values = tree.item(each)["values"]
                tree.delete(each)
                tree.insert("",0,values=search_values ,tag = tag(search_values[0]-1),)
    def filter_country_func():
        global filter_used
        show_companies_2()
        filter_used = True
        items = tree.get_children()
        for i,each in enumerate(items):
            if str(filter_by_countery.get()) in str(tree.item(each)["values"][2]):
                search_values = tree.item(each)["values"]
                tree.delete(each)
                tree.insert("", tkinter.END, values=search_values, tag=tag(i), )


            else:
                tree.delete(each)
    def filter_country(e):
        filter_country_func()

    def send_number():
        send(e1_company.get(), e3_number.get())

    def delete_enteries():
        # delet records
        e1_company.set((" "))
        e2_contery.set(" ")
        e3_number.set(" ")
        e4_email.delete(0, tkinter.END)
        e5_manger.delete(0, tkinter.END)
        e6_web.set(" ")
        b1_update_company.configure(state=tkinter.DISABLED)
    def switch(b1):
        if b1.cget("state") == tkinter.NORMAL:
            print(b1.cget("state") == tkinter.NORMAL)
            b1.configure(state=tkinter.DISABLED)
        else:
            b1.configure(state= tkinter.NORMAL)
    def show_companies_2():
        global  filter_used
        filter_used = False
        df1= df_company

        for i in tree.get_children():
            tree.delete(i)
        app.update()

        for i in range (df_company.shape[0]):
                tree.insert('', index= tkinter.END, iid= 1+i,values= [1+i]+df1.iloc[i,:].tolist(), tag = tag(i))

    def show_companies():
        global filter_used
        filter_used = False
        wk = set_work_sheet(user)
        df1,df_impornot = get_all_companies(wk)

        for i in tree.get_children():
            tree.delete(i)
        app.update()
        print(len(df1), df1.iloc[-1,:])
        for i in range(df_company.shape[0]):
            tree.insert('', index=tkinter.END, iid=1 + i, values=[1 + i] + df1.iloc[i, :].tolist(), tag=tag(i))





    def up_contact():
        row = get_entery()
        update_c(company_index,int(selected_index),row,wk)


    def add_contact():
        row = get_entery()
        if len(tree.get_children()) == 0: new_index = 0
        else : new_index = len(tree.get_children()) -1
        print(len(tree.get_children()))
        print(new_index)
        update_c(company_index, new_index , row,wk) # -1 because of the list

        # insert in tree
        children = tree.get_children()
        mbox.showinfo("Well Done", f"The Company {row[0]} Is Added Successfully")
        tree.insert("", 'end', values=([len(children) + 1] + row))
        delete_enteries()



    def get_history():
        global company_index
        selected = tree.focus()
        values = tree.item(selected, "values")
        heading.configure(text= values[1])
        idx = int(values[0])+2
        company_index = idx
        return history(idx,wk)

    def show_history():
        global history_or_main
        history_or_main = True

        add_frame.pack_forget()
        choose.pack()
        l_chose.pack()

        delete_enteries()
        li = get_history()
        #####
        columns = columns_2
        tree["columns"] = columns
        tree.heading("#0",text="", anchor=tkinter.CENTER)
        for i in columns:
            tree.heading(i ,text=i, anchor=tkinter.CENTER)

        for i in columns:
            if i == "index":
                tree.column(i, minwidth=0, width=50, stretch=tkinter.NO, anchor=tkinter.CENTER)
            else:
                tree.column(i, minwidth=0, width=190, stretch=tkinter.NO, anchor=tkinter.CENTER)

        #####

        l1_company.configure(text= "Contact Method")
        e1_company.configure(values=contacts)
        l2_contery.configure(text="Number of contact")
        e2_contery.configure(values= [])
        l3_number.configure(text="Date")
        e3_number.configure(values= dates)
        b_send.grid_forget()
        b_minuts.grid(row=3, column=4, padx=5, pady=10)
        l4_email.configure(text="Puan")
        l5_manger.configure(text="Minuts")
        l6_web.configure(text="Result")
        e6_web.configure(values = results)

        ###### change Buttons #####
        b1_update_company.configure(command= up_contact)
        b1_new_company.configure(command=add_contact)
        b1_new_company.grid_forget()
        b_report.grid_forget()



        for i in tree.get_children():
            tree.delete(i)
        app.update()



        for i in range(len(li)):
            if not li[i]:
                tree.insert('', index=tkinter.END, values=[i + 1], tag="evenrow", )

            else:
                if i % 2 == 0:
                    tree.insert('', index=tkinter.END, values=[i+1]+li[i][0] , tag="evenrow", )
                else:
                    tree.insert('',index=tkinter.END, values=[i+1]+li[i][0] , tag=("oddrow",))
        b3_show_history.configure(state=tkinter.DISABLED)
        b4_back.configure(state=tkinter.NORMAL)
        b1_update_company.configure(state=tkinter.DISABLED)



    def back():
        global history_or_main
        history_or_main = False
        columns = columns_1
        tree["columns"] = columns
        tree.heading("#0",text="", anchor=tkinter.W)
        for i in columns:
            tree.heading(i,text=i, anchor=tkinter.W)
        for i in columns:
            if i == "index":
                tree.column(i, minwidth=0, width=50, stretch=tkinter.NO, anchor=tkinter.CENTER)
            else:
                tree.column(i, minwidth=0, width=190, stretch=tkinter.NO, anchor=tkinter.CENTER)

        ###### change Buttons #####
        b1_update_company.configure(command=update_btn)
        b1_new_company.configure(command=add_btn)
        b1_new_company.grid(row = 1, column = 6 ,padx = 25,pady = 10 )
        b_report.grid(row = 2, column = 6 ,padx = 25,pady = 10 )


        l_contact.grid_forget()
        l1_company.configure(text= "Company Name")
        e1_company.configure(values= [])
        l2_contery.configure(text="Country")
        e2_contery.configure(values=countries)
        l3_number.configure(text="Phone Number")
        e3_number.configure(values=[])
        b_send.grid(row=2, column=4, padx=5, pady=10)
        b_minuts.grid_forget()
        l4_email.configure(text="Email")
        l5_manger.configure(text="Manger")
        l6_web.configure(text="Web Site")
        e6_web.configure(values= [])

        b4_back.configure(state=tkinter.DISABLED)
        delete_enteries()

        #Tree
        if filter_used:
            filter_country_func()
            childern = tree.get_children()
            for i, child in enumerate(childern):
                child_index = 0
                print(tree.item(child)["values"][0], str(company_index - 2))
                if str(tree.item(child)["values"][0]) == str(
                        company_index - 2):  # company index is spread sheet idex, tree index -2
                    child_index = i
                    print(i)
                    break

            tree.focus_set()
            tree.focus(childern[child_index])
            tree.selection_set(childern[child_index])
            tree.see(childern[child_index])
        else:
            show_companies_2()
            childern = tree.get_children()
            tree.focus_set()
            tree.focus(
                childern[company_index - 3])  # because chidern is list 0 , and -2 deffrent between sheet and tree
            tree.selection_set(childern[company_index - 3])
            tree.see(childern[company_index - 3])
            # tree.see( childern[int(selected_index) -3] ) # selected_index in spread sheet in tree view - 3

    #tree frame
    tree_frrame = ctk.CTkFrame(app,corner_radius=15, height=200)
    tree_frrame.pack(pady=20,padx =20 ,expand = "yes", fill="x")

    #tree view scroll bar
    tree_scroll = ctk.CTkScrollbar(tree_frrame)
    tree_scroll.pack(pady = 10 ,side = tkinter.RIGHT, fill=tkinter.Y)


    #tree view
    heading = ctk.CTkLabel(tree_frrame,text="All Companies" )
    heading.pack()
    tree = ttk.Treeview(tree_frrame,yscrollcommand= tree_scroll.set,selectmode= "extended")
    tree.pack(fill='x')
    tree.tk.call("source", "azure.tcl")
    tree.tk.call("set_theme", "light")


    #confifure scroll bar
    tree_scroll.configure(command=tree.yview)

    #columns

    #select columns
    columns = columns_1

    tree["columns"] = columns_1
    tree.column("#0", width=0, stretch=tkinter.NO)
    for i in columns:
        if i == "index":
            tree.column(i, minwidth=0, width=50,stretch= tkinter.NO,anchor=tkinter.CENTER)
        else:
            tree.column(i,minwidth=0, width=190,stretch= tkinter.NO,anchor= tkinter.CENTER)

    # create heading
    tree.heading("#0", text="", anchor= tkinter.W)
    for i in columns:
        tree.heading(i, text = i, anchor= tkinter.W)

    # create striped rows
    tree.tag_configure("oddrow", background="white")
    tree.tag_configure("evenrow", background="lightblue")
    tree.tag_configure("important", background="green")
    tree.tag_configure("notImportant", background="red")


    #Frame Buttons

    buttons_frame = ctk.CTkFrame(app,corner_radius=15, height= 30)
    buttons_frame.pack(pady=20,padx =20 ,expand = "yes", fill="x",)

    get_all = ctk.CTkButton(buttons_frame, text = "Get All Companies", width=10, height=10, corner_radius=20, command= show_companies_2)
    get_all.grid(row=0 , column = 0,padx = 25,pady = 10)

    get_all = ctk.CTkButton(buttons_frame, text="Refresh", width=10, height=10, corner_radius=20,
                            command=show_companies)
    get_all.grid(row=0, column=1, padx=25, pady=10)

    get_all = ctk.CTkButton(buttons_frame, text = "Clear All Records", width=10, height=10, corner_radius=20, command= delete_enteries)
    get_all.grid(row=0 , column = 2,padx = 25,pady = 10)


    filter_by_countery = ctk.CTkComboBox(buttons_frame, values= df_company[1].unique(), command= filter_country)
    filter_by_countery.grid(row=0, column=3 ,padx = 25,pady = 10 )




    search_by_name = ctk.CTkEntry(buttons_frame)
    search_by_name.grid(row = 0, column= 4 ,padx = 10,pady = 10 )

    b_search = ctk.CTkButton(buttons_frame,text= "Search", command= search)
    b_search.grid(row=0,column= 5, padx = 10,pady = 10 )

    def get_report():
        Window(app)


    #please chose frame
    choose = ctk.CTkFrame(app,corner_radius=15)
    l_chose = ctk.CTkLabel(choose, text= "Please Choose A Contact For Adding Or Updating")
    #record frame
    add_frame = ctk.CTkFrame(app,corner_radius=15)
    add_frame.pack()

    l_contact= ctk.CTkLabel(add_frame,text="")
    # company name
    l1_company = ctk.CTkLabel(add_frame, text =  "Company Name")
    l1_company.grid(row = 1, column= 0, padx = 10,pady = 10)
    e1_company = ctk.CTkComboBox(add_frame, width=250)
    e1_company.set((""))
    e1_company.configure(values=[e1_company.get()])
    e1_company.grid(row = 1, column= 1, padx = 10,pady = 10)
    #CreateToolTip(e1_company, text = e1_company.get())


    l2_contery = ctk.CTkLabel(add_frame,text = "Country" )
    l2_contery.grid(row = 1, column= 2, padx = 10,pady = 10)



    e2_contery = ctk.CTkComboBox(add_frame, values= countries)
    e2_contery.grid(row = 1, column= 3, padx = 10,pady = 10)


    l3_number = ctk.CTkLabel(add_frame, text = "Phone Number")
    l3_number.grid(row = 2, column= 2, padx = 10,pady = 10)

    e3_number = ctk.CTkComboBox(add_frame )
    e3_number.configure(values=[e3_number.get()])
    e3_number.grid(row = 2, column= 3, padx = 10,pady = 10)


    l4_email = ctk.CTkLabel(add_frame, text = "Email")
    l4_email.grid(row = 2, column= 0, padx = 10,pady = 10)

    e4_email = ctk.CTkEntry(add_frame,width=250 )
    e4_email.grid(row = 2, column= 1, padx = 10,pady = 10)


    l5_manger = ctk.CTkLabel(add_frame,text = "Manger")
    l5_manger.grid(row = 3, column= 2, padx = 10,pady = 10)
    e5_manger = ctk.CTkEntry(add_frame )
    e5_manger.grid(row = 3, column= 3, padx = 10,pady = 10)


    l6_web = ctk.CTkLabel(add_frame, text = "Web Site")
    l6_web.grid(row = 3, column= 0, padx = 10,pady = 10)
    e6_web = ctk.CTkComboBox(add_frame, width=250 )
    e6_web.configure(values=[e6_web.get()])

    e6_web.grid(row = 3, column= 1, padx = 10,pady = 10)

    # select a record
    def select_record(e):
        global selected_index
        global selected_chiled
        b1_update_company.configure(state=tkinter.NORMAL)
        b3_show_history.configure(state=tkinter.NORMAL)
        #delet records
        e1_company.set(" ")
        e2_contery.set(" ")
        e3_number.set(" ")
        e4_email.delete(0, tkinter.END)
        e5_manger.delete(0,tkinter.END)
        e6_web.set(" ")
        # grab the selected record
        selected = tree.focus()
        values = tree.item(selected, "values")
        print(values)
        # fill entery
        selected_index = values[0]
        if history_or_main==True:
            choose.pack_forget()
            l_chose.pack_forget()
            add_frame.pack()

            l_contact.configure(text=f"Your Updating Contact Number {values[0]}")
            l_contact.grid(row=0,column= 0,padx = 10,pady = 10)

        print(selected_index)
        e1_company.set( (values[1]))
        e1_company.set(e1_company.get())
        e2_contery.set(values[2])
        e3_number.set(values[3])
        e3_number.set(e3_number.get())
        e4_email.insert(0, values[4])
        if values[5]:
            e5_manger.insert(0, values[5])
        else:
            e5_manger.insert(0,"00:00")

        e6_web.set(values[6])
        e6_web.set(e6_web.get())



    # bind select to the tree
    tree.bind("<ButtonRelease-1>", select_record)

    #add button function
    def get_entery():
        e1=e1_company.get()
        e2= e2_contery.get()
        e3=e3_number.get()
        e4=e4_email.get()
        e5=e5_manger.get()
        e6=e6_web.get()
        return [e1,e2,e3,e4,e5,e6]

    def add_btn():
        global selected_index
        row = get_entery()

        children = tree.get_children()
        selected_index = len(children)
        tree.insert("", 'end', values=([len(children) + 1] + row))
        add(row, selected_index,wk,df_company, add= True)
        print(row , selected_index)
        print(len(children))
        tree.see(children[-1])
        mbox.showinfo("Well Done",f"The Company {row[0]} Is Added Successfully")
        delete_enteries()



    def update_btn():
        global company_index
        row = get_entery()
        add(row, selected_index,wk,df_company)
        if filter_used:
            filter_country_func()
            childern = tree.get_children()
            for i, child in enumerate(childern):
                child_index = 0
                print(tree.item(child)["values"][0], str(company_index - 2))
                if str(tree.item(child)["values"][0]) == str(
                        company_index - 2):  # company index is spread sheet idex, tree index -2
                    child_index = i
                    print(i)
                    break

            tree.focus_set()
            tree.focus(childern[child_index])
            tree.selection_set(childern[child_index])
            tree.see(childern[child_index])
        else:
            show_companies_2()
            childern = tree.get_children()
            tree.focus_set()
            tree.focus(childern[company_index - 3])  # because chidern is list 0 , and -2 deffrent between sheet and tree
            tree.selection_set(childern[company_index - 3])
            tree.see(childern[company_index - 3])

    def add_one_min():
        mins,secs = e5_manger.get().split(":")
        mins = list(mins)
        print(int(mins[1])+1)
        n = int(mins[1])+1
        e5_manger.delete(0,tkinter.END)
        e5_manger.insert(0, f"{mins[0]}{n}:{secs}")

    b1_new_company = ctk.CTkButton(add_frame, text= "Add New", command=  add_btn, )
    b1_new_company.grid(row = 1, column = 6 ,padx = 25,pady = 10 )
    b_report = ctk.CTkButton(add_frame, text="Get Today's Report", command=get_report)
    b_report.grid(row=2, column=6, padx=25, pady=10)


    b1_update_company = ctk.CTkButton(add_frame, text= "Update Records", command= update_btn, state= tkinter.DISABLED)
    b1_update_company.grid(row = 1, column =5 ,padx = 25,pady = 10 )


    b_send = ctk.CTkButton(add_frame, text="send",command= send_number, width= 50)
    b_send.grid(row=2, column=4, padx=5, pady=10)
    b_minuts = ctk.CTkButton(add_frame, text="+",command=add_one_min, width= 50)



    b3_show_history = ctk.CTkButton(add_frame, text= "Show History", command= show_history, state= tkinter.DISABLED)
    b3_show_history.grid(row = 2, column =5 ,padx = 15,pady = 10)

    b4_back = ctk.CTkButton(add_frame, text= "Back", command= back, state= tkinter.DISABLED)
    b4_back.grid(row = 3, column = 5 ,padx = 15,pady = 10)
    #Funtions






    frame = ctk.CTkFrame(master=app, width=320, height=360, corner_radius=15)
    l1 = ctk.CTkLabel(master= frame, text="Add New Company", font=("Century Gothic", 20))
    l2 = ctk.CTkLabel(master=frame, text="Company")




    #todo 0: playing with grid system

    # Row 1

    #heading.grid(row=2,column =1) # col 1
    #space_col_2.grid(row=1,column = 2)# col 2









    app.mainloop()



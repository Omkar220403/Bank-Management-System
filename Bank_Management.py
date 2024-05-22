from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import sqlite3

def Database():
    global conn, cursor
    conn = sqlite3.connect("bank.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS BANK_REGISTRATION (ACCOUNT_NO INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, CONTACT TEXT, EMAIL TEXT, BRANCH TEXT)")

def DisplayForm():
    display_screen = Tk()
    display_screen.geometry("900x400")
    display_screen.title("Bank Management System")

    global tree
    global SEARCH
    global name,contact,email,branch

    SEARCH = StringVar()
    name = StringVar()
    contact = StringVar()
    email = StringVar()
    branch = StringVar()

    TopViewForm = Frame(display_screen, width=600, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)

    LFrom = Frame(display_screen, width="350")
    LFrom.pack(side=LEFT, fill=Y)
    
    LeftViewForm = Frame(display_screen, width=500,bg="gray")
    LeftViewForm.pack(side=LEFT, fill=Y)
    
    MidViewForm = Frame(display_screen, width=600)
    MidViewForm.pack(side=RIGHT)
    
    lbl_text = Label(TopViewForm, text="Bank Management System", font=('verdana', 18), width=600,bg="#1C2833",fg="white")
    lbl_text.pack(fill=X)

    Label(LFrom, text="Name  ", font=("Arial", 12)).pack(side=TOP)
    Entry(LFrom,font=("Arial",10,"bold"),textvariable=name).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Contact ", font=("Arial", 12)).pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"),textvariable=contact).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Email ", font=("Arial", 12)).pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"),textvariable=email).pack(side=TOP, padx=10, fill=X)
    Label(LFrom, text="Branch ", font=("Arial", 12)).pack(side=TOP)
    Entry(LFrom, font=("Arial", 10, "bold"),textvariable=branch).pack(side=TOP, padx=10, fill=X)
    Button(LFrom,text="Submit",font=("Arial", 10, "bold"),command=register).pack(side=TOP, padx=10,pady=5, fill=X)

    lbl_txtsearch = Label(LeftViewForm, text="Enter name to Search", font=('verdana', 10),bg="gray")
    lbl_txtsearch.pack()

    search = Entry(LeftViewForm, textvariable=SEARCH, font=('verdana', 15), width=10)
    search.pack(side=TOP, padx=10, fill=X)
    
    btn_search = Button(LeftViewForm, text="Search", command=SearchRecord)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
    
    btn_view = Button(LeftViewForm, text="View All", command=DisplayData)
    btn_view.pack(side=TOP, padx=10, pady=10, fill=X)
    
    btn_reset = Button(LeftViewForm, text="Reset", command=Reset)
    btn_reset.pack(side=TOP, padx=10, pady=10, fill=X)
    
    btn_delete = Button(LeftViewForm, text="Delete", command=Delete)
    btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
   
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    tree = ttk.Treeview(MidViewForm,columns=("Account_No", "Name", "Contact", "Email","Branch"),
                        selectmode="extended", height=100, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)

    tree.heading('Account_No', text="Account_No", anchor=W)
    tree.heading('Name', text="Name", anchor=W)
    tree.heading('Contact', text="Contact", anchor=W)
    tree.heading('Email', text="Email", anchor=W)
    tree.heading('Branch', text="Branch", anchor=W)

    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=100)
    tree.column('#2', stretch=NO, minwidth=0, width=150)
    tree.column('#3', stretch=NO, minwidth=0, width=80)
    tree.column('#4', stretch=NO, minwidth=0, width=120)
    tree.pack()
    DisplayData()

def register():
    Database()
    name1=name.get()
    con1=contact.get()
    email1=email.get()
    branch1=branch.get()
    if name1=='' or con1==''or email1=='' or branch1=='':
        tkMessageBox.showinfo("Warning","fill the empty field!!!")
    else:
        conn.execute('INSERT INTO BANK_REGISTRATION (NAME,CONTACT,EMAIL,BRANCH) \
              VALUES (?,?,?,?)',(name1,con1,email1,branch1));
        conn.commit()
        tkMessageBox.showinfo("Message","Stored successfully")
        DisplayData()
        conn.close()

def Reset():
    tree.delete(*tree.get_children())
    DisplayData()
    SEARCH.set("")
    name.set("")
    contact.set("")
    email.set("")
    branch.set("")

def Delete():
    Database()
    if not tree.selection():
        tkMessageBox.showwarning("Warning","Select data to delete")
    else:
        result = tkMessageBox.askquestion('Confirm', 'Are you sure you want to delete this record?',
                                          icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            cursor=conn.execute("DELETE FROM BANK_REGISTRATION WHERE ACCOUNT_NO = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()

def SearchRecord():
    Database()
    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        cursor=conn.execute("SELECT * FROM BANK_REGISTRATION WHERE NAME LIKE ?", ('%' + str(SEARCH.get()) + '%',))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        
def DisplayData():
    Database()
    tree.delete(*tree.get_children())
    cursor=conn.execute("SELECT * FROM BANK_REGISTRATION")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

DisplayForm()
if __name__=='__main__':
 mainloop()
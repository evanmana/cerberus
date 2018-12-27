from tkinter import *
from tkinter.ttk import Treeview
import addNewServiceForm
import sqlite3

conn = sqlite3.connect('cerberus.db')
try:
    conn = sqlite3.connect('cerberus.db')
except sqlite3.Error as e:
    print(e)


def exitApp(event):
    master.destroy()

def secretKeys(event):
    kp = (event.char)
    print(kp)
    if kp =="0":
        tv.pack(fill=BOTH, expand=1)


def getAddNewServiceForm():
    master.withdraw()
    addNewServiceForm.main(master)

def LoadTable():
    cur = conn.cursor()
    cur.execute("SELECT name, email, username, password, value FROM service")

    rows = cur.fetchall()

    i=1
    for row in rows:
        if (i % 2) == 0:
            tag="oddrow"
        else:
            tag="evenrow"
        tv.insert('', 'end', text=row[0], values=(row[1],
                         row[2],row[3],row[4]),tags = tag)
        i=i+1

master = Tk()
master.title('Cerberus Beta')
master.geometry("860x400")
master.resizable(0, 0)

menubar = Menu(master)
filemenu = Menu(menubar, tearoff=0)

menubar.add_cascade(label="Cerberus", menu=filemenu)
filemenu.add_command(label="Εισαγωγή Υπηρεσίας", command=getAddNewServiceForm)
filemenu.add_command(label="Έξοδος", command=master.quit)

settingsMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Ρυθμίσεις", menu=settingsMenu)

aboutMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Σχετικά", menu=aboutMenu)

master.config(menu=menubar)

tv = Treeview()
tv['columns'] = ('email', 'username', 'passwd', 'id')

tv.heading('#0', text='Service', anchor='w')
tv.column('#0', anchor="w",  width=120)

tv.heading('email', text='Email')
tv.column('email', anchor='center', width=200)

tv.heading('username', text='Username')
tv.column('username', anchor='center', width=100)

tv.heading('passwd', text='Password')
tv.column('passwd', anchor='center', width=100)

tv.heading('id', text='ID')
tv.column('id', anchor='center', width=100)

tv.pack(fill=BOTH, expand=1)
tv.tag_configure('oddrow', background='thistle')
tv.tag_configure('evenrow', background='pink')

tv.pack_forget()
LoadTable()


master.bind("<Escape>", exitApp)
master.bind("<Key>", secretKeys)
mainloop( )

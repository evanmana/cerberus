from tkinter import *
import addNewServiceForm
import sqlite3

conn = sqlite3.connect('cerberus.db')
c = conn.cursor()

for row in c.execute('SELECT * FROM service'):
    print(row)


def exitApp(event):
    master.destroy()

def secretKeys(event):
    kp = (event.char)
    print(kp)

def getAddNewServiceForm():
    master.withdraw()
    addNewServiceForm.main(master)


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


master.bind("<Escape>", exitApp)
master.bind("<Key>", secretKeys)
mainloop( )

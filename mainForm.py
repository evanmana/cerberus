from tkinter import *
import addNewServiceForm
import sqlite3
conn = sqlite3.connect('cerberus.db')


def exitApp(event):
    master.destroy()

def secretKeys(event):
    kp = (event.char)
    kp.replace('s', '')
    print("Pressed:  "+kp)


master = Tk()
master.title('Cerberus Beta')
master.geometry("860x400")
master.resizable(0, 0)

menubar = Menu(master)
filemenu = Menu(menubar, tearoff=0)

menubar.add_cascade(label="Cerberus", menu=filemenu)
filemenu.add_command(label="Εισαγωγή Υπηρεσίας", command=addNewServiceForm.main)
filemenu.add_command(label="Έξοδος", command=master.quit)

settingsMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Ρυθμίσεις", menu=settingsMenu)

aboutMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Σχετικά", menu=aboutMenu)

master.config(menu=menubar)


master.bind("<Escape>", exitApp)
master.bind("<Key>", secretKeys)
mainloop( )

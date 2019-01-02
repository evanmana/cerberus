from tkinter import *
from tkinter.ttk import Treeview
import sqlite3
from cryptography.fernet import Fernet


class cerberus:
    def __init__(self, master):
        self.master = master
        self.master.title('Cerberus Beta')
        self.master.geometry("860x400")
        self.master.resizable(0, 0)

        self.menubar = Menu(master)
        filemenu = Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label="Cerberus", menu=filemenu)
        filemenu.add_command(label="Εισαγωγή Υπηρεσίας", command=self.getAddNewServiceForm)
        filemenu.add_command(label="Έξοδος", command=master.quit)

        settingsMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Ρυθμίσεις", menu=settingsMenu)

        aboutMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Σχετικά", menu=aboutMenu)

        self.master.config(menu=self.menubar)

        self.search = StringVar()
        self.search.trace("w", lambda name, index, mode, sv=self.search: self.callback())
        searchEntry = Entry(master, textvariable=self.search)
        searchEntry.pack(pady=5, padx= 20, fill=X)

        self.table = Treeview()
        self.table['columns'] = ('email', 'username', 'passwd', 'id')

        self.table.heading('#0', text='Service', anchor='w')
        self.table.column('#0', anchor="w",  width=120)

        self.table.heading('email', text='Email')
        self.table.column('email', anchor='center', width=200)

        self.table.heading('username', text='Username')
        self.table.column('username', anchor='center', width=100)

        self.table.heading('passwd', text='Password')
        self.table.column('passwd', anchor='center', width=100)

        self.table.heading('id', text='ID')
        self.table.column('id', anchor='center', width=100)

        self.table.tag_configure('oddrow', background='#e6eef2')
        self.table.tag_configure('evenrow', background='#b3cfdd')
        self.table.focus()

        self.loadTable()
        #table.pack_forget()

        self.master.bind("<Escape>", self.exitApp)
        self.master.bind("<Key>", self.secretKeys)

    def callback(self):
        print(self.search.get())
        return True

    def exitApp(self, event):
        self.master.destroy()

    def secretKeys(self, event):
        kp = (event.char)
        print(kp)
        if kp =="0":
            for i in self.table.get_children():
                self.table.delete(i)

            self.loadTable()
            self.table.pack(fill=BOTH, expand=1)


    def getAddNewServiceForm(self):
        self.master.withdraw()
        import addNewServiceForm
        addNewServiceForm.addNewServiceForm(self.master)

    def loadTable(self):
        key =b''
        cipher_suite = Fernet(key)

        try:
            conn = sqlite3.connect('cerberus.db')
        except sqlite3.Error as e:
            print(e)

        cur = conn.cursor()
        cur.execute("SELECT name, email, username, password, value FROM service ")

        rows = cur.fetchall()

        i=1
        for row in rows:
            if (i % 2) == 0:
                tag="oddrow"
            else:
                tag="evenrow"


            self.table.insert('', 'end', text=cipher_suite.decrypt(row[0]).decode("utf-8"),
                              values=(cipher_suite.decrypt(row[1]).decode("utf-8"),
                             cipher_suite.decrypt(row[2]).decode("utf-8"),cipher_suite.decrypt(row[3]).decode("utf-8"),cipher_suite.decrypt(row[4]).decode("utf-8")),tags = tag)
            i=i+1
        conn.close()

def a():
    App.loadTable()


if __name__ == "__main__":
    import platform
    print(platform.system())
    root = Tk()
    App = cerberus(root)
    a()
    root.mainloop()



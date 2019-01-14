from tkinter import *
from tkinter.ttk import Treeview
import sqlite3
import keyring
from cryptography.fernet import Fernet
import webbrowser


class cerberus:
    def __init__(self, master):
        self.runAppFirstTime()

        self.key = keyring.get_password("cerberus", "admin")
        self.cipher_suite = Fernet(self.key)

        self.master = master
        self.master.title('Cerberus Beta')
        windowWidth = self.master.winfo_reqwidth()
        windowHeight = self.master.winfo_reqheight()
        positionRight = int(self.master.winfo_screenwidth()/3 - windowWidth/3)
        positionDown = int(self.master.winfo_screenheight()/5 - windowHeight/5)
        self.master.geometry("860x400+{}+{}".format(positionRight, positionDown))

        self.master.resizable(0, 0)

        self.menubar = Menu(master)
        filemenu = Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label="Cerberus", menu=filemenu)
        filemenu.add_command(label="Εισαγωγή Υπηρεσίας", command=self.getAddNewServiceForm)
        filemenu.add_command(label="Επεξεργασία Υπηρεσίας")
        filemenu.add_command(label="Έξοδος", command=master.quit)

        settingsMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Ρυθμίσεις", menu=settingsMenu)

        aboutMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Σχετικά", menu=aboutMenu)

        self.master.config(menu=self.menubar)

        self.search = StringVar()
        self.search.trace("w", lambda name, index, mode, sv=self.search: self.searchService())
        searchEntry = Entry(master, textvariable=self.search)
        searchEntry.pack(pady=5, padx= 20, fill=X)

        self.table = Treeview()
        self.table['columns'] = ('email', 'username', 'passwd', 'id', 'url')

        self.table.heading('#0', text='Service', anchor='w')
        self.table.column('#0', anchor="w",  width=125)

        self.table.heading('email', text='Email')
        self.table.column('email', anchor='center', width=200)

        self.table.heading('username', text='Username')
        self.table.column('username', anchor='center', width=100)

        self.table.heading('passwd', text='Password')
        self.table.column('passwd', anchor='center', width=100)

        self.table.heading('url', text='URL')
        self.table.column('url', anchor='center', width=120)

        self.table.heading('id', text='ID')
        self.table.column('id', anchor='center', width=100)

        self.table.tag_configure('oddrow', background='#e6eef2')
        self.table.tag_configure('evenrow', background='#b3cfdd')
        self.table.tag_configure('focus', background='#c6b6b4')
        self.last_focus = None
        self.last_focus_tag = None
        self.table.focus()
        self.table.pack(fill=BOTH, expand=1)
        self.table.bind("<<TreeviewSelect>>", self.onTableSelect)
        self.table.bind("<ButtonRelease-1>", self.openURLService)
        self.table.bind("<Motion>", self.changePointerOnHover)
        self.table.bind("<Leave>", self.onLeaveTable)

        self.loadTable()

        self.master.bind("<Escape>", self.exitApp)
        self.master.bind("<Key>", self.secretKeys)

    def onLeaveTable(self, event):
        if self.table.winfo_ismapped():
            self.table.item(self.last_focus, tags=[self.last_focus_tag])
            self.last_focus = None

    def changePointerOnHover(self, event):
        _iid = self.table.identify_row(event.y)

        if _iid != self.last_focus:
            if self.last_focus:
                self.table.item(self.last_focus, tags=[self.last_focus_tag])

            self.last_focus_tag = self.table.item(_iid, "tag")
            self.table.item(_iid, tags=['focus'])
            self.last_focus = _iid

        curItem = self.table.item(self.table.identify('item', event.x, event.y))
        if curItem['values'] != '':
            col = self.table.identify_column(event.x)
            url = curItem['values'][int(col[-1])-1]

            if col[-1]=="5" and url !='---':
                self.master.config(cursor="hand2")
            else:
                self.master.config(cursor="")

    def openURLService(self, event):
        curItem = self.table.item(self.table.focus())
        col = self.table.identify_column(event.x)

        if col[-1] == "5":
            url = curItem['values'][int(col[-1])-1]
            if url != '---':
                webbrowser.open_new_tab('http://'+url)


    def onTableSelect(self, event):
        for item in self.table.selection():
            item_text = self.table.item(item,"text")
            print(item_text)

    def runAppFirstTime(self):
        if keyring.get_password("cerberus", "admin") == None:
            key = Fernet.generate_key()
            keyring.set_password("cerberus", "admin", key)

    def searchService(self):
        print(self.search.get())

        try:
            conn = sqlite3.connect('cerberus.db')
        except sqlite3.Error as e:
            print(e)

        cur = conn.cursor()
        if self.search.get()!='':
            cur.execute("SELECT name, email, username, password, value, url FROM service WHERE name LIKE '%"+self.search.get()+"%' or name LIKE '%"+self.search.get().upper()+"%'") #('%'+self.search.get()+'%',),'Α')

        rows = cur.fetchall()
        cur.close()


        for k in self.table.get_children():
                self.table.delete(k)

        i=1
        for row in rows:
            if (i % 2) == 0:
                tag = "oddrow"
            else:
                tag = "evenrow"


            self.table.insert('', 'end', text=row[0],
                              values=(self.cipher_suite.decrypt(row[1]).decode("utf-8"),
                             self.cipher_suite.decrypt(row[2]).decode("utf-8"),self.cipher_suite.decrypt(row[3]).decode("utf-8"),self.cipher_suite.decrypt(row[4]).decode("utf-8"),row[5]),tags = tag)
            i=i+1

    def exitApp(self, event):
        self.master.destroy()

    def secretKeys(self, event):
        kp = (event.char)
        if kp =="0":
            if self.table.winfo_ismapped()==True:
                self.table.pack_forget()
            else:
                self.table.pack(fill=BOTH, expand=1)


    def getAddNewServiceForm(self):
        self.master.withdraw()
        import addNewServiceForm
        addNewServiceForm.addNewServiceForm(self.master)

    def loadTable(self):
        try:
            conn = sqlite3.connect('cerberus.db')
        except sqlite3.Error as e:
            print(e)

        cur = conn.cursor()
        cur.execute("SELECT name, email, username, password, value, url value FROM service ")

        rows = cur.fetchall()

        i=1
        for row in rows:
            if (i % 2) == 0:
                tag="oddrow"
            else:
                tag="evenrow"

            self.table.insert('', 'end', text=row[0],
                              values=(self.cipher_suite.decrypt(row[1]).decode("utf-8"),
                                      self.cipher_suite.decrypt(row[2]).decode("utf-8"),
                                      self.cipher_suite.decrypt(row[3]).decode("utf-8"),
                                      self.cipher_suite.decrypt(row[4]).decode("utf-8"),
                                      row[5]),
                              tags = tag )
            i = i+1

        conn.close()


def a():
    App.loadTable()


if __name__ == "__main__":
    import platform
    print(platform.system())

    root = Tk()
    App = cerberus(root)

    root.mainloop()

from tkinter import *
from tkinter.ttk import Treeview
from tkinter import ttk
import sqlite3
import keyring
from cryptography.fernet import Fernet
import webbrowser


class Cerberus:
    def __init__(self, master):
        self.runAppFirstTime()

        self.key = keyring.get_password("cerberus", "admin")
        self.cipher_suite = Fernet(self.key)

        self.master = master
        self.master.title('Cerberus Beta')
        windowWidth = self.master.winfo_reqwidth()
        windowHeight = self.master.winfo_reqheight()
        positionRight = int(self.master.winfo_screenwidth() / 3 - windowWidth / 3)
        positionDown = int(self.master.winfo_screenheight() / 5 - windowHeight / 5)
        self.master.geometry("1060x450+{}+{}".format(positionRight, positionDown))

        self.master.resizable(0, 0)

        self.menubar = Menu(master)
        filemenu = Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label="Cerberus", menu=filemenu)
        filemenu.add_command(label="Εισαγωγή Υπηρεσίας", command=self.getAddNewServiceForm)
        filemenu.add_command(label="Επεξεργασία Υπηρεσίας", command=self.getEditServiceForm)
        filemenu.add_command(label="Έξοδος", command=master.quit)

        settingsMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Ρυθμίσεις", menu=settingsMenu)

        aboutMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Σχετικά", menu=aboutMenu)

        self.master.config(menu=self.menubar)

        self.search = StringVar()
        self.search.trace("w", lambda name, index, mode, sv=self.search: self.searchService())
        searchEntry = Entry(master, textvariable=self.search)
        searchEntry.pack(pady=5, padx=20, fill=X)

        # Fix BUG with Treeview colors in Python3.7
        def fixed_map(option):
            # Fix for setting text colour for Tkinter 8.6.9
            # From: https://core.tcl.tk/tk/info/509cafafae
            #
            # Returns the style map for 'option' with any styles starting with
            # ('!disabled', '!selected', ...) filtered out.

            # style.map() returns an empty list for missing options, so this
            # should be future-safe.
            return [elm for elm in style.map('Treeview', query_opt=option) if
                    elm[:2] != ('!disabled', '!selected')]

        style = ttk.Style(root)
        style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
        # Fix BUG with Treeview colors in Python3.7

        self.table = Treeview()
        self.table['show'] = 'headings'
        self.table['columns'] = ('Services','email', 'username', 'passwd', 'id', 'category', 'url')

        for col in self.table['columns'] :
            self.table.heading(col, command=lambda c=col: self.sortby(self.table, c, 0))

        self.table.heading('Services', text='Services')
        self.table.column('Services', anchor='center', width=200)

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

        self.table.heading('category', text='Category')
        self.table.column('category', anchor='center', width=100)

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

        self.loadTable()

        self.master.bind("<Escape>", self.exitApp)

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
            url = curItem['values'][int(col[-1]) - 1]

            if col[-1] == "6" and url != '---':
                self.master.config(cursor="hand2")
            else:
                self.master.config(cursor="")

    def openURLService(self, event):
        curItem = self.table.item(self.table.focus())
        col = self.table.identify_column(event.x)
        region = self.table.identify("region", event.x, event.y)

        if col[-1] == "6" and region != 'heading':
            url = curItem['values'][int(col[-1]) - 1]
            if url != '---':
                webbrowser.open_new_tab('http://' + str(url))

    def onTableSelect(self, event):
        for item in self.table.selection():
            item_text = self.table.item(item, "values")
            print(item_text[0])

    def getSelectedService(self, event):
        for item in self.table.selection():
            selectedRow = self.table.item(item, "value")
            return selectedRow

    def runAppFirstTime(self):
        if keyring.get_password("cerberus", "admin") is None:
            key = Fernet.generate_key()
            keyring.set_password("cerberus", "admin", key)

    def searchService(self):
        try:
            conn = sqlite3.connect('cerberus.db')
        except sqlite3.Error as e:
            print(e)

        cur = conn.cursor()
        if self.search.get() != '':
            cur.execute(
                "SELECT name, email, username, password, value, category, url FROM service WHERE name LIKE '%" + self.search.get() + "%' or name LIKE '%" + self.search.get().upper() + "%'")  # ('%'+self.search.get()+'%',),'Α')
        elif not self.search.get():
            cur.execute(
                "SELECT name, email, username, password, value, category, url FROM service ")

        rows = cur.fetchall()
        cur.close()

        for k in self.table.get_children():
            self.table.delete(k)

        i = 1
        for row in rows:
            if (i % 2) == 0:
                tag = "oddrow"
            else:
                tag = "evenrow"

            self.table.insert('', 'end',
                              values=(row[0],
                                      self.cipher_suite.decrypt(row[1]).decode("utf-8"),
                                      self.cipher_suite.decrypt(row[2]).decode("utf-8"),
                                      self.cipher_suite.decrypt(row[3]).decode("utf-8"),
                                      self.cipher_suite.decrypt(row[4]).decode("utf-8"),
                                      row[5],
                                      row[6]), tags=tag)
            i = i + 1

    def exitApp(self, event):
        self.master.destroy()

    def getAddNewServiceForm(self):
        self.master.withdraw()
        import addNewServiceForm
        addNewServiceForm.addNewServiceForm(self.master)

    def getEditServiceForm(self):
        service = self.getSelectedService(self)

        if service is None:
            from tkinter import messagebox
            messagebox.showerror("Μήνυμα Σφάλματος", "Παρακαλώ επιλέξτε την Υπηρεσία που θέλετε να Επεξεργαστείτε.")
        else:
            self.master.withdraw()
            import editServiceForm
            editServiceForm.editServiceForm(self.master, service)

    def sortby(self, tree, col, descending):
        """sort tree contents when a column header is clicked on"""
        # grab values to sort
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        # if the data to be sorted is numeric change to float

        # now sort the data in place
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        # switch the heading so that it will sort in the opposite direction
        tree.heading(col,
                     command=lambda col=col: self.sortby(tree, col, int(not descending)))

    def loadTable(self):
        try:
            conn = sqlite3.connect('cerberus.db')
        except sqlite3.Error as e:
            print(e)

        cur = conn.cursor()
        cur.execute("SELECT name, email, username, password, value, category, url value FROM service ")

        rows = cur.fetchall()

        for row in self.table.get_children():
            self.table.delete(row)

        i = 1
        for row in rows:
            if (i % 2) == 0:
                tag = "oddrow"
            else:
                tag = "evenrow"

            self.table.insert('', 'end',
                              values=(row[0],self.cipher_suite.decrypt(row[1]).decode("utf-8"),
                                      self.cipher_suite.decrypt(row[2]).decode("utf-8"),
                                      self.cipher_suite.decrypt(row[3]).decode("utf-8"),
                                      self.cipher_suite.decrypt(row[4]).decode("utf-8"),
                                      row[5],
                                      row[6]), tags=tag)
            i = i + 1

        conn.close()


if __name__ == "__main__":
    import platform
    print(platform.system())

    root = Tk()
    App = Cerberus(root)
    root.mainloop()



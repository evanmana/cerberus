from pathlib import Path
from tkinter import *
from tkinter.ttk import Treeview
from tkinter import ttk
import sqlite3
from cryptography.fernet import Fernet
import webbrowser
from tkinter import messagebox
from tkinter import filedialog
import csv


class Cerberus:
    def getAppIcon(self):
        appIcon = """
                iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAADXSURB
                VDhPrdJNDsFQFIbhEiSY+R34mYhNiD2IJYglkLAEAyEGxA6YifXYhBgxEN6vjqSR9LZNfMkT5xzt7c1tvYhkTeLksMUdD+xsFju64YUjDlbvESsF6Iaz331y
                gmZFv4uRC8af0s8ImkUmgwm03TUWZmWzKZyHWoO26lJHaKq4Qhfq9PvoWa3ZDXpIaH4X6KJjdeIFZIhBoI9c4PcMniY4c56B3sIMS7Mx334O51tIoQTtpGK/
                wVr/OZNGE220UDaqNWtAD3FGn7IEP1vVmuX97n/xvDdpfjuRn6jN2AAAAABJRU5ErkJggg==
                """
        return appIcon

    def getSearchIcon(self):
        searchIcon = '''
                        iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQA
                        AAD4SURBVDhPtZK9TsMwFIUzsLAVxF51Dh1SBpZKDKAYFNshW9nasR1AQmKhZeBn6dL36QPxBjwAn6WjDHWJsASfdBWdc32Pb6Jk/0pd1/1Qkr+n
                        qqoL59wbw4+hrLUvPMdqd8OgoVYMHMsKgTd4a+pK1n442OO2D8mW4DN8Tu+1LMsj2THe+0sO3UlGhF7nFjTJ8E4yggDLNreSMbz3KSEPkhGE39Mf
                        Su6HS545eCbZws0jekvJn9EHeydkFjZqmiZncIr31PkBd2HomuEFIfMQSE3USoetBgR8GWNOZKXDRltqI5kOG4Qf6ZM6lJUOr5IXRXEg+Rdk2Tea
                        80eK5t/XLAAAAABJRU5ErkJggg==
                        '''
        return searchIcon

    def __init__(self, master):
        self.versionApp, self.key = self.initApp()

        self.cipher_suite = Fernet(self.key)

        self.master = master
        self.master.title('Cerberus {}'.format(self.versionApp))
        windowWidth = 1060
        windowHeight = 450
        screenWidth = self.master.winfo_screenwidth()
        screenHeight = self.master.winfo_screenheight()
        positionRight = int(screenWidth / 2 - windowWidth / 2)
        positionDown = int(screenHeight / 3 - windowHeight / 2)
        self.master.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, positionRight, positionDown))

        img = PhotoImage(data=self.getAppIcon())
        root.wm_iconphoto(True, img)

        self.master.resizable(0, 0)

        self.menubar = Menu(master)
        filemenu = Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label="Cerberus", menu=filemenu)
        filemenu.add_command(label="Εισαγωγή Υπηρεσίας", command=self.getAddNewServiceForm)
        filemenu.add_command(label="Επεξεργασία Υπηρεσίας", command=self.getEditServiceForm)
        filemenu.add_command(label="Διαγραφή Υπηρεσίας", command=self.deleteService)
        filemenu.add_separator()
        filemenu.add_command(label="Εξαγωγή σε Excel", command=self.exportToCSV)
        filemenu.add_separator()
        filemenu.add_command(label="Έξοδος", command=self.exitApp)

        settingsMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Ρυθμίσεις", menu=settingsMenu)

        aboutMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Σχετικά", menu=aboutMenu)

        self.master.config(menu=self.menubar)

        self.popup = Menu(root, tearoff=0)
        self.popup.add_command(label="Επεξεργασία Υπηρεσίας", command=self.getEditServiceForm)
        self.popup.add_command(label="Διαγραφή Υπηρεσίας", command=self.deleteService)
        self.popup.add_separator()
        self.popup.add_command(label="Έξοδος", command=self.exitApp)

        self.frame = Frame(background="white", borderwidth=1, relief="sunken",
                           highlightthickness=1)
        self.frame.pack(side="top", fill="x", padx=4, pady=4)

        self.search = StringVar()

        self.searchEntry = Entry(self.frame, textvariable=self.search, borderwidth=0, highlightthickness=0,
                                 background="white")
        self.searchEntry.insert(0, 'Αναζήτηση Υπηρεσίας')
        self.searchEntry['fg'] = 'grey'
        self.search.trace("w", lambda name, index, mode, sv=self.search: self.searchService())

        self.searchEntry.image = PhotoImage(data=self.getSearchIcon())
        imageLabel = Label(self.frame, image=self.searchEntry.image)
        imageLabel.pack(side="left")
        imageLabel['bg'] = 'white'

        self.searchEntry.pack(side="left", fill="both", expand=True)

        # Fix BUG with Treeview colors in Python3.7
        def fixed_map(option):
            return [elm for elm in style.map('Treeview', query_opt=option) if
                    elm[:2] != ('!disabled', '!selected')]

        style = ttk.Style(root)
        style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
        # Fix BUG with Treeview colors in Python3.7

        self.table = Treeview()
        self.table['show'] = 'headings'
        self.table['columns'] = ('Services', 'email', 'username', 'passwd', 'id', 'category', 'url')

        for col in self.table['columns']:
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
        self.table.bind("<Button-3>", self.popupMenu)
        self.searchEntry.bind("<FocusIn>", self.foc_in)
        self.searchEntry.bind("<FocusOut>", self.foc_out)

        self.loadTable(self)

        self.master.bind("<Escape>", self.exitApp)

    def foc_in(self, *args):
        if self.search.get() == 'Αναζήτηση Υπηρεσίας':
            self.searchEntry.delete('0', 'end')
            self.searchEntry['fg'] = 'black'

    def foc_out(self, *args):
        if not self.search.get():
            self.searchEntry.insert(0, 'Αναζήτηση Υπηρεσίας')
            self.searchEntry['fg'] = 'grey'
            self.loadTable(self)

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

            if col[-1] == "7" and url != '---':
                self.master.config(cursor="hand2")
            else:
                self.master.config(cursor="")

    def openURLService(self, event):
        curItem = self.table.item(self.table.focus())
        col = self.table.identify_column(event.x)
        region = self.table.identify("region", event.x, event.y)

        if col[-1] == "7" and region != 'heading':
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

    def initApp(self):
        print("Initialize Cerberus App")
        try:
            conn = sqlite3.connect('cerberus.db')
        except sqlite3.Error as e:
            print(e)

        cur = conn.cursor()
        cur.execute(
            "SELECT version, masterToken FROM cerberusParameters")
        row = cur.fetchone()
        cur.close()

        return row

    @staticmethod
    def getMasterToken():
        try:
            conn = sqlite3.connect('cerberus.db')
        except sqlite3.Error as e:
            print(e)

        cur = conn.cursor()
        cur.execute(
            "SELECT  masterToken FROM cerberusParameters")
        masterToken = cur.fetchone()
        cur.close()

        return masterToken[0]

    def searchService(self):
        try:
            conn = sqlite3.connect('cerberus.db')
        except sqlite3.Error as e:
            print(e)

        cur = conn.cursor()

        if self.search.get() == 'Αναζήτηση Υπηρεσίας':
            pass
        elif self.search.get():
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

    def exitApp(self, event=None):
        self.master.destroy()

    def getAddNewServiceForm(self):
        self.master.withdraw()
        import addNewServiceForm
        addNewServiceForm.addNewServiceForm(self)

    def getEditServiceForm(self):
        service = self.getSelectedService(self)

        if service is None:
            messagebox.showerror("Μήνυμα Σφάλματος", "Παρακαλώ επιλέξτε την Υπηρεσία που θέλετε να Επεξεργαστείτε.")
        else:
            self.master.withdraw()
            import editServiceForm
            editServiceForm.editServiceForm(self, service)

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

    @staticmethod
    def loadTable(self):
        try:
            conn = sqlite3.connect('cerberus.db')
        except sqlite3.Error as e:
            print(e)

        cur = conn.cursor()
        cur.execute("SELECT name, email, username, password, value, category, url value FROM service")

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
                              values=(row[0], self.cipher_suite.decrypt(row[1]).decode("utf-8"),
                                      self.cipher_suite.decrypt(row[2]).decode("utf-8"),
                                      self.cipher_suite.decrypt(row[3]).decode("utf-8"),
                                      self.cipher_suite.decrypt(row[4]).decode("utf-8"),
                                      row[5],
                                      row[6]), tags=tag)
            i = i + 1

        conn.close()

        self.last_focus = None
        self.table.selection()

    def deleteService(self):
        service = self.getSelectedService(self)

        if service is None:
            messagebox.showerror("Μήνυμα Σφάλματος", "Παρακαλώ επιλέξτε την Υπηρεσία που θέλετε να Διαγράξετε.")
        else:
            msgBox = messagebox.askquestion('Διαγραφή: {}'.format(service[0]),
                                            'Είστε σίγουρος ότι θέλετε να διαγράψετε την Υπηρεσία: ''{}'' ?'.format(
                                                service[0]),
                                            icon='warning')
            if msgBox == 'yes':
                try:
                    conn = sqlite3.connect('cerberus.db')
                except sqlite3.Error as e:
                    print(e)
                sql = 'DELETE FROM service WHERE name=?'
                cur = conn.cursor()
                cur.execute(sql, (service[0],))
                conn.commit()
                conn.close()
                self.loadTable(self)

    def popupMenu(self, event):
        serviceId = self.table.identify_row(event.y)

        if serviceId:
            self.table.selection_set(serviceId)
            try:
                self.popup.tk_popup(event.x_root, event.y_root)
            finally:
                self.popup.grab_release()

    def exportToCSV(self):
        try:
            conn = sqlite3.connect('cerberus.db')
        except sqlite3.Error as e:
            print(e)

        cur = conn.cursor()
        cur.execute("SELECT category, name, email, username, password, value, url value FROM service")

        rows = cur.fetchall()

        csvData = [['Κατηγορία', 'Υπηρεσία', 'Email', 'Όνομα Χρήστη', 'Κωδικός', 'ID', 'URL', ]]

        for row in rows:
            csvData = csvData + [[row[0],
                                  row[1],
                                  self.cipher_suite.decrypt(row[2]).decode("utf-8"),
                                  self.cipher_suite.decrypt(row[3]).decode("utf-8"),
                                  self.cipher_suite.decrypt(row[4]).decode("utf-8"),
                                  self.cipher_suite.decrypt(row[5]).decode("utf-8"),
                                  row[6]
                                  ]]

        try:
            homeFolder = str(Path.home())
            filePath = filedialog.asksaveasfile(initialdir=homeFolder,
                                                initialfile='cerberus.csv',
                                                title="Επιλογή Αρχείου",
                                                filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
            if filePath:
                try:
                    with open(filePath.name, 'w') as csvFile:
                        csvFile = csv.writer(csvFile, delimiter='\t')
                        csvFile.writerows(csvData)
                    messagebox.showinfo("Μήνυμα Σφάλματος",
                                        "Το αρχείο αποθηκέυτηκε με Επιτυχία στην τοποθεσία {}.".format(filePath.name))
                except Exception as e:
                    messagebox.showerror("Μήνυμα Σφάλματος", "Δεν ήταν δυνατή η Εξαγωγή του αρχείου.")
        except Exception as e:
            print(e)
            messagebox.showerror("Μήνυμα Σφάλματος", "Δεν ήταν δυνατή η Εξαγωγή του αρχείου.")


if __name__ == "__main__":
    import platform

    print(platform.system())
    root = Tk()
    App = Cerberus(root)
    root.mainloop()

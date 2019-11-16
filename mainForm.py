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
    @staticmethod
    def getAppIcon():
        appIcon = """
                iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAADXSURB
                VDhPrdJNDsFQFIbhEiSY+R34mYhNiD2IJYglkLAEAyEGxA6YifXYhBgxEN6vjqSR9LZNfMkT5xzt7c1tvYhkTeLksMUdD+xsFju64YUjDlbvESsF6Iaz331y
                gmZFv4uRC8af0s8ImkUmgwm03TUWZmWzKZyHWoO26lJHaKq4Qhfq9PvoWa3ZDXpIaH4X6KJjdeIFZIhBoI9c4PcMniY4c56B3sIMS7Mx334O51tIoQTtpGK/
                wVr/OZNGE220UDaqNWtAD3FGn7IEP1vVmuX97n/xvDdpfjuRn6jN2AAAAABJRU5ErkJggg==
                """
        return appIcon

    @staticmethod
    def getSearchIcon():
        searchIcon = '''
                        iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQA
                        AAD4SURBVDhPtZK9TsMwFIUzsLAVxF51Dh1SBpZKDKAYFNshW9nasR1AQmKhZeBn6dL36QPxBjwAn6WjDHWJsASfdBWdc32Pb6Jk/0pd1/1Qkr+n
                        qqoL59wbw4+hrLUvPMdqd8OgoVYMHMsKgTd4a+pK1n442OO2D8mW4DN8Tu+1LMsj2THe+0sO3UlGhF7nFjTJ8E4yggDLNreSMbz3KSEPkhGE39Mf
                        Su6HS545eCbZws0jekvJn9EHeydkFjZqmiZncIr31PkBd2HomuEFIfMQSE3USoetBgR8GWNOZKXDRltqI5kOG4Qf6ZM6lJUOr5IXRXEg+Rdk2Tea
                        80eK5t/XLAAAAABJRU5ErkJggg==
                        '''
        return searchIcon

    @staticmethod
    def getAddIcon():
        addIcon = '''
                    iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAABmJLR0QA/wD/AP+gvaeTAAAAOElEQVQokWNgoBJwgGIMwEQtDTgByRoYcTgBxj6AJHaAgYHhAMk24AINUIwBaO9pZjxyD6CYMgAA6/MG0do6pCsAAAAASUVORK5CYII=
                    '''
        return addIcon

    @staticmethod
    def getEditIcon():
        editIcon = '''
                    iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAABmJLR0QA/wD/AP+gvaeTAAAAXElEQVQokcXNoQ2AQBBE0ZeAowLqoRE6AYlDUAF90AVFUMZhViHuDkGYZLLmz18+yIylFu5wIsVQWzD3GHDEKAun6BafquCE6R94fMBzDn7as+YmbosLO9aS/VVuPnQeCUPPWjYAAAAASUVORK5CYII=
                    '''
        return editIcon

    @staticmethod
    def getDeleteIcon():
        deleteIcon = '''
                    iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAABmJLR0QA/wD/AP+gvaeTAAAAoUlEQVQokb2OMQ6CUBBEZ792xuPA7+GfhCBBg17GQoKJJ+ECxuPgTyyQsTCEFX+r0+3szO4D/ibvbOGTOP/ykzj3zhbjbNSup6Du0minjmQU1AOGxejJ7EtGsiF4MGIeJBsK9+v2dgoWptJwhgAEKh2eI02Sdzqkj4JCqkTMRijHzkXbYNM7m93TuNeBkKc/LIUoNfOqvV6EKA3MMwz4C70A3ZVMHzoSQQYAAAAASUVORK5CYII=
                    '''
        return deleteIcon

    @staticmethod
    def getInfoIcon():
        infoIcon = '''
                   iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAABmJLR0QA/wD/AP+gvaeTAAAARElEQVQokWNgoAJQYWBguAPFKuiSTFg0+DMwMChDsR+xNtxmYGC4BdVEffAfit+QowkDYPM0XkB7DYxYxNDdjk0N8QAA5qgK0QnW7YsAAAAASUVORK5CYII=
                    '''
        return infoIcon

    @staticmethod
    def getExcelIcon():
        excelIcon = '''
                    iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAABmJLR0QA/wD/AP+gvaeTAAABK0lEQVQokZWRzUoCYRSGn+8bhcaigSgHjLDctLAfaycULdsU0RXUtpuIghZdQRfQBURBqzYtIoIgs3TaBGqGxczYQmgGQfRrUQ1jBeG7fM95zjmcF3qU+Gmkd7JDWqc5JzrCuNvLHf0JzG7PLysltkBlgCSAFtUeEjOJw6BRifPT9ePrCICCLKi18KSBWP+YqZv7ZiyO1/IoNcq7wCcAMD6cZDWzQr6aR4/q3NsFzYzFmR6ewvYdSo0yAPIbqNSfSI2k2FzY4OLxkj5N1+JfQMqYCDbL0BVoUhKREaTosrsUnJQeTXNTyVF9e2ZpcpHcy23b8R0K9SK27/wGrJqFVbOCgmEMtm3fgXoRr+V1AwKuFOIk/Nb3pvfqeu6B67kAKKnOghzC+i+4nvUBGuFnrHFS+BMAAAAASUVORK5CYII=
                     '''
        return excelIcon

    @staticmethod
    def getExitIcon():
        exitIcon = '''
                    iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAABmJLR0QA/wD/AP+gvaeTAAAArElEQVQokZXRsWpCQRCF4S96A1fQwpR5Fe0E7Wyt0ljapAxok8rKUmx9DQvtfIe8QkCwsggoIc1c0ORuLh447MDOP3OW5U49xPmEMeqJvgvWOBYNrxjigEaJB2hhnwWQY4v3X5OfY8gsemT+1zSgD5xTQBedqD/xgj4WKSBHO+rH8HdxWQZsw7DEJiKBWsUb5hgV+a83fKGHtwTYwY7bj5ugmQBOWOFYkeivfgCGpRoLVq8K4wAAAABJRU5ErkJggg==
                     '''
        return exitIcon

    @staticmethod
    def getSettingscon():
        settingsIcon = '''
                    iVBORw0KGgoAAAANSUhEUgAAAAwAAAAMCAYAAABWdVznAAAABmJLR0QA/wD/AP+gvaeTAAAAdUlEQVQoka3RTQqCABQE4I8O0An0HIG30OyKeYJ05cVEqM0rXoKl4MBshpn3ywGoMAerX8YaF4x4BsfQ6qX5lkxrbOEUgSaFHyhQYkj6NXc4Y4pKRdLL0KbwfDrsRpdm7RcjvfV7DrT+L/21AzvPmrH5cZvwAiTzLK0qoOjqAAAAAElFTkSuQmCC
                     '''
        return settingsIcon

    def __init__(self, master, root):
        self.versionApp, self.key = self.initApp()

        self.cipher_suite = Fernet(self.key)

        self.master = master
        self.master.title('Cerberus {}'.format(self.versionApp))
        self.windowWidth = 1060
        self.windowHeight = 450
        self.screenWidth = self.master.winfo_screenwidth()
        self.screenHeight = self.master.winfo_screenheight()
        self.positionRight = int(self.screenWidth / 2 - self.windowWidth / 2)
        self.positionDown = int(self.screenHeight / 3 - self.windowHeight / 2)
        self.master.geometry(
            "{}x{}+{}+{}".format(self.windowWidth, self.windowHeight, self.positionRight, self.positionDown))

        self.img = PhotoImage(data=self.getAppIcon())
        self.master.wm_iconphoto(True, self.img)

        self.master.resizable(0, 0)

        self.menubar = Menu(master)
        filemenu = Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label="Cerberus", menu=filemenu)
        self.addIcon = PhotoImage(data=self.getAddIcon())
        filemenu.add_command(label="Εισαγωγή Υπηρεσίας", image=self.addIcon, compound='left',
                             command=self.getAddNewServiceForm)
        self.editIcon = PhotoImage(data=self.getEditIcon())
        filemenu.add_command(label="Επεξεργασία Υπηρεσίας", image=self.editIcon, compound='left',
                             command=self.getEditServiceForm)
        self.deleteIcon = PhotoImage(data=self.getDeleteIcon())
        filemenu.add_command(label="Διαγραφή Υπηρεσίας", image=self.deleteIcon, compound='left',
                             command=self.deleteService)
        filemenu.add_separator()
        self.excelIcon = PhotoImage(data=self.getExcelIcon())
        filemenu.add_command(label="Εξαγωγή σε Excel", image=self.excelIcon, compound='left', command=self.exportToCSV)
        filemenu.add_separator()
        self.exitIcon = PhotoImage(data=self.getExitIcon())
        filemenu.add_command(label="Έξοδος", image=self.exitIcon, compound='left', command=self.exitApp)

        settingsMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Ρυθμίσεις", menu=settingsMenu)
        self.settingsIcon = PhotoImage(data=self.getSettingscon())
        settingsMenu.add_command(label="Αλλαγή κωδικού", image=self.settingsIcon, compound='left')

        aboutMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Βοήθεια", menu=aboutMenu)
        self.infoIcon = PhotoImage(data=self.getInfoIcon())
        aboutMenu.add_command(label="Περί", image=self.infoIcon, compound='left', command=self.getAboutAppForm)

        self.master.config(menu=self.menubar)

        self.popup = Menu(root, tearoff=0)
        self.popup.add_command(label="Επεξεργασία Υπηρεσίας", image=self.editIcon, compound='left', command=self.getEditServiceForm)
        self.popup.add_command(label="Διαγραφή Υπηρεσίας", image=self.deleteIcon, compound='left', command=self.deleteService)
        self.popup.add_separator()
        self.popup.add_command(label="Έξοδος", image=self.exitIcon, compound='left', command=self.exitApp)

        self.frame = Frame(self.master, background="white", borderwidth=1, relief="sunken",
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

        self.table = Treeview(self.master)
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
        self.master.protocol("WM_DELETE_WINDOW", self.exitApp)

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

    @staticmethod
    def exitApp(event=None):
        root.destroy()

    @staticmethod
    def getAboutAppForm():
        print('asd')
        import aboutApp
        aboutApp.aboutApp()

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
                     command=lambda x=col: self.sortby(tree, col, int(not descending)))

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
        cur.execute("SELECT masterToken FROM cerberusParameters")
        masterToken = cur.fetchone()

        # TODO
        passwd = 'YUaMl3PfzNvyJLzlbPzVCb78wcobfLjhcXgACw9rvkk='

        if masterToken[0] == passwd:
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
                        messagebox.showinfo("Μήνυμα Επιτυχίας",
                                            "Το αρχείο αποθηκέυτηκε με Επιτυχία στην τοποθεσία {}.".format(
                                                filePath.name))
                    except Exception as e:
                        messagebox.showerror("Μήνυμα Σφάλματος", "Δεν ήταν δυνατή η Εξαγωγή του αρχείου.")
            except Exception as e:
                print(e)
                messagebox.showerror("Μήνυμα Σφάλματος", "Δεν ήταν δυνατή η Εξαγωγή του αρχείου.")


if __name__ == "__main__":
    import platform

    print(platform.system())


    def check_password(failures=[]):
        try:
            conn = sqlite3.connect('cerberus.db')
        except sqlite3.Error as e:
            print(e)

        cur = conn.cursor()
        cur.execute(
            "SELECT masterToken FROM cerberusParameters")
        row = cur.fetchone()
        cur.close()
        print(row[0])
        if entry.get() == row[0]:
            print('Logged in')
            root.withdraw()
            master = Toplevel()
            App = Cerberus(master, root)

        failures.append(1)
        if sum(failures) >= 3:
            root.destroy()
            raise SystemExit('Unauthorized login attempt')
        else:
            entry.delete(0, 'end')
            root.title('Λάθος Κωδικός, παρακαλώ δοκιμάστε ξανά. Προσπάθεια %i/%i' % (sum(failures) + 1, 3))


    def exitApp():
        root.destroy()


    def sendPasswdToEmail():
        import sendEmail
        print("asda")
        sendEmail.sendEmail()

    root = Tk()
    windowWidth = 720
    windowHeight = 150
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    positionRight = int(screenWidth / 2 - windowWidth / 2)
    positionDown = int(screenHeight / 3 - windowHeight / 2)
    root.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, positionRight, positionDown))

    img = PhotoImage(data=Cerberus.getAppIcon())
    root.wm_iconphoto(True, img)

    root.title('Εισαγωγή Κωδικού')

    parent = Frame(root, padx=10, pady=10)
    parent.pack(fill=BOTH, expand=True)

    Label(parent, text="Παρακαλώ εισάγεται τον Κωδικό σας:").pack(side=TOP)
    entry = Entry(parent, show="*", )
    entry.pack(side=TOP, pady=(0, 15), fill=BOTH)

    b = Button(parent, borderwidth=1, text="Είσοδος", width=10, pady=8, command=check_password)
    b.pack(pady="7")

    forgotPasswdLbl = Label(parent, text='Ξεχάσατε τον Κωδικό σας?', font=(None, 8), fg='blue')
    forgotPasswdLbl.pack()

    forgotPasswdLbl.bind("<Button-1>", lambda x: sendPasswdToEmail())
    forgotPasswdLbl.bind("<Motion>", forgotPasswdLbl.config(cursor="hand2"))
    entry.bind('<Return>', lambda x: check_password())
    root.bind("<Escape>", lambda x: exitApp())
    entry.focus_set()
    root.resizable(0, 0)
    root.mainloop()

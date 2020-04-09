from pathlib import Path
from tkinter import *
from tkinter.ttk import Treeview
from tkinter import ttk
import sqlite3
import webbrowser
from tkinter import messagebox
from tkinter import filedialog
import csv
from cryptography.fernet import Fernet
import icons
import cerberusCryptography


class Cerberus:
    def __init__(self, master, root):
        self.exportToCSV = False
        self.versionApp, self.key, self.salt = self.initApp()

        self.key = cerberusCryptography.getMasterKey()
        self.cipher_suite = Fernet(self.key)

        self.master = master
        self.master.title('Cerberus')
        self.windowWidth = 1060
        self.windowHeight = 450
        self.screenWidth = self.master.winfo_screenwidth()
        self.screenHeight = self.master.winfo_screenheight()
        self.positionRight = int(self.screenWidth / 2 - self.windowWidth / 2)
        self.positionDown = int(self.screenHeight / 3 - self.windowHeight / 2)
        self.master.geometry(
            "{}x{}+{}+{}".format(self.windowWidth, self.windowHeight, self.positionRight, self.positionDown))

        self.img = PhotoImage(data=icons.getAppIcon())
        self.master.wm_iconphoto(True, self.img)

        self.master.resizable(0, 0)

        self.menubar = Menu(master)
        filemenu = Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(label="Cerberus", menu=filemenu)
        self.addIcon = PhotoImage(data=icons.getAddIcon())
        filemenu.add_command(label="Εισαγωγή Υπηρεσίας", image=self.addIcon, compound='left',
                             command=self.getAddNewServiceForm)
        self.editIcon = PhotoImage(data=icons.getEditIcon())
        filemenu.add_command(label="Επεξεργασία Υπηρεσίας", image=self.editIcon, compound='left',
                             command=self.getEditServiceForm)
        self.deleteIcon = PhotoImage(data=icons.getDeleteIcon())
        filemenu.add_command(label="Διαγραφή Υπηρεσίας", image=self.deleteIcon, compound='left',
                             command=self.deleteService)
        filemenu.add_separator()
        self.excelIcon = PhotoImage(data=icons.getExcelIcon())
        filemenu.add_command(label="Εξαγωγή σε Excel", image=self.excelIcon, compound='left',
                             command=self.checkPasswordToExportToCSV)
        filemenu.add_separator()
        self.exitIcon = PhotoImage(data=icons.getExitIcon())
        filemenu.add_command(label="Έξοδος", image=self.exitIcon, compound='left', command=self.exitApp)

        settingsMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Ρυθμίσεις", menu=settingsMenu)
        self.settingsIcon = PhotoImage(data=icons.getSettingsIcon())
        settingsMenu.add_command(label="Επεξεργασία Στοιχείων", image=self.settingsIcon, compound='left')
                                 #command=self.getSettingsForm)

        aboutMenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Βοήθεια", menu=aboutMenu)
        self.infoIcon = PhotoImage(data=icons.getInfoIcon())
        aboutMenu.add_command(label="Περί", image=self.infoIcon, compound='left', command=self.getAboutAppForm)

        self.master.config(menu=self.menubar)

        self.copyIcon = PhotoImage(data=icons.getCopyIcon())
        self.popup = Menu(root, tearoff=0)
        self.popup.add_command(label=" Αντιγραφή Email", image=self.copyIcon, compound='left',
                               command=self.copyEmail)
        self.popup.add_command(label=" Αντιγραφή Username", image=self.copyIcon, compound='left',
                               command=self.copyUsername)
        self.popup.add_command(label=" Αντιγραφή Κωδικού", image=self.copyIcon, compound='left',
                               command=self.copyPasswd)
        self.popup.add_command(label=" Αντιγραφή ID", image=self.copyIcon, compound='left',
                               command=self.copyID)
        self.popup.add_separator()
        self.popup.add_command(label=" Επεξεργασία Υπηρεσίας", image=self.editIcon, compound='left',
                               command=self.getEditServiceForm)
        self.popup.add_command(label=" Διαγραφή Υπηρεσίας", image=self.deleteIcon, compound='left',
                               command=self.deleteService)
        self.popup.add_separator()
        self.popup.add_command(label=" Έξοδος", image=self.exitIcon, compound='left', command=self.exitApp)

        self.frame = Frame(self.master, background="white", borderwidth=1, relief="sunken",
                           highlightthickness=1)
        self.frame.pack(side="top", fill="x", padx=4, pady=4)

        self.search = StringVar()

        self.searchEntry = Entry(self.frame, textvariable=self.search, borderwidth=0, highlightthickness=0,
                                 background="white")
        self.searchEntry.insert(0, 'Αναζήτηση Υπηρεσίας')
        self.searchEntry['fg'] = 'grey'
        self.search.trace("w", lambda name, index, mode, sv=self.search: self.searchService())

        self.searchEntry.image = PhotoImage(data=icons.getSearchIcon())
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
        self.table['columns'] = ('Services', 'email', 'username', 'passwd', 'id', 'category', 'url', 'ID')
        self.table["displaycolumns"] = ('Services', 'email', 'username', 'passwd', 'id', 'category', 'url')

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

        self.table.heading('ID', text='ID')
        self.table.column('ID', anchor='center', width=200)

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
        self.popup.bind("<FocusOut>", self.popupFocusOut)
        self.master.protocol("WM_DELETE_WINDOW", self.exitApp)

        self.loadTable(self)

        self.master.bind("<Escape>", self.exitApp)

    def popupFocusOut(self, event=None):
        self.popup.unpost()

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
            "SELECT version, masterToken, salt FROM cerberusParameters")
        row = cur.fetchone()
        cur.close()

        return row

    def copyEmail(self):
        for item in self.table.selection():
            item_text = self.table.item(item, "values")
            self.master.clipboard_clear()
            root.clipboard_append(item_text[1])

    def copyUsername(self):
        for item in self.table.selection():
            item_text = self.table.item(item, "values")
            self.master.clipboard_clear()
            root.clipboard_append(item_text[2])

    def copyPasswd(self):
        for item in self.table.selection():
            item_text = self.table.item(item, "values")
            self.master.clipboard_clear()
            root.clipboard_append(item_text[3])

    def copyID(self):
        for item in self.table.selection():
            item_text = self.table.item(item, "values")
            self.master.clipboard_clear()
            root.clipboard_append(item_text[4])

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
                "SELECT id, name, email, username, password, value, category, url FROM service WHERE name LIKE '%" + self.search.get() + "%' or name LIKE '%" + self.search.get().upper() + "%'")  # ('%'+self.search.get()+'%',),'Α')
        elif not self.search.get():
            cur.execute(
                "SELECT id, name, email, username, password, value, category, url FROM service ")

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
                              values=(row[1],
                                      self.cipher_suite.decrypt(row[2]).decode("utf-8").split(),
                                      self.cipher_suite.decrypt(row[3]).decode("utf-8").split(),
                                      self.cipher_suite.decrypt(row[4]).decode("utf-8").split(),
                                      self.cipher_suite.decrypt(row[5]).decode("utf-8").split(),
                                      self.cipher_suite.decrypt(row[6]).decode("utf-8").split(),
                                      self.cipher_suite.decrypt(row[7]).decode("utf-8").split(),
                                      row[0]),
                              tags=tag)
            i = i + 1

    @staticmethod
    def exitApp(event=None):
        root.destroy()

    @staticmethod
    def getAboutAppForm():
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

    def getSettingsForm(self):
        import settingsForm
        settingsForm.settingsForm()

    def sortby(self, tree, col, descending):
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            if (ix % 2) == 0:
                tag = "evenrow"
            else:
                tag = "oddrow"
            tree.move(item[1], '', ix)
            tree.item(item[1], tags=tag)
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
        cur.execute("SELECT id, name, email, username, password, value, category, url value FROM service")

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
                              values=(row[1],
                                      self.cipher_suite.decrypt(row[2]).decode("utf-8").split(),
                                      self.cipher_suite.decrypt(row[3]).decode("utf-8").split(),
                                      self.cipher_suite.decrypt(row[4]).decode("utf-8").split(),
                                      self.cipher_suite.decrypt(row[5]).decode("utf-8").split(),
                                      self.cipher_suite.decrypt(row[6]).decode("utf-8").split(),
                                      self.cipher_suite.decrypt(row[7]).decode("utf-8").split(),
                                      row[0]),
                              tags=tag)

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
                sql = 'DELETE FROM service WHERE id=?'
                cur = conn.cursor()
                cur.execute(sql, (service[-1],))
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

    def checkPasswordToExportToCSV(self):
        print("Check Password..")
        import logInForm
        self.master.withdraw()
        logInForm.logIn(self)

    @staticmethod
    def exportToCSV():
        print("Export Services to CSV...")
        try:
            conn = sqlite3.connect('cerberus.db')
        except sqlite3.Error as e:
            print(e)

        key = cerberusCryptography.getMasterKey()
        cipher_suite = Fernet(key)

        cur = conn.cursor()
        cur.execute("SELECT category, name, email, username, password, value, url value FROM service")

        rows = cur.fetchall()

        csvData = [['Κατηγορία', 'Υπηρεσία', 'Email', 'Όνομα Χρήστη', 'Κωδικός', 'ID', 'URL', ]]

        for row in rows:
            csvData = csvData + [[cipher_suite.decrypt(row[0]).decode("utf-8").split(),
                                  cipher_suite.decrypt(row[1]).decode("utf-8").split(),
                                  cipher_suite.decrypt(row[2]).decode("utf-8").split(),
                                  cipher_suite.decrypt(row[3]).decode("utf-8").split(),
                                  cipher_suite.decrypt(row[4]).decode("utf-8").split(),
                                  cipher_suite.decrypt(row[5]).decode("utf-8").split(),
                                  cipher_suite.decrypt(row[6]).decode("utf-8").split(),
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


def check_password(failures=[1]):
    try:
        conn = sqlite3.connect('cerberus.db')
    except sqlite3.Error as e:
        print(e)

    cur = conn.cursor()
    cur.execute(
        "SELECT masterToken, salt FROM cerberusParameters")
    row = cur.fetchone()
    cur.close()

    salt = row[1]
    import cerberusCryptography
    cerberusCryptography.salt = salt
    cerberusCryptography.password = entry.get()
    password = cerberusCryptography.decrypt(row[0])

    if entry.get() == password:
        failures.clear()
        print('Logged in')
        root.withdraw()
        master = Toplevel()
        Cerberus(master, root)

    failures.append(1)
    if sum(failures) > 3:
        root.destroy()
        raise SystemExit('Unauthorized login attempt')
    else:
        entry.delete(0, 'end')
        root.title('Λάθος Κωδικός, παρακαλώ δοκιμάστε ξανά. Προσπάθεια %i/%i' % (sum(failures), 3))


def exitApp():
    root.destroy()


def sendPasswdToEmail():
    import sendEmail
    sendEmail.sendEmail()


root = Tk()
windowWidth = 720
windowHeight = 300
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
positionRight = int(screenWidth / 2 - windowWidth / 2)
positionDown = int(screenHeight / 3 - windowHeight / 2)
root.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, positionRight, positionDown))

img = PhotoImage(data=icons.getAppIcon())
root.wm_iconphoto(True, img)
root.wait_visibility(root)
root.wm_attributes('-alpha', 0.98)
root.title('Cerberus - Εισαγωγή Κωδικού')

welcomeFrame = Frame(root, height=130, bg='#1e1e2f')
welcomeFrame.pack(side="top", fill=BOTH)

appIcon = PhotoImage(data=icons.getLogoIcon())
panel = Label(root, image=appIcon, bg='#1e1e2f').place(x=20, y=20)
Label(welcomeFrame, text="Καλώς ορίσατε στον", font=("Comic Sans MS", 32), fg='white', bg='#1e1e2f').place(x=110,
                                                                                                           y=20)
Label(welcomeFrame, text="Cerberus", font=("Helvetica", 32), fg='#d9ddff', bg='#1e1e2f').place(x=380, y=72)

parent = Frame(root, bg='lightgrey')
parent.pack(side="top", fill=BOTH, expand=True)

Label(parent, text="Παρακαλώ εισάγεται τον Κωδικό σας:", bg='lightgrey').pack(pady=(25, 0), side=TOP)
entry = Entry(parent, show="*", width=40)
entry.pack(side=TOP, pady=(0, 15))

enterIcon = PhotoImage(data=icons.getEnterIcon())
b = Button(parent, borderwidth=1, text="Είσοδος", image=enterIcon, compound=LEFT, pady=8, width=120,
           command=check_password)
b.pack(pady="7")

forgotPasswdLbl = Label(parent, text='Ξεχάσατε τον Κωδικό σας?', font=(None, 8), fg='blue', bg='lightgrey')
forgotPasswdLbl.pack()

forgotPasswdLbl.bind("<Button-1>", lambda x: sendPasswdToEmail())
forgotPasswdLbl.bind("<Motion>", forgotPasswdLbl.config(cursor="hand2"))
entry.bind('<Return>', lambda x: check_password())
root.bind("<Escape>", lambda x: exitApp())
entry.focus_set()
root.resizable(0, 0)
root.mainloop()

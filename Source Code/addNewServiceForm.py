from tkinter import *
import sqlite3
from tkinter.ttk import Combobox
from cryptography.fernet import Fernet

import categoriesList
import cerberusCryptography
import mainForm
import icons


def addNewServiceForm(self):
    try:
        conn = sqlite3.connect('cerberus.db')
    except sqlite3.Error as e:
        print(e)

    def onDestory(event=NONE):
        master.destroy()
        self.master.deiconify()
        self.master.lift()
        self.master.focus_force()
        self.master.grab_set()
        mainForm.Cerberus.loadTable(self)

    def insertNewService(event=NONE):
        key = cerberusCryptography.getMasterKey()
        cipher_suite = Fernet(key)

        if eCategory.get() != '':
            category = eCategory.get()
        else:
            category = '---'

        if eService.get() != '':
            name = eService.get()
        else:
            name = '---'

        if eServiceUrl.get() != '':
            serviceUrl = eServiceUrl.get()
        else:
            serviceUrl = '---'

        if eEmail.get() != '':
            email = eEmail.get()
        else:
            email = '---'

        if eUsername.get() != '':
            username = eUsername.get()
        else:
            username = '---'

        if ePassword.get() != '':
            password = ePassword.get()
        else:
            password = '---'

        if eValue.get() != '':
            value = eValue.get()
        else:
            value = '---'

        email = cipher_suite.encrypt(bytes(email, encoding="UTF-8"))
        username = cipher_suite.encrypt(bytes(username, encoding="UTF-8"))
        password = cipher_suite.encrypt(bytes(password, encoding="UTF-8"))
        value = cipher_suite.encrypt(bytes(value, encoding="UTF-8"))
        category = cipher_suite.encrypt(bytes(category, encoding="UTF-8"))
        serviceUrl = cipher_suite.encrypt(bytes(serviceUrl, encoding="UTF-8"))

        cursor = conn.cursor()
        try:
            cursor.execute('''INSERT INTO service(name, email, username, password, value, category, url)
                  VALUES(?,?,?,?,?,?,?)''', (name, email, username, password, value, category, serviceUrl))
            conn.commit()
            conn.close()
            onDestory()
        except sqlite3.IntegrityError as e:
            from tkinter import messagebox
            messagebox.showerror("Μήνυμα Σφάλματος", "Η Υπηρεσία υπάρχει ήδη.")

    master = Toplevel()
    windowWidth = 385
    windowHeight = 280
    screenWidth = master.winfo_screenwidth()
    screenHeight = master.winfo_screenheight()
    positionRight = int(screenWidth / 2 - windowWidth / 2)
    positionDown = int(screenHeight / 3 - windowHeight / 2)
    master.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, positionRight, positionDown))
    master.lift()
    master.focus_force()
    master.grab_set()

    master.title('Cerberus - Εισαγωγή Νέας Υπηρεσίας')
    img = PhotoImage(data=icons.getAppIcon())
    master.wm_iconphoto(True, img)
    master.resizable(0, 0)

    Label(master, text="Κατηγορία:").grid(row=0, sticky="W", padx=5, pady=5)
    Label(master, text="Υπηρεσία:").grid(row=1, sticky="W", padx=5, pady=5)
    Label(master, text="URL:").grid(row=2, sticky="W", padx=5, pady=5)
    Label(master, text="Email:").grid(row=3, sticky="W", padx=5, pady=5)
    Label(master, text="Username:").grid(row=4, sticky="W", padx=5, pady=5)
    Label(master, text="Password:").grid(row=5, sticky="W", padx=5, pady=5)
    Label(master, text="ID:").grid(row=6, sticky="W", padx=5, pady=5)

    categoryExamples = ["Προσωπικά Στοιχεία", "Κοινωνική Δικτύωση", "Email", "Banking"]
    categories = categoriesList.getCategoriesList()
    for cat in categories:
        if cat not in categoryExamples:
            categoryExamples.append(cat)

    eCategory = Combobox(master, width=33, values=categoryExamples)

    eCategory.focus()
    eService = Entry(master, width=35)
    eServiceUrl = Entry(master, width=35)
    eEmail = Entry(master, width=35)
    eUsername = Entry(master, width=35)
    ePassword = Entry(master, width=35)
    eValue = Entry(master, width=35)

    eCategory.grid(row=0, column=1, pady=5, padx=5)
    eService.grid(row=1, column=1, pady=5, padx=5)
    eServiceUrl.grid(row=2, column=1, pady=5, padx=5)
    eEmail.grid(row=3, column=1, pady=5, padx=5)
    eUsername.grid(row=4, column=1, pady=5, padx=5)
    ePassword.grid(row=5, column=1, pady=5, padx=5)
    eValue.grid(row=6, column=1, pady=5, padx=5)

    enterButton = Button(master, text="Εισαγωγή Στοιχείων", command=insertNewService)
    enterButton.grid(row=7, column=0, columnspan=2, sticky="we", padx=5, pady=5)

    master.bind("<Escape>", onDestory)
    master.bind("<Return>", insertNewService)
    master.protocol("WM_DELETE_WINDOW", onDestory)

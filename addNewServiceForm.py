from tkinter import *
import sqlite3
from tkinter.ttk import Combobox
from cryptography.fernet import Fernet
import mainForm


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
        key = mainForm.Cerberus.getMasterToken()
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
    windowWidth = master.winfo_reqwidth()
    windowHeight = master.winfo_reqheight()
    positionRight = int(master.winfo_screenwidth() / 2 - windowWidth / 2)
    positionDown = int(master.winfo_screenheight() / 5 - windowHeight / 5)
    master.geometry("+{}+{}".format(positionRight, positionDown))
    master.lift()
    master.focus_force()
    master.grab_set()

    master.title('Εισαγωγή Νέας Υπηρεσίας')
    master.resizable(0, 0)

    Label(master, text="Κατηγορία:").grid(row=0, sticky="W", padx=5, pady=5)
    Label(master, text="Υπηρεσία:").grid(row=1, sticky="W", padx=5, pady=5)
    Label(master, text="URL:").grid(row=2, sticky="W", padx=5, pady=5)
    Label(master, text="Email:").grid(row=3, sticky="W", padx=5, pady=5)
    Label(master, text="Username:").grid(row=4, sticky="W", padx=5, pady=5)
    Label(master, text="Password:").grid(row=5, sticky="W", padx=5, pady=5)
    Label(master, text="ID:").grid(row=6, sticky="W", padx=5, pady=5)

    cursor = conn.cursor()
    cursor.execute(
        "SELECT distinct category FROM service where category<>'Προσωπικά Στοιχεία' and category<>'Κοινωνική Δικτύωση' and category<>'Email' and category<>'Banking' and category<>'Άλλο' ")
    rows = cursor.fetchall()
    cursor.close()

    eCategory = Combobox(master, width=33,
                         values=("Προσωπικά Στοιχεία", "Κοινωνική Δικτύωση", "Email", "Banking", "Άλλο"))
    for row in rows:
        eCategory['values'] = eCategory['values'] + row

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
    mainloop()

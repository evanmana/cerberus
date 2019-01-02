from tkinter import *
import sqlite3
from tkinter.ttk import Combobox

from cryptography.fernet import Fernet


def addNewServiceForm(root):
    conn = sqlite3.connect('cerberus.db')
    try:
        conn = sqlite3.connect('cerberus.db')
    except sqlite3.Error as e:
        print(e)

    def exitForm(event=NONE):
        onDestory()

    def onDestory():
        master.destroy()
        root.deiconify()

    def insertNewService(event=NONE):
        key =b''
        cipher_suite = Fernet(key)

        if (eCategory.get()!=''):
            category=eCategory.get()
        else:
            category='---'

        if (eService.get() !=''):
            name=eService.get()
        else:
            name='---'

        if (eEmail.get()!=''):
            email=eEmail.get()
        else:
            email='---'

        if (eUsername.get()!=''):
            username=eUsername.get()
        else:
            username='---'

        if (ePassword.get()!=''):
            password=ePassword.get()
        else:
            password='---'

        if (eValue.get()!=''):
            value=eValue.get()
        else:
            value='---'

        name = cipher_suite.encrypt(bytes(name, encoding="UTF-8"))
        email = cipher_suite.encrypt(bytes(email, encoding="UTF-8"))
        username = cipher_suite.encrypt(bytes(username, encoding="UTF-8"))
        password = cipher_suite.encrypt(bytes(password, encoding="UTF-8"))
        value = cipher_suite.encrypt(bytes(value, encoding="UTF-8"))

        cursor = conn.cursor()
        cursor.execute('''INSERT INTO service(name, email, username, password, value, category)
                  VALUES(?,?,?,?,?,?)''', (name, email, username, password, value, category))
        conn.commit()
        conn.close()
        exitForm()

    master = Toplevel()
    master.lift()
    master.focus_force()
    master.grab_set()

    master.title('Εισαγωγή Νέας Υπηρεσίας')
    master.resizable(0, 0)

    Label(master, text="Κατηγορία:").grid(row=0, sticky="W", padx=5, pady=5)
    Label(master, text="Υπηρεσία:").grid(row=1, sticky="W", padx=5, pady=5)
    Label(master, text="Email:").grid(row=2, sticky="W", padx=5, pady=5)
    Label(master, text="Username:").grid(row=3, sticky="W", padx=5, pady=5)
    Label(master, text="Password:").grid(row=4, sticky="W", padx=5, pady=5)
    Label(master, text="ID:").grid(row=5, sticky="W", padx=5, pady=5)

    cursor = conn.cursor()
    cursor.execute("SELECT distinct category FROM service where category<>'Προσωπικά Στοιχεία' and category<>'Κοινωνική Δικτύωση' and category<>'Email' and category<>'Banking' and category<>'Άλλο' ")
    rows = cursor.fetchall()
    cursor.close()

    eCategory = Combobox(master, width=33, values=("Προσωπικά Στοιχεία", "Κοινωνική Δικτύωση", "Email", "Banking", "Άλλο"))
    for row in rows:
        eCategory['values'] = eCategory['values']+row

    eCategory.focus()
    eService = Entry(master, width=35)
    eEmail = Entry(master, width=35)
    eUsername = Entry(master, width=35)
    ePassword = Entry(master, width=35)
    eValue = Entry(master, width=35)

    eCategory.grid(row=0, column=1, pady=5, padx=5)
    eService.grid(row=1, column=1, pady=5, padx=5)
    eEmail.grid(row=2, column=1, pady=5, padx=5)
    eUsername.grid(row=3, column=1, pady=5, padx=5)
    ePassword.grid(row=4, column=1, pady=5, padx=5)
    eValue.grid(row=5, column=1, pady=5, padx=5)

    enterButton = Button(master, text="Εισαγωγή Στοιχείων", command=insertNewService)
    enterButton.grid(row=6, column=0, columnspan=2, sticky="we", padx=5, pady=5)


    master.bind("<Escape>", exitForm)
    master.bind("<Return>", insertNewService)
    master.protocol("WM_DELETE_WINDOW", onDestory)
    mainloop( )

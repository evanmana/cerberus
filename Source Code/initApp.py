from datetime import date
from tkinter import *
from tkinter import messagebox as msgBox
import sqlite3
import icons
import cerberusCryptography


def exitForm():
    root.destroy()


def insertEmailAndPasswdToDB():
    today = date.today()
    primaryEmail = entryEmail.get()
    password = entryPasswd.get()
    password1 = entryPasswd1.get()
    print(primaryEmail)
    print(password)
    print(password1)

    if primaryEmail == "" or password == "" or password1 == "":
        msgBox.showerror("Μήνυμα Σφάλματος", "Παρακαλώ συμπληρώστε όλα τα πεδία.")
        return None

    if password != password1:
        msgBox.showerror("Μήνυμα Σφάλματος", "Οι δύο κωδικοί δεν ταιριάζουν. Παρακαλώ εισάγεται τους ξανα.")
        entryPasswd.delete(0, 'end')
        entryPasswd1.delete(0, 'end')
        entryPasswd.config(highlightcolor='red', highlightbackground='red')
        entryPasswd1.config(highlightcolor='red', highlightbackground='red')
        entryPasswd.focus_set()
    else:
        print("Insert to db...")
        salt, key = cerberusCryptography.createNewPassword(password)
        cerberusCryptography.salt = salt
        cerberusCryptography.password = password
        encryptedKey = cerberusCryptography.encrypt(key)
        primaryEmail = cerberusCryptography.encrypt(primaryEmail)
        today = cerberusCryptography.encrypt(today.strftime("%m/%d/%Y"))

        print(salt)
        print(key)
        print(encryptedKey)

        try:
            conn = sqlite3.connect('cerberus.db')
        except sqlite3.Error as e:
            print(e)

        cursor = conn.cursor()
        try:
            cursor.execute('''INSERT INTO cerberusParameters(primaryEmail, masterToken, salt, passwdLastUpdate)
                          VALUES(?,?,?,?)''', (primaryEmail, encryptedKey, salt, today))
            conn.commit()
            conn.close()
            exitForm()
            import mainForm
        except sqlite3.IntegrityError as e:
            from tkinter import messagebox
            messagebox.showerror("Μήνυμα Σφάλματος", "Κάτι πήγε στραβά.. Παρακαλώ προσπαθήστε ξανά.")


root = Tk()
windowWidth = 650
windowHeight = 440
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
positionRight = int(screenWidth / 2 - windowWidth / 2)
positionDown = int(screenHeight / 3 - windowHeight / 2)
root.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, positionRight, positionDown))

img = PhotoImage(data=icons.getAppIcon())
root.wm_iconphoto(True, img)
root.wait_visibility(root)
root.wm_attributes('-alpha', 0.98)
root.title('Cerberus - Δημιουργία Λογαριασμού')

welcomeFrame = Frame(root, height=130, bg='#1e1e2f')
welcomeFrame.pack(side="top", fill=BOTH)

appIcon = PhotoImage(data=icons.getLogoIcon())
panel = Label(root, image=appIcon, bg='#1e1e2f').place(x=20, y=20)
Label(welcomeFrame, text="Καλώς ορίσατε στον", font=("Comic Sans MS", 32), fg='white', bg='#1e1e2f').place(x=110, y=25)
Label(welcomeFrame, text="Cerberus", font=("Helvetica", 32), fg='#d9ddff', bg='#1e1e2f').place(x=380, y=72)

parent = Frame(root, bg='lightgrey')
parent.pack(side="top", fill=BOTH, expand=True)

Label(parent, text="Παρακαλώ εισάγεται το Email σας:", bg='lightgrey').pack(pady=(25, 0), side=TOP)
entryEmail = Entry(parent, width=40)
entryEmail.pack(side=TOP, pady=(0, 7))

Label(parent, text="Παρακαλώ εισάγεται τον νέο σας Κωδικό:", bg='lightgrey').pack(pady=(25, 0), side=TOP)
entryPasswd = Entry(parent, show="*", width=40)
entryPasswd.pack(side=TOP, pady=(0, 5))

Label(parent, text="Παρακαλώ εισάγεται ξανά τον νέο σας Κωδικό:", bg='lightgrey').pack(pady=(25, 0), side=TOP)
entryPasswd1 = Entry(parent, show="*", width=40)
entryPasswd1.pack(side=TOP, pady=(0, 25))

enterIcon = PhotoImage(data=icons.getEnterIcon())
okBtn = Button(parent, borderwidth=1, text="Είσοδος", image=enterIcon, compound=LEFT, pady=8, width=120,
               command=insertEmailAndPasswdToDB)
okBtn.pack()

root.bind('<Return>', lambda x: insertEmailAndPasswdToDB())
root.bind('<Escape>', lambda x: exitForm())
entryEmail.focus_set()
root.resizable(0, 0)
root.mainloop()

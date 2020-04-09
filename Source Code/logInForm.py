import sqlite3
from tkinter import *
import icons
import mainForm


def logIn(self):
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
            onDestroy()
            mainForm.Cerberus.exportToCSV()
        else:
            failures.append(1)
            if sum(failures) > 3:
                master.destroy()
                raise SystemExit('Unauthorized login attempt')
            else:
                entry.delete(0, 'end')
                master.title('Λάθος Κωδικός, παρακαλώ δοκιμάστε ξανά. Προσπάθεια %i/%i' % (sum(failures), 3))

    def onDestroy():
        master.destroy()
        self.master.deiconify()
        self.master.lift()
        self.master.focus_force()
        self.master.grab_set()

    master = Toplevel()
    windowWidth = 720
    windowHeight = 280
    screenWidth = master.winfo_screenwidth()
    screenHeight = master.winfo_screenheight()
    positionRight = int(screenWidth / 2 - windowWidth / 2)
    positionDown = int(screenHeight / 3 - windowHeight / 2)
    master.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, positionRight, positionDown))
    master.lift()
    master.focus_force()
    master.grab_set()

    img = PhotoImage(data=icons.getAppIcon())
    master.wm_iconphoto(True, img)
    master.wait_visibility(master)
    master.wm_attributes('-alpha', 0.98)
    master.title('Cerberus - Εισαγωγή Κωδικού')

    welcomeFrame = Frame(master, height=125, bg='#1e1e2f')
    welcomeFrame.pack(side="top", fill=BOTH)

    appIcon = PhotoImage(data=icons.getLogoIcon())
    panel = Label(master, image=appIcon, bg='#1e1e2f').place(x=20, y=20)
    Label(welcomeFrame, text="Καλώς ορίσατε στον", font=("Comic Sans MS", 32), fg='white', bg='#1e1e2f').place(x=110,
                                                                                                               y=20)
    Label(welcomeFrame, text="Cerberus", font=("Helvetica", 32), fg='#d9ddff', bg='#1e1e2f').place(x=380, y=72)

    parent = Frame(master, bg='lightgrey')
    parent.pack(side="top", fill=BOTH, expand=True)

    Label(parent, text="Παρακαλώ εισάγεται τον Κωδικό σας:", bg='lightgrey').pack(pady=(25, 0), side=TOP)
    entry = Entry(parent, show="*", width=40)
    entry.pack(side=TOP, pady=(0, 15))

    enterIcon = PhotoImage(data=icons.getEnterIcon())
    b = Button(parent, borderwidth=1, text="Είσοδος", image=enterIcon, compound=LEFT, pady=8, width=120,
               command=check_password)
    b.pack(pady="7")

    entry.focus_set()
    master.resizable(0, 0)

    entry.bind('<Return>', lambda x: check_password())
    master.bind("<Escape>", lambda x: onDestroy())
    master.mainloop()

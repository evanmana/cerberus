from tkinter import *
import mainForm
import icons


def settingsForm():
    root = Toplevel()
    windowWidth = 700
    windowHeight = 340
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    positionRight = int(screenWidth / 2 - windowWidth / 2)
    positionDown = int(screenHeight / 3 - windowHeight / 2)
    root.geometry("{}x{}+{}+{}".format(windowWidth, windowHeight, positionRight, positionDown))
    root.wait_visibility(root)
    root.wm_attributes('-alpha', 0.98)

    img = PhotoImage(data=icons.getAppIcon())
    root.wm_iconphoto(True, img)

    root.title('Cerberus - Επεξεργασία Στοιχείων')

    welcomeFrame = Frame(root, height=130, bg='#1e1e2f')
    welcomeFrame.pack(side="top", fill=BOTH)

    appIcon = PhotoImage(data=icons.getLogoIcon())
    panel = Label(root, image=appIcon, bg='#1e1e2f').place(x=20, y=20)
    Label(welcomeFrame, text="Καλώς ορίσατε στον", font=("Comic Sans MS", 32), fg='white', bg='#1e1e2f').place(x=110,
                                                                                                              y=25)
    Label(welcomeFrame, text="Cerberus", font=("Helvetica", 32), fg='#d9ddff', bg='#1e1e2f').place(x=380, y=72)

    mainFrame = Frame(root, bg='lightgrey')
    mainFrame.pack(side="top", fill=BOTH, expand=True)

    Label(mainFrame, text="Κύριο Email:", font=("Arial", 12), bg='lightgrey').pack(pady=(25, 0))

    emailFrame = Frame(mainFrame, background="white", borderwidth=1, relief="sunken", highlightthickness=1)
    emailFrame.pack(side="top", padx=0, pady=0)

    emailEntry = Entry(emailFrame, width=35, borderwidth=0, highlightthickness=0, background="white")

    emailEntry.image = PhotoImage(data=icons.getEmailIcon())
    imageLabel = Label(emailFrame, image=emailEntry.image)
    imageLabel.pack(side="left")
    imageLabel['bg'] = 'white'

    emailEntry.pack(side="left", fill="both", expand=True)

    Label(mainFrame, text="Κύριος Κωδικός:", font=("Arial", 12), bg='lightgrey').pack(pady=(20,0))

    passwordFrame = Frame(mainFrame, background="white", borderwidth=1, relief="sunken", highlightthickness=1)
    passwordFrame.pack(side="top", padx=0, pady=0)

    passwordEntry = Entry(passwordFrame, width=35, borderwidth=0, highlightthickness=0, background="white")

    passwordEntry.image = PhotoImage(data=icons.getPasswordIcon())
    imageLabel = Label(passwordFrame, image=passwordEntry.image)
    imageLabel.pack(side="left")
    imageLabel['bg'] = 'white'

    passwordEntry.pack(side="left", fill="both", expand=True)

    saveIcon = PhotoImage(data=icons.getSaveIcon())
    okBtn = Button(mainFrame, borderwidth=1, text="Αποθήκευση", image=saveIcon, compound=LEFT, width=125)
    okBtn.pack(pady="15")

    root.resizable(0, 0)
    root.mainloop()
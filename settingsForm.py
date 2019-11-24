from tkinter import *
import mainForm


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
    root.wm_attributes('-alpha', 0.9)

    img = PhotoImage(data=mainForm.Cerberus.getAppIcon())
    root.wm_iconphoto(True, img)

    appIcon = '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'
    saveIcon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QA/wD/AP+gvaeTAAAApUlEQVQ4jc3SsQ3CMBQE0AeioGUeqBAt80CZdGEFtmABGgIdk1AwAAUUuPhYSQiigJO+fD5/nc7+5tcYBD7D9E3/AacoDANfYIkJqrRGXmGHeZt7kQruQa+CNsclpQWjjrirtF4D32Ob0tZdBpsUO9fgFsU2g3VHshcMG7TC875NVfQxgNJzxLHKvgk+wtcG+SPGn7jqODs2GdQYh30+xnPW+yd4ABmcHWJY2FSaAAAAAElFTkSuQmCC'
    emailIcon = 'iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAA/UlEQVQoka3QL0vDcRAG8M/8M9BgURGDDGYRw4KgGEwaBrbZZcEiZoNlwWwVX4OvwCEYVJhxoGAwiEVkzSJDmIhh94OvPzaTT7q755577m7UYBQxhx6+hvT8wjqaeMYdnnCL6l+iPbSxkatXQtwY5tTGVORrOMRm5OO4Qi0vbCZOWzHkANeoR72M+1RUjJsynGE74mVcJFwLJRjBNDoJOYFuxN3IM7xgIRO+YzYhe3FTtk0x4Qr4hjF8hmMFD7jEUYjrWMI+PrCSv7Oq//LMaQen2MUMjnGCRQPQ0H95OVefx+QgQYparNLCOW7wiNV8Y2HIgFI4veFVPORf8ANKHy70AdaDagAAAABJRU5ErkJggg=='
    passwordIcon = 'iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAA5ElEQVQokZ3Rr0qDYRQG8N/nJkzvwKUZRas2YSDCTHa9DW9CsBlWDN6CwbBgMowlNQwMsvhZTSIIavjO8OX1lYkPnPKc85zn/OF3rEb8GesYYRoxQm+RaAUPGCTcQXCdtLCVCQ9R4TzhnrAVtY9zcikTbuC+MMkdNlOiShqcheMb6kzYjVGvcIKPdiR2ouN+wS3FENuYzIWdcJlpXvCK5ci9J1ytOeCPHY/xojn/dUQvuKO0sJ0JxziNzhf4xHNw49IqfVwu2E/U9Pm+ahe3uAmXEirsYRd1lSTWZL8qYKoZ/f/4As90Kcf5M3zwAAAAAElFTkSuQmCC'

    root.title('Επεξεργασία Στοιχείων')

    welcomeFrame = Frame(root, height=130, bg='#1e1e2f')
    welcomeFrame.pack(side="top", fill=BOTH)

    appIcon = PhotoImage(data=mainForm.Cerberus.getLogoIcon())
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

    emailEntry.image = PhotoImage(data=emailIcon)
    imageLabel = Label(emailFrame, image=emailEntry.image)
    imageLabel.pack(side="left")
    imageLabel['bg'] = 'white'

    emailEntry.pack(side="left", fill="both", expand=True)

    Label(mainFrame, text="Κύριος Κωδικός:", font=("Arial", 12), bg='lightgrey').pack(pady=(20,0))

    passwordFrame = Frame(mainFrame, background="white", borderwidth=1, relief="sunken", highlightthickness=1)
    passwordFrame.pack(side="top", padx=0, pady=0)

    passwordEntry = Entry(passwordFrame, width=35, borderwidth=0, highlightthickness=0, background="white")

    passwordEntry.image = PhotoImage(data=passwordIcon)
    imageLabel = Label(passwordFrame, image=passwordEntry.image)
    imageLabel.pack(side="left")
    imageLabel['bg'] = 'white'

    passwordEntry.pack(side="left", fill="both", expand=True)

    saveIcon = PhotoImage(data=saveIcon)
    okBtn = Button(mainFrame, borderwidth=1, text="Αποθήκευση", image=saveIcon, compound=LEFT, width=125)
    okBtn.pack(pady="15")

    root.resizable(0, 0)
    root.mainloop()
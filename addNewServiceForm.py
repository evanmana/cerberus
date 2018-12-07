from tkinter import *

def main(root):
    def exitForm(event):
        onDestory()

    def onDestory():
        root.deiconify()
        master.destroy()

    master = Toplevel()
    master.lift()
    master.focus_force()
    master.grab_set()

    master.title('Εισαγωγή Νέας Υπηρεσίας')
    master.resizable(0, 0)

    Label(master, text="Υπηρεσία:").grid(row=0, sticky="W", padx=5, pady=5)
    Label(master, text="Email:").grid(row=1, sticky="W", padx=5, pady=5)
    Label(master, text="Username:").grid(row=2, sticky="W", padx=5, pady=5)
    Label(master, text="Password:").grid(row=3, sticky="W", padx=5, pady=5)

    eService = Entry(master, width=35)
    eService.focus()
    eEmail = Entry(master, width=35)
    eUsername = Entry(master, width=35)
    ePassword = Entry(master, width=35)

    eService.grid(row=0, column=1, pady=5, padx=5)
    eEmail.grid(row=1, column=1, pady=5, padx=5)
    eUsername.grid(row=2, column=1, pady=5, padx=5)
    ePassword.grid(row=3, column=1, pady=5, padx=5)

    enterButton = Button(master, text="Εισαγωγή Στοιχείων")
    enterButton.grid(row=4, column=0, columnspan=2, sticky="we", padx=5, pady=5)



    master.bind("<Escape>", exitForm)
    master.protocol("WM_DELETE_WINDOW", onDestory)
    mainloop( )

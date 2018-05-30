from tkinter import *

def show_entry_fields():
   print("First Name: %s\nLast Name: %s" % (eService.get(), eEmail.get()))

master = Tk()
master.title('Εισαγωγή Νέας Υπηρεσίας')
#master.geometry("330x300") #You want the size of the app to be 500x500
master.resizable(0, 0) #Don't allow resizing in the x or y direction



Label(master, text="Υπηρεσία:").grid(row=0, sticky="W", padx=5, pady=5)
Label(master, text="Email:").grid(row=1, sticky="W", padx=5, pady=5)
Label(master, text="Username:").grid(row=2, sticky="W", padx=5, pady=5)
Label(master, text="Password:").grid(row=3, sticky="W", padx=5, pady=5)

eService = Entry(master, width=35)
eEmail = Entry(master, width=35)
eUsername = Entry(master, width=35)
ePassword = Entry(master, width=35)

eService.grid(row=0, column=1, pady=5)
eEmail.grid(row=1, column=1, pady=5)
eUsername.grid(row=2, column=1, pady=5)
ePassword.grid(row=3, column=1, pady=5)

enterButton = Button(master, text="Εισαγωγή Στοιχείων", command=master.quit)
enterButton.grid(row=4, column=0, columnspan=2, sticky="we", padx=5, pady=5)


mainloop( )

from tkinter import *
import connectDB


def show_entry_fields():
   print("%s\t%s\t%s\t%s" % (eService.get(), eEmail.get(), eUsername.get(), ePassword.get()))

def insertService():
   print("Connecting to MySQL...")
   connection = connectDB.connect()
   print("Connected to MySQL...")
   try:
    with connection.cursor() as cursor:
        sql = "INSERT INTO `account` (`nameService`, `email`, `username`,  `password`) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (eService.get(), eEmail.get(), eUsername.get(), ePassword.get()))
    connection.commit()
   finally:
    connection.close()


master = Tk()
master.title('Εισαγωγή Νέας Υπηρεσίας')
master.resizable(0, 0)

Label(master, text="Υπηρεσία:").grid(row=0, sticky="W", padx=5, pady=5)
Label(master, text="Email:").grid(row=1, sticky="W", padx=5, pady=5)
Label(master, text="Username:").grid(row=2, sticky="W", padx=5, pady=5)
Label(master, text="Password:").grid(row=3, sticky="W", padx=5, pady=5)

eService = Entry(master, width=35)
eEmail = Entry(master, width=35)
eUsername = Entry(master, width=35)
ePassword = Entry(master, width=35)

eService.grid(row=0, column=1, pady=5, padx=5)
eEmail.grid(row=1, column=1, pady=5, padx=5)
eUsername.grid(row=2, column=1, pady=5, padx=5)
ePassword.grid(row=3, column=1, pady=5, padx=5)

enterButton = Button(master, text="Εισαγωγή Στοιχείων", command=insertService)
enterButton.grid(row=4, column=0, columnspan=2, sticky="we", padx=5, pady=5)


mainloop( )

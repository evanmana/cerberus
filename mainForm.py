from tkinter import *
import connectDB
import addNewServiceForm

def getServices():
   print("Connecting to MySQL...")
   connection = connectDB.connect()
   print("Connected to MySQL...")
   try:
     with connection.cursor() as cursor:
        sql = "SELECT * FROM `account`"
        cursor.execute(sql)
        result = cursor.fetchone()
        while result is not None:
            print(result)
            result = cursor.fetchone()
   finally:
    connection.close()


master = Tk()
master.title('Εισαγωγή Νέας Υπηρεσίας')
master.resizable(0, 0)

menubar = Menu(master)
filemenu = Menu(menubar, tearoff=0)

menubar.add_cascade(label="Cerberus", menu=filemenu)
filemenu.add_command(label="Εισαγωγή Υπηρεσίας", command=addNewServiceForm)
filemenu.add_command(label="Έξοδος", command=master.quit)

master.config(menu=menubar)



mainloop( )

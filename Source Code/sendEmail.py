import smtplib
import sqlite3
from tkinter import messagebox


def sendEmail():
    try:
        conn = sqlite3.connect('cerberus.db')
    except sqlite3.Error as e:
        print(e)

    cur = conn.cursor()
    cur.execute(
        "SELECT masterToken FROM cerberusParameters")
    masterToken = cur.fetchone()
    cur.close()

    TO = 'vagelis.manavis@gmail.com'
    SUBJECT = 'Υπενθύμιση Κωδικού Cerberus'
    TEXT = 'Ο Κωδικός σας έιναι:\t'+ masterToken[0]

    gmail_sender = 'vagelis.manavis@gmail.com'
    gmail_passwd = 'man@(((@MAN'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % SUBJECT,
                        '', TEXT])

    try:
        server.sendmail(gmail_sender, [TO], BODY.encode("utf8"))
        messagebox.showinfo("Μήνυμα Επιτυχίας", "Ο Κωδικός σας στάλθηκε στο Email σας.")
    except Exception as e:
        print(e)
        print('error sending mail')

    server.quit()

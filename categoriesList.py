import sqlite3
from cryptography.fernet import Fernet
import cerberusCryptography


def getCategoriesList():
    key = cerberusCryptography.getMasterKey()
    cipher_suite = Fernet(key)
    categoriesList = []

    try:
        conn = sqlite3.connect('cerberus.db')
    except sqlite3.Error as e:
        print(e)

    cur = conn.cursor()
    cur.execute(
        "SELECT category FROM service")
    rows = cur.fetchall()
    cur.close()

    for row in rows:
        category = cipher_suite.decrypt(row[0]).decode("utf-8")
        if category not in categoriesList:
            categoriesList.append(category)

    return categoriesList

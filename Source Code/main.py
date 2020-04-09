import platform
import sqlite3
import os


if __name__ == '__main__':
    print(platform.system())
    if not os.path.isfile('cerberus.db'):
        print("Creating database...")
        import createDatabase
        createDatabase.main()

    try:
        conn = sqlite3.connect('cerberus.db')
    except sqlite3.Error as e:
        print(e)

    cur = conn.cursor()
    cur.execute(
        "SELECT primaryEmail, masterToken, salt FROM cerberusParameters")
    row = cur.fetchone()
    cur.close()

    if row is None:
        import initApp
    else:
        import mainForm
import sqlite3
from sqlite3 import Error

database = r"cerberus.db"


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def runSQLStatement(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    sqlCreateCerberusTable = """ 
                                CREATE TABLE IF NOT EXISTS `service` (
                                `id`	INTEGER NOT NULL,
                                `name`	TEXT NOT NULL,
                                `value`	TEXT,
                                `email`	TEXT,
                                `username`	TEXT,
                                `password`	TEXT,
                                `url`	TEXT,
                                `category`	TEXT,
                                PRIMARY KEY(`id`) 
                                );
                            """
    createIndex = """
                    CREATE INDEX `nameIdx` ON `service` (
                    `name`	ASC
                    ); 
                  """

    sqlCreateCerberusParmTable = """
                                CREATE TABLE IF NOT EXISTS `cerberusParameters` (
                                `primaryEmail`	TEXT NOT NULL,
                                `masterToken`	TEXT NOT NULL,
                                `salt`	TEXT NOT NULL,
                                `version`	TEXT,
                                `passwdLastUpdate`	TEXT
                                );
                            """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create Cerberus table
        runSQLStatement(conn, sqlCreateCerberusTable)
        runSQLStatement(conn, createIndex)

        # create cerberusParameters table
        runSQLStatement(conn, sqlCreateCerberusParmTable)
    else:
        print("Error! cannot create the database connection.")
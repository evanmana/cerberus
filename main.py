import connectDB

connection = connectDB.connect()

try:
    #with connection.cursor() as cursor:
    #    sql = "INSERT INTO `user` (`username`, `password`, `email`) VALUES (%s, %s, %s)"
    #    cursor.execute(sql, ('evanmana', 'asdfasdf', 'vagelis.manavis@gmail.com'))

    #connection.commit()

    with connection.cursor() as cursor:
        sql = "SELECT * FROM `user`"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()


print("Hello Cerberus :)")

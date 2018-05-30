import connectDB

connection = connectDB.connect()

try:
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `user`"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()


print("Hello Cerberus :)")

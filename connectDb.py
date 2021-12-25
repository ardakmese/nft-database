import mysql.connector

def startDb():
    from mysql.connector import Error

    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='nft',
                                             user='root',
                                             password='12345678',
                                             auth_plugin='mysql_native_password'
                                             )
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("MySQL'e bağlantı başarılı, server versiyonu: ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("Bağlanılan database: ", record)
            return connection

    except Error as e:
        print("MySql'e bağlanırken hata oluştu!", e)

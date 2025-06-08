import mysql.connector
from mysql.connector import Error

class Conexion:
    def __init__(self):
        self.__server = 'localhost'
        self.__user = 'root'
        self.__pass = 'root'
        self.__db = "lamalca_db"
        self.__port = 3306


    def get_conexion(self):
            con = mysql.connector.connect(
                host=self.__server, 
                user=self.__user, 
                password=self.__pass, 
                db=self.__db, 
                port=self.__port,
                auth_plugin='mysql_native_password' 
            )
            return con
        


conecta = Conexion()

try: 
    con = conecta.get_conexion()
    if con:
        print('Conexion exitosa')
except Error as e:
    print(e)

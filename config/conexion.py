import psycopg2
import os
from psycopg2 import Error
from dotenv import load_dotenv

load_dotenv()

class Conexion:
    def __init__(self):
        self.__server = os.getenv("DB_HOST", "localhost")
        self.__user = os.getenv("DB_USER")
        self.__pass = os.getenv("DB_PASS") 
        self.__db = os.getenv("DB_NAME")
        self.__port = os.getenv("DB_PORT", 5432)

    def get_conexion(self):
            con = psycopg2.connect(
                host=self.__server, 
                user=self.__user, 
                password=self.__pass, 
                dbname=self.__db,  
                port=self.__port,
            )
            return con


if __name__ == "__main__":
    conecta = Conexion()
    try: 
        con = conecta.get_conexion()
        if con:
            print('Conexion exitosa a PostgreSQL')
            con.close()
    except Error as e:
        print(f"Error de conexión: {e}")
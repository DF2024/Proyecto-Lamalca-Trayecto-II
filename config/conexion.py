import psycopg2
from psycopg2 import Error

class Conexion:
    def __init__(self):
        self.__server = 'localhost'
        self.__user = 'dandefensor'
        self.__pass = 'andres123' 
        self.__db = "lamalca_pg"
        self.__port = 5432

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
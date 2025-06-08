# id_pedido 
# id_cliente 
# fecha_pedido 
# estado_pedido  
# total_pedido 


import os 
import sys 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conexion import Conexion
from mysql.connector import Error
from 
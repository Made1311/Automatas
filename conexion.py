import mysql.connector

def conectar_bd():
    # Cambia los parámetros según tu configuración
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Taylorswift13",
        database="automatas2"
    )
    return conexion
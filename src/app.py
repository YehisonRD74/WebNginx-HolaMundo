import os
import time
from flask import Flask
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def conectar_bd():
    # Intentamos conectar varias veces por si MySQL tarda un poco en arrancar
    for i in range(5):
        try:
            conexion = mysql.connector.connect(
                host=os.environ.get('DB_HOST', 'db'),
                user=os.environ.get('DB_USER', 'root'),
                password=os.environ.get('DB_PASSWORD', 'rootpassword'),
                database=os.environ.get('DB_NAME', 'holamundo_db')
            )
            if conexion.is_connected():
                return conexion
        except Error:
            time.sleep(3) # Espera 3 segundos antes de reintentar
    return None

@app.route('/')
def hola_mundo():
    conexion = conectar_bd()
    if conexion:
        conexion.close()
        return """
        <div style="text-align:center; margin-top:10%; font-family:sans-serif;">
            <h1 style="color:#2ecc71; font-size: 3rem;">🚀 ¡Hola Mundo desde Docker!</h1>
            <p style="font-size:1.5rem; color:#34495e;">La conexión a la base de datos MySQL fue <strong>EXITOSA</strong>.</p>
        </div>
        """
    else:
        return """
        <div style="text-align:center; margin-top:10%; font-family:sans-serif;">
            <h1 style="color:#e74c3c; font-size: 3rem;">❌ Error de Conexión</h1>
            <p style="font-size:1.5rem; color:#34495e;">No se pudo conectar a la base de datos MySQL.</p>
        </div>
        """, 500

if __name__ == '__main__':
    # Escucha en todas las redes del contenedor en el puerto 5000
    app.run(host='0.0.0.0', port=5000)
from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'prode'
}

def get_db_connection():
    conn = mysql.connector.connect(*db_config)
    return conn

def execute(query):
    conexion = get_db_connection()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute(query)
        resultados = cursor.fetchall()
    finally:
        cursor.close()
        conexion.close()

    return resultados

@app.route("/")
def home():
    return "Servidor ok"

@app.route("/partidos")
def listar_partidos():
    resultados = execute("SELECT FROM partidos")
    return jsonify(resultados)

if __name__ == "__main__":
    app.run(debug=True, port=5000)


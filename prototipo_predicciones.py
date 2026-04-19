from flask import Blueprint, request, jsonify
from mysql_database import get_connection


predicciones_bp = Blueprint("predicciones", __name__)

@predicciones_bp.route("/partidos/<int:id>/prediccion", methods=["POST"])
def crear_prediccion(id):
    
    if id <= 0:
      return jsonify({"error": "ID inválido"}), 400
    
    
    data = request.get_json()
    id_usuario = data.get("usuario_id")
    goles_local = data.get("goles_local")
    goles_visitante = data.get("goles_visitante")
    if not id_usuario or goles_local is None or goles_visitante is None:
        return jsonify({"error": "Datos incompletos"}), 400

    conn = None
    cursor = None


    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        #vrificar que el partido exista
        cursor.execute("SELECT * FROM partidos WHERE id_partido = %s", (id,))
        partido = cursor.fetchone()

        if not partido:
            return jsonify({"error": "El partido no existe"}), 404

        #verificar que no tenga resultado
        cursor.execute("SELECT * FROM resultados WHERE id_partido = %s", (id,))
        resultado = cursor.fetchone()

        if resultado:
            return jsonify({"error": "El partido ya se jugó"}), 400

        #verificar que no exista predicción previa
        cursor.execute("""
            SELECT * FROM predicciones 
            WHERE id_usuario = %s AND id_partido = %s
        """, (id_usuario, id))

        if cursor.fetchone():
            return jsonify({"error": "Ya hiciste una predicción para este partido"}), 400

        #INSERTAR PREDICCION
        cursor.execute("""
            INSERT INTO predicciones (id_usuario, id_partido, goles_local, goles_visitante)
            VALUES (%s, %s, %s, %s)
        """, (id_usuario, id, goles_local, goles_visitante))

        conn.commit()

        return jsonify({"message": "Predicción creada"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
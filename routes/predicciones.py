from flask import Blueprint, request, jsonify
from db import get_connection
from .errores import(bad_request, not_found, server_error)

predicciones_bp = Blueprint("predicciones", __name__)


@predicciones_bp.route("/<int:id>/predicciones/", methods=['POST'])
def crear_prediccion(id):

    data = request.get_json()
    id_usuario = data.get('usuario_id')
    local = data.get('goles_local')
    visitante = data.get('goles_visitante')

    if local is None or visitante is None:
        return jsonify(bad_request), 400
    
    try:
        connector = get_db_connection()
        cursor = connector.cursor(dictionary=True)

        cursor.execute("""
        INSERT INTO predicciones
               (partido_id, usuario_id, goles_local, goles_visitante) 
        VALUES (%s, %s, %s, %s)    
    """, (id, id_usuario, local, visitante))


        connector.commit()

        return jsonify({'message' : 'Prediccion hecha correctamente'}), 201

    except Exception as e:
        print(f"el error es: {e}")
        return jsonify(server_error), 500

    finally:
        cursor.close()
        connector.close() 

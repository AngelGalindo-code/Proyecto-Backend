from flask import Blueprint, jsonify, request

from .errores import bad_request, not_found, server_error

partidos_bp = Blueprint("partidos", __name__)

@partidos_bp.route('/partidos/<int:id>/resultados', methods=['PUT'])

def actualizar_resultado(id_partido):

    if id_partido<= 0:
            error_400 = bad_request.copy()
            error_400["errors"][0]["description"] = "Id invalido, debe ser mayor a 0"
            return jsonify(error_400), 400
    
    data = request.get_json()
    
    if not data or "local" not in data or "visitante" not in data:
            error_400 = bad_request.copy()
            error_400["errors"][0]["description"] = "No se recibió información en el cuerpo de la peticion o el formato no es JSON"
            return jsonify(error_400), 400
    
    conn = None
    cursor = None

    try: 
        conn = get_connection()
        cursor = conn.cursor()

        goles_local = data.get('goles_local')
        goles_visitante = data.get('goles_visitante')

        query = """
            UPDATE partidos
            SET goles_local = %s,
                goles_visitante = %s
            WHERE id = %s

        """
        cursor.execute(query, (goles_local, goles_visitante, id_partido))
        conn.commit()

        if cursor.rowcount == 0:
            error_404 = not_found.copy()
            error_404["errors"][0]["description"] = f"El partido con ID {id_partido} no existe, no se pudo actualizar."
            return jsonify(error_404), 404
        
        return '', 204

    except Exception:
   
            return jsonify(server_error), 500
    finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()



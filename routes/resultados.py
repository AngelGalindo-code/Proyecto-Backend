from flask import Blueprint, jsonify, request

partidos_bp = Blueprint("partidos", __name__)

@partidos_bp.route('/partidos/<int:id>/resultados', methods=['PUT'])

def actualizar_resultado(id):

    if id <= 0:
            error_400 = {
                  "errors": [
                        {
                            "code": "400",
                            "message": "Bad request",
                            "level": "error",
                            "description": "El id debe ser mayor a 0"
                        }
                  ]
            }
            return jsonify(error_400), 400
    
    data = request.get_json()
    
    if not data or "local" not in data or "visitante" not in data:
            error_400 = {
                "errors": [
                    {
                        "code": "EMPTY_BODY",
                        "message": "Bad Request",
                        "level": "error",
                        "description": "El cuerpo de la solicitud es obligatorio y debe ser JSON"
                    }
                ]
            }
            return jsonify(error_400), 400
    
    conn = None
    cursor = None

    try: 
        conn = get_connection()
        cursor = conn.cursor()

        resultado_local = data.get('resultado_local')
        resultado_visitante = data.get('resultado_visitante')

        query = """
            UPDATE partidos
            SET resultado_local = %s,
                resultado_visitante = %s
            WHERE id = %s

        """
        cursor.execute(query, (resultado_local, resultado_visitante, id))
        conn.commit()

        if cursor.rowcount == 0:
            error_400 = {
                "errors": [
                    {
                    "code": "NOT_FOUND",
                    "message": "Bad Request",
                    "level": "error",
                    "description": f"El partido con ID {id} no existe, no se pudo actualizar."
                    }
                ]
            }
            return jsonify(error_400), 400
        
        return '', 204

    except Exception as e:
            error_500 = {
                "errors": [
                    {
                    "code": "INTERNAL_ERROR",
                    "message": "Ocurrio un error inesperado en el servidor",
                    "level": "error",
                    "description": str(e)
                    }
                ]
            }
            return jsonify(error_500), 500
    finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()



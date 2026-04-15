from flask import Blueprint, jsonify, request
from datetime import datetime

partidos_bp = Blueprint("partidos", __name__)

fases_validas = ['grupos', 'dieciseisavos', 'octavos', 'cuartos', 'semis', 'final']

@partidos_bp.route('/partidos', methods=['GET'])

def listar_partidos():

    fecha = request.args.get('fecha')
    fase = request.args.get('fase')

    if fase and fase.lower() not in fases_validas:
        error_bad_request = {
            "errors": [
                {      
                    "code": "XXX",
                    "message": "Mensaje",
                    "level": "error",
                    "description": "Fase invalida"
                }
            ]
        }
        return jsonify(error_bad_request), 400
    if fecha:
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
        except ValueError:
            error_bad_request = {
            "errors": [
                    {      
                        "code": "XXX",
                        "message": "Mensaje",
                        "level": "error",
                        "description": "Fecha invalida"
                    }
                ]
            }
            return jsonify(error_bad_request), 400
        

    try: 
        conn = get_conection()
        cursor = conn.cursor(dictionary=True)

        equipo = request.args.get('equipo')

        limit = request.args.get('_limit', default=10, type=int)
        offset = request.args.get('_offset', default=0, type=int)

        query = "SELECT id, equipo_local, equipo_visitante, fecha, fase FROM partidos "
        filtros = []
        params = []

        if equipo:
            filtros.append("(equipo_local = %s OR equipo_visitante = %s)")
            params.extend([equipo,equipo])
        if fecha:
            filtros.append("fecha = %s")
            params.append(fecha)
        if fase:
            filtros.append("fase = %s")
            params.append(fase.lower())

        if filtros: 
            query += " WHERE " + " AND ".join(filtros)


        query += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        cursor.execute(query, params)

        partidos = cursor.fetchall()

        if not partidos:
            cursor.close()
            conn.close()
            return '', 204
        else:
            cursor.close()
            conn.close()
            return jsonify({"partidos": partidos}), 200
        
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

@partidos_bp.route('/partidos', methods=["POST"])

def crear_partido():
        
        data = request.get_json()

        equipo_local = data.get('equipo_local')
        equipo_visitante = data.get('equipo_visitante')
        fecha = data.get('fecha')
        fase = data.get('fase')

        if not equipo_local or not equipo_visitante or not fecha or not fase:
            error_bad_request = {
                "errors": [
                    {
                        "code": "XXX",
                        "message": "Mensaje",
                        "level": "error",
                        "description": "Descripción"
                    }
                ]
            }
            return jsonify(error_bad_request), 400
        
        if fase.lower() not in fases_validas:
            error_bad_request = {
                "errors": [
                    {
                        "code": "XXX",
                        "message": "Mensaje",
                        "level": "error",
                        "description": "Descripción"
                    }
                ]
            }
            return jsonify(error_bad_request), 400
        if fecha:
            try:
                datetime.strptime(fecha, '%Y-%m-%d')
            except ValueError:
                error_bad_request = {
                    "errors": [
                    {      
                        "code": "XXX",
                        "message": "Mensaje",
                        "level": "error",
                        "description": "Fecha invalida"
                    }
                ]
            }
            return jsonify(error_bad_request), 400
        
        try:
            conn = get_conection()
            cursor = conn.cursor()

            query = """
            INSERT INTO partidos (equipo_local, equipo_visitante, fecha, fase)
            VALUES (%s %s %s %s)
            """
            cursor.execute(query, (equipo_local, equipo_visitante, fecha, fase.lower()))
            conn.commit()

            cursor.close()
            conn.close()
        
            return jsonify({"message" : "partido creado"}), 201
        
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
        
@partidos_bp.route('/partidos/<int:id>', methods=["GET"])

def obtener_partido(id):
    if id <= 0:
            error_400 = {
                "errors": [
                    {
                        "code": "INVALID_ID",
                        "message": "Bad Request",
                        "level": "error",
                        "description": "El id debe ser mayor a 0"
                    }
                ]
            }
            return jsonify(error_400), 400
    try: 
        
        conn = get_conection()
        cursor = conn.cursor()

        query = """
        SELECT id, equipo_local, equipo_visitante, fecha, fase FROM partidos
        WHERE id = %s
        """
        cursor.execute(query, (id,))
        resultado = cursor.fetchone()
        
        if not resultado:
            error_not_found = {
                "errors": [
                    {
                        "code": "XXX",
                        "message": "Mensaje",
                        "level": "error",
                        "description": "Descripción"
                    }
                ]         
            }
            return jsonify(error_not_found), 404
        
        partido = {
                "id": resultado[0],
                "equipo_local": resultado[1],
                "equipo_visitante": resultado[2],
                "fecha": str(resultado[3]),
                "fase": resultado[4]
        }
        return jsonify(partido), 200

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

@partidos_bp.route('/partidos/<int:id>', methods=['PUT'])

def remplazar_partido(id):
    if id <= 0:
            error_400 = {
                "errors": [
                    {
                        "code": "INVALID_ID",
                        "message": "Bad Request",
                        "level": "error",
                        "description": "El id debe ser mayor a 0"
                    }
                ]
            }
            return jsonify(error_400), 400
    
    data = request.get_json()

    if not data:
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
        equipo_local = data.get("equipo_local")
        equipo_visitante = data.get("equipo_visitante")
        fecha = data.get("fecha")
        fase = data.get("fase")

        conn = get_conection()
        cursor = conn.cursor()

        query = """
        UPDATE partidos SET equipo_local = %s, equipo_visitante = %s,
        fecha = %s, fase = %s 
        WHERE id = %s
        """

        cursor.execute(query, (equipo_local, equipo_visitante, fecha, fase, id))
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

@partidos_bp.route('/partidos/<int:id>', methods=['PATCH'])

def actualizar_parcialmente_partido(id):

    if id <= 0:
            error_400 = {
                "errors": [
                    {
                        "code": "INVALID_ID",
                        "message": "Bad Request",
                        "level": "error",
                        "description": "El id debe ser mayor a 0"
                    }
                ]
            }
            return jsonify(error_400), 400
    
    data = request.get_json()

    if not data:
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
        conn = get_conection()
        cursor = conn.cursor()

        equipo_local = data.get("equipo_local")
        equipo_visitante = data.get("equipo_visitante")
        fecha = data.get("fecha")
        fase = data.get("fase")

        query = """
        UPDATE partidos 
        SET equipo_local = COALESCE(%s, equipo_local),
            equipo_visitante = COALESCE(%s, equipo_visitante),
            fecha = COALESCE(%s, fecha),
            fase = COALESCE(%s, fase)
        WHERE id = %s
        """

        cursor.execute(query, (equipo_local, equipo_visitante, fecha, fase, id))
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

@partidos_bp.route('/partidos/<int:id>', methods=['DELETE'])

def eliminar_partido(id):
    
    if id <= 0:
            error_400 = {
                "errors": [
                    {
                        "code": "INVALID_ID",
                        "message": "Bad Request",
                        "level": "error",
                        "description": "El id debe ser mayor a 0"
                    }
                ]
            }
            return jsonify(error_400), 400
    conn = None
    cursor = None

    try:
        conn = get_conection()
        cursor = conn.cursor()

        query = "DELETE FROM partidos WHERE id = %s "
        cursor.execute(query, (id))

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
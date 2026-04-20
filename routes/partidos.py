from flask import Blueprint, jsonify, request
from datetime import datetime
from .errores import bad_request, not_found, server_error, conflict
from db import get_connection

partidos_bp = Blueprint("partidos", __name__)

fases_validas = ['grupos', 'dieciseisavos', 'octavos', 'cuartos', 'semis', 'final']

@partidos_bp.route('/partidos', methods=['GET'])

def listar_partidos():

    try: 
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        equipo = request.args.get('equipo')
        fecha = request.args.get('fecha')
        fase = request.args.get('fase')
        limit = request.args.get('_limit', default=10, type=int)
        offset = request.args.get('_offset', default=0, type=int)

        if fase and fase.lower() not in fases_validas:
            error_400 = bad_request.copy()
            error_400["errors"][0]["description"] = "La fase proporcionada no es válida"
            return jsonify(error_400), 400


        query = "SELECT id_partido, equipo_local, equipo_visitante, fecha, fase FROM partidos"
        filtros = []
        valores_query = []

        if equipo:
            filtros.append("(equipo_local = %s OR equipo_visitante = %s)")
            valores_query.extend([equipo, equipo])
        
        if fecha:
            filtros.append("fecha = %s")
            valores_query.append(fecha)
            
        if fase:
            filtros.append("fase = %s")
            valores_query.append(fase.lower())

        if filtros:
            query += " WHERE " + " AND ".join(filtros)

        query += " LIMIT %s OFFSET %s"

        valores_query.extend([limit, offset])     
        cursor.execute(query, valores_query)
        partidos = cursor.fetchall()
        
        if not partidos:
            cursor.close()
            conn.close()
            return '', 204
        else:
            cursor.close()
            conn.close()
            return jsonify({"partidos": partidos}), 200
        
    except Exception:
        return jsonify(server_error), 500

@partidos_bp.route('/partidos', methods=["POST"])

def crear_partido():
        
        data = request.get_json()

        equipo_local = data.get('equipo_local')
        equipo_visitante = data.get('equipo_visitante')
        fecha = data.get('fecha')
        fase = data.get('fase')

        if not equipo_local or not equipo_visitante or not fecha or not fase:
            error_400 = bad_request.copy()
            error_400["errors"][0]["description"] = "Faltan campos obligatorios: equipo_local, equipo_visitante, fecha o fase"
            return jsonify(error_400), 400
        
        if fase.lower() not in fases_validas:
            error_400 = bad_request.copy
            error_400["errors"][0]["description"] = "La fase no es valida"
            return jsonify(error_400), 400
        if fecha:
            try:
                datetime.strptime(fecha, '%Y-%m-%d')
            except ValueError:
                error_400= bad_request.copy()
                error_400["errors"][0]["description"] = "El formato de fecha debe ser YYYY-MM-DD"
                return jsonify(error_400), 400
        
        try:
            conn = get_connection()
            cursor = conn.cursor()

            check_query = """
            SELECT id_partido FROM partidos 
            WHERE equipo_local = %s AND equipo_visitante = %s AND fecha = %s AND fase = %s
            """
            cursor.execute(check_query, (equipo_local, equipo_visitante, fecha, fase))
            existe = cursor.fetchone()

            if existe:
                error_409 = conflict.copy()
                error_409["errors"][0]["description"] = "Ya existe un partido programado entre estos equipos en esa fecha."
                return jsonify(error_409), 409

            else: 
                 query = """
                INSERT INTO partidos (equipo_local, equipo_visitante, fecha, fase)
                VALUES (%s, %s, %s, %s)
                """
            cursor.execute(query, (equipo_local, equipo_visitante, fecha, fase.lower()))
            conn.commit()
            
            return jsonify({"message" : "partido creado"}), 201
        
        except Exception:
            return jsonify(server_error), 500
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        
@partidos_bp.route('/partidos/<int:id_partido>', methods=["GET"])

def obtener_partido(id_partido):
    if id_partido <= 0:
            error_400 = bad_request.copy()
            error_400["errors"][0]["description"] = "Id invalido"
            return jsonify(error_400), 400
    try: 
        
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM partidos WHERE id_partido = %s"
        cursor.execute(query, (id_partido,))
        partido = cursor.fetchone() 

        if partido:
            return jsonify(partido), 200
        else:
            error_404 = not_found.copy()
            error_404["errors"][0]["description"] =  "Partido no encontrado"
            return jsonify(error_404), 404
            
    except Exception:
            return jsonify(server_error), 500
    finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

@partidos_bp.route('/partidos/<int:id_partido>', methods=['PUT'])

def remplazar_partido(id_partido):
    if id_partido <= 0:
            error_400 = bad_request.copy()
            error_400["errors"][0]["description"] = "Id invalido, debe ser mayor a 0"
            return jsonify(error_400), 400
    
    data = request.get_json(silent= True)
    if data == None:
        error_400 = bad_request.copy()
        error_400["errors"][0]["description"] = "No se recibió información en el cuerpo de la peticion o el formato no es JSON"
        return jsonify(error_400), 400
    
    conn = None
    cursor = None

    try:
        equipo_local = data.get("equipo_local")
        equipo_visitante = data.get("equipo_visitante")
        fecha = data.get("fecha")
        fase = data.get("fase")

        conn = get_connection()
        cursor = conn.cursor()

        query = """
        UPDATE partidos SET equipo_local = %s, equipo_visitante = %s,
        fecha = %s, fase = %s 
        WHERE id = %s
        """

        cursor.execute(query, (equipo_local, equipo_visitante, fecha, fase, id_partido))
        conn.commit()

        if cursor.rowcount == 0:
            error_404 = not_found.copy()
            error_404["errors"][0]["description"] = f"El partido con ID {id} no existe, no se pudo actualizar."
            return jsonify(error_404), 404
        
        return '', 204

    except Exception:
            return jsonify(server_error), 500
    finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

@partidos_bp.route('/partidos/<int:id_partido>', methods=['PATCH'])

def actualizar_parcialmente_partido(id_partido):

    if id_partido <= 0:
            error_400 = bad_request.copy()
            error_400["errors"][0]["description"] = "Id invalido, debe ser mayor a 0"
            return jsonify(error_400), 400
    
    data = request.get_json(silent= True)
    if data == None:
        error_400 = bad_request.copy()
        error_400["errors"][0]["description"] = "No se recibió información en el cuerpo de la peticion o el formato no es JSON"
        return jsonify(error_400), 400
    
    conn = None
    cursor = None

    try: 
        conn = get_connection()
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
        WHERE id_partido = %s
        """

        cursor.execute(query, (equipo_local, equipo_visitante, fecha, fase, id_partido))
        conn.commit()
        
        if cursor.rowcount == 0:
            error_404 = not_found.copy()
            error_404["errors"][0]["description"] = f"El partido con ID {id_partido} no existe, no se pudo eliminar."
            return jsonify(error_404), 404

        
        return '', 204

    except Exception:
            return jsonify(server_error), 500
    finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

@partidos_bp.route('/partidos/<int:id_partido>', methods=['DELETE'])

def eliminar_partido(id_partido):
    
    if id_partido <= 0:
            error_400 = bad_request.copy()
            error_400["errors"][0]["description"] = "Id invalido, debe ser mayor a 0"
            return jsonify(error_400), 400
    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = "DELETE FROM partidos WHERE id_partido = %s "
        cursor.execute(query, (id_partido,))

        conn.commit()
        
        if cursor.rowcount == 0:
            error_404 = not_found.copy()
            error_404["errors"][0]["description"] = f"El partido con ID {id_partido} no existe, no se pudo eliminar."
            return jsonify(error_404), 404
        
        
        return '', 204
    except Exception:
            return jsonify(server_error), 500
    finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
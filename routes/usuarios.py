from flask import Blueprint, request, jsonify
from db import get_connection
from .errores import (bad_request, not_found, conflict, server_error)


usuarios_bp = Blueprint("usuarios", __name__) 



@usuarios_bp.route("/", methods=['GET'])
def listar_usuarios():


    try:
        
        connector = get_connection()
        cursor = connector.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()

        cursor.close()
        connector.close()

        if not usuarios:
            cursor.close()
            connector.close()
        
            return jsonify(not_found), 404
    
        return jsonify(usuarios), 200

    except Exception as e:
        error = server_error
        error['errors'[0]['description']] = str(e) # Para que pueda leer el Json


        return jsonify(error), 500



@usuarios_bp.route("/<int:id>", methods=['GET'])
def listar_por_id(id):

    if id <= 0:
        return jsonify(bad_request), 400
    
    try: 

        connector = get_connection()
        cursor = connector.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))

        usuario = cursor.fetchone()

        if not usuario:
            cursor.close()
            connector.close()

            return jsonify(not_found), 404
    
        if usuario.get("created_at"):
            usuario["created_at"] = str(usuario["created_at"]) # PAra evitar los errores de Data Type

        return jsonify(usuario), 200
    
    except Exception as e:

        error = server_error
        error["errors"][0]["description"] = str(e)

        return jsonify(server_error), 500
    
    finally:
        cursor.close()
        connector.close()



# Crear usuario

@usuarios_bp.route("/", methods=['POST'])
def crear_usuario():


    data = request.get_json()
    usuario = data.get('usuario')
    mail = data.get('mail')
    id = data.get('id_usuario')



    if not usuario or not mail:
        return jsonify(bad_request), 400
    
    try:

        connector = get_connection()
        cursor = connector.cursor(dictionary=True)



        cursor.execute("""
                   INSERT INTO usuarios
                   (usuario,
                    mail)
                   VALUES (%s, %s)""", (usuario, mail))

        if cursor.fetchone():
            return jsonify(conflict), 409
        

        connector.commit()

        return jsonify({'message' : 'Usuario creado correctamente'}), 201
    
    except Exception:
        return jsonify(server_error), 500
    
    finally:
        cursor.close()
        connector.close()




# Actualizar

@usuarios_bp.route("/<int:id>", methods=['PUT'])
def modificar_usuario(id, usuario=None, mail=None):

    if id <= 0:
        return jsonify(bad_request), 400


    try: 
        connector = get_connection()
        cursor = connector.cursor(dictionary=True)
        cursor.execute("Select * FROM usuarios WHERE id = %s", (id,))
        usuario = cursor.fetchone()

        if not usuario:

            return jsonify(not_found), 404
    
        data = request.json
        usuario = data.get('usuario')
        mail = data.get('mail')

        cursor.execute("""
                    UPDATE usuarios
                    SET usuario = %s,
                       mail = %s
                    WHERE id = %s;
            """, (usuario, mail, id))
    
        connector.commit()

        return jsonify({'Guardado' : 'Usuario actualizado correctamente'}), 200
    
    except Exception:

        return jsonify(server_error), 500

    finally:
        cursor.close()
        connector.close()

    

# Borrar ----> Terminar de ver por que no esta funcionando
@usuarios_bp.route("/<int:id>", methods=['DELETE'])
def eliminar_usuario(id):

    if id <= 0:
        return jsonify(not_found), 404


    try:
        connector = get_connection()
        cursor = connector.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
        usuario = cursor.fetchone()

        if not usuario:
            cursor.close()
            connector.close

            return jsonify(not_found), 404
    
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        connector.commit()

        return jsonify({'message' : 'Usuario borrado correctamente'}), 200
    
    except Exception:

        return jsonify(server_error), 500

    finally:
        cursor.close()
        connector.close()

    
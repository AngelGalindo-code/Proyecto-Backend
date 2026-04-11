from flask import Blueprint, jsonify, request

partidos_bp = Blueprint("partidos", __name__)

@partidos_bp.route('/partidos', methods=['GET'])

def listar_partidos():

    equipo = request.args.get('equipo')
    
    fecha = request.args.get('fecha')

    fase = request.args.get('fase')

    fases_validas = ['grupos', 'dieciseisavos', 'octavos', 'cuartos', 'semis', 'final']

    if fase and fase.lower() not in fases_validas:
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

    limit = request.args.get('limit', default=10, type=int)
    offset = request.args.get('offset', default=0, type=int)

    lista_de_partidos = [
        {
            "id": 1,
            "equipo_local": "Argentina",
            "equipo_visitante": "Brazil",
            "fecha": "2025-05-19",
            "fase": "GRUPOS"
        }
    ]
    return jsonify(lista_de_partidos), 200

@partidos_bp.route('/partidos', methods=['POST'])
def crear_partido():

    return jsonify({"mensaje": "Partido creado"}), 201



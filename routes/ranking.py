from flask import Blueprint, request, jsonify
from db import get_connection
ranking_bp = Blueprint("ranking", __name__)


@ranking_bp.route("/ranking", methods=["GET"])
def obtener_ranking_usuarios():
    limit = request.args.get(
        "_limit", default=10, type=int
    )  # cantidad de apariciones por pagina
    offset = request.args.get(
        "_offset", default=0, type=int
    )  # posicion desde donde empieza a leer
    if limit is None or offset is None or limit <= 0 or offset < 0:
        error_400 = {
            "errors": [
                {
                    "code": "400",
                    "message": "Bad Request",
                    "level": "error",
                    "description": "El limit o el offset tienen un dato invalido o son negativos",
                }
            ]
        }
        return jsonify(error_400), 400

    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        ranking = []

        cur.execute(
            """
        SELECT r.id_partido, 
        r.goles_local, 
        r.goles_visitante, 
        p.id_usuario, 
        p.prediccion_goles_local, 
        p.prediccion_goles_visitante
        FROM resultados r
        INNER JOIN predicciones p
        ON r.id_partido = p.id_partido 
        """
        )

        usuarios = cur.fetchall()
        puntaje_usuarios = {}
        for usuario in usuarios:
            id_usuario = usuario["id_usuario"]
            goles_local = usuario["goles_local"]
            predi_local = usuario["prediccion_goles_local"]
            goles_visitante = usuario["goles_visitante"]
            predi_visitante = usuario["prediccion_goles_visitante"]
            if goles_local is None or goles_visitante is None:
                puntos = 0

            elif goles_local == predi_local and goles_visitante == predi_visitante:
                puntos = 3

            elif (
                (goles_local > goles_visitante and predi_local > predi_visitante)
                or (goles_local < goles_visitante and predi_local < predi_visitante)
                or (goles_local == goles_visitante and predi_local == predi_visitante)
            ):
                puntos = 1

            else:
                puntos = 0

            puntaje_usuarios[id_usuario] = puntaje_usuarios.get(id_usuario, 0) + puntos

        puntajes_ordenados = sorted(  # convierte el diccionario en una lista de tuplas y ordena por el segundo elemento de cada una
            puntaje_usuarios.items(), key=lambda x: x[1], reverse=True
        )
        for id_usuario, puntos in puntajes_ordenados:
            ranking.append({"id_usuario": id_usuario, "puntos": puntos})

        cantidad_usuarios = len(ranking)
        if offset >= cantidad_usuarios:
            error_400 = {
                "errors": [
                    {
                        "code": "400",
                        "message": "Bad Request",
                        "level": "error",
                        "description": "El offset excede la cantidad de usuarios en el ranking",
                    }
                ]
            }
            return jsonify(error_400), 400
        ranking = ranking[offset : offset + limit]
        primera_pagina = 0
        pagina_anterior = 0 if offset - limit < 0 else offset - limit
        ultima_pagina = ((cantidad_usuarios - 1) // limit) * limit
        pagina_siguiente = (
            ultima_pagina if offset + limit >= cantidad_usuarios else offset + limit
        )

        links = {
            "_first": {
                "href": f"http://localhost:5000/ranking?_offset={primera_pagina}&_limit={limit}"
            },
            "_prev": {
                "href": f"http://localhost:5000/ranking?_offset={pagina_anterior}&_limit={limit}"
            },
            "_next": {
                "href": f"http://localhost:5000/ranking?_offset={pagina_siguiente}&_limit={limit}"
            },
            "_last": {
                "href": f"http://localhost:5000/ranking?_offset={ultima_pagina}&_limit={limit}"
            },
        }

        return jsonify({"ranking": ranking, "_links": links}), 200

    except Exception as e:
        error_500 = {
            "errors": [
                {
                    "code": "500",
                    "message": "Internal Server Error",
                    "level": "error",
                    "description": str(e),
                }
            ]
        }
        return jsonify(error_500), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

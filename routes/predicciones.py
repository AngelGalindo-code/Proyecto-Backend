from flask import Blueprint, jsonify, request

predicciones_bp = Blueprint("predicciones", __name__)

@predicciones_bp.route('/partidos/<int:id>/prediccion', methods=['POST'])
def registrar_prediccion(id):
    
    return jsonify({"mensaje": "Prediccion registrada"}), 201

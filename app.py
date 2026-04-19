from flask import Flask

from routes.partidos import partidos_bp
from routes.usuarios import usuarios_bp
from routes.predicciones import predicciones_bp
from routes.resultados import resultados_bp
from routes.ranking import ranking_bp

app = Flask(__name__)

app.register_blueprint(partidos_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(predicciones_bp)
app.register_blueprint(resultados_bp)
app.register_blueprint(ranking_bp)


app = Flask(__name__)

if __name__ == "__main__":
    app.run(port=8080, debug=True)
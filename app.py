from flask import Flask
from routes.partidos import partidos_bp

app = Flask(__name__)

app.register_blueprint(partidos_bp)

if __name__ == "__main__":
    app.run(port=8080, debug=True)
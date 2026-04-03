from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "¡Hola mundo!" 

# Configuramos el servidor Web para que se ejecute en el puerto 8080
if __name__ == "__main__":
    app.run(port=8080, debug=True)
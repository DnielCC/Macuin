from flask import Flask, jsonify, request

app = Flask(__name__)

# Ruta de prueba (Health check)
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "online",
        "project": "MACUIN - Access Control",
        "service": "Flask API"
    })

# Ejemplo de una ruta para recibir datos (POST)
@app.route('/api/access', methods=['POST'])
def log_access():
    data = request.get_json()
    # Aquí iría tu lógica de validación o guardado
    return jsonify({"message": "Access logged", "data": data}), 201

if __name__ == '__main__':
    # Usamos el puerto 5001 para no chocar con Laravel
    # host='0.0.0.0' permite que se vea en tu red local si es necesario
    app.run(host='0.0.0.0', port=5001, debug=True)
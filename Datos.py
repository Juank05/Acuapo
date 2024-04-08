from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

class Sensor:
    def __init__(self, nombre):
        self.nombre = nombre
        self.datos = None

    def agregar_dato(self, dato):
        self.datos = dato   

sensores = {
    "PH": Sensor("phValue"),
    "Temperatura" : Sensor("temperatura")
}

@app.route('/data', methods=['POST'])
def recibir_datos():
    datos = request.json
    for nombre_sensor, valor in datos.items():
        if nombre_sensor in sensores:
            sensor = sensores[nombre_sensor]
            sensor.agregar_dato(valor)
            print("Datos recibidos para el sensor '{}': {}".format(sensor.nombre, valor))
        else:
            print("Sensor desconocido: {}".format(nombre_sensor))
    return "Datos recibidos correctamente"

@app.route('/', methods=['GET'])
def mostrar_datos():
    datos_sensor = {nombre: sensor.datos for nombre, sensor in sensores.items()}
    return render_template('index.html', datos=datos_sensor)

# Ruta para manejar la solicitud GET de los datos de sensores
@app.route('/datos-sensores', methods=['GET'])
def obtener_datos_sensores():
    datos_sensor = {nombre: sensor.datos for nombre, sensor in sensores.items()}
    return jsonify(datos_sensor)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

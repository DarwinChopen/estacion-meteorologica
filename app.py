import os

from flask import Flask, render_template_string, request, jsonify
from datetime import datetime, timezone

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY", "clave-prueba-local")

datos_estacion = {
    "temperatura": 0,
    "humedad": 0,
    "presion": 0,
    "velocidad_viento": 0,
    "direccion_viento": "--",
    "lluvia": 0,
    "sensacion": 0,
    "ultima_actualizacion": "--:--:--"
}

ultima_recepcion = None
HTML = """
<!DOCTYPE html>

<html lang="es">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Estación Meteorológica</title>


    <style>

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Arial, sans-serif;
        }


        body {

            min-height: 100vh;

            background:
                linear-gradient(
                    135deg,
                    #0ea5e9,
                    #2563eb,
                    #4f46e5
                );

            padding: 35px 20px;

            color: white;
        }


        .contenedor {

            width: 95%;
            max-width: 1250px;

            margin: auto;
        }


        /* =========================
           ENCABEZADO
        ========================= */

        .encabezado {

            display: flex;

            justify-content: space-between;

            align-items: center;

            flex-wrap: wrap;

            margin-bottom: 30px;
        }


        .titulo h1 {

            font-size: 40px;

            font-weight: 700;
        }


        .titulo p {

            margin-top: 5px;

            font-size: 17px;

            opacity: 0.85;
        }


        .estado {

            background: rgba(255,255,255,0.18);

            backdrop-filter: blur(10px);

            padding: 12px 20px;

            border-radius: 30px;

            box-shadow:
                0 5px 20px rgba(0,0,0,0.15);
        }


        .online {

            color: #86efac;

            font-weight: bold;
        }


        .offline {

            color: #fca5a5;

            font-weight: bold;
        }


        /* =========================
           PANEL PRINCIPAL
        ========================= */

        .principal {

            background:
                linear-gradient(
                    135deg,
                    #38bdf8,
                    #0284c7
                );

            border-radius: 25px;

            padding: 35px;

            margin-bottom: 25px;

            box-shadow:
                0 12px 30px rgba(0,0,0,0.20);

            display: flex;

            justify-content: space-between;

            align-items: center;

            flex-wrap: wrap;
        }


        .principal-info h2 {

            font-size: 20px;

            opacity: 0.9;
        }


        .temperatura {

            font-size: 75px;

            font-weight: bold;

            margin-top: 5px;
        }


        .clima {

            font-size: 18px;

            margin-top: 5px;
        }


        .principal-icono {

            font-size: 110px;
        }


        /* =========================
           TARJETAS
        ========================= */

        .tarjetas {

            display: grid;

            grid-template-columns:
                repeat(auto-fit, minmax(240px, 1fr));

            gap: 20px;
        }


        .tarjeta {

            border-radius: 22px;

            padding: 25px;

            min-height: 210px;

            box-shadow:
                0 10px 25px rgba(0,0,0,0.18);

            transition:
                transform 0.3s,
                box-shadow 0.3s;
        }


        .tarjeta:hover {

            transform: translateY(-7px);

            box-shadow:
                0 15px 35px rgba(0,0,0,0.25);
        }


        /* =========================
           COLORES DE TARJETAS
        ========================= */

        .humedad {

            background:
                linear-gradient(
                    135deg,
                    #06b6d4,
                    #0891b2
                );
        }


        .presion {

            background:
                linear-gradient(
                    135deg,
                    #8b5cf6,
                    #6d28d9
                );
        }


        .viento {

            background:
                linear-gradient(
                    135deg,
                    #22c55e,
                    #15803d
                );
        }


        .direccion {

            background:
                linear-gradient(
                    135deg,
                    #f59e0b,
                    #ea580c
                );
        }


        .lluvia {

            background:
                linear-gradient(
                    135deg,
                    #3b82f6,
                    #1d4ed8
                );
        }


        .sensacion {

            background:
                linear-gradient(
                    135deg,
                    #ef4444,
                    #be123c
                );
        }


        .icono {

            font-size: 43px;
        }


        .tarjeta h3 {

            margin-top: 15px;

            font-size: 17px;

            opacity: 0.9;
        }


        .dato {

            font-size: 38px;

            font-weight: bold;

            margin-top: 8px;
        }


        .unidad {

            font-size: 18px;

            font-weight: normal;

            opacity: 0.85;
        }


        .sensor {

            margin-top: 12px;

            font-size: 13px;

            opacity: 0.75;
        }


        /* =========================
           INFORMACIÓN DEL SISTEMA
        ========================= */

        .sistema {

            margin-top: 25px;

            background:
                rgba(255,255,255,0.16);

            backdrop-filter: blur(12px);

            border-radius: 20px;

            padding: 20px;

            display: grid;

            grid-template-columns:
                repeat(auto-fit, minmax(180px,1fr));

            gap: 15px;

            text-align: center;
        }


        .sistema span {

            display: block;

            font-size: 13px;

            opacity: 0.75;

            margin-bottom: 5px;
        }


        .sistema strong {

            font-size: 17px;
        }


        footer {

            text-align: center;

            margin-top: 25px;

            font-size: 13px;

            opacity: 0.7;
        }


        /* =========================
           DISEÑO PARA CELULAR
        ========================= */

        @media(max-width:600px) {


            .titulo h1 {

                font-size: 30px;
            }


            .estado {

                margin-top: 15px;
            }


            .temperatura {

                font-size: 55px;
            }


            .principal-icono {

                font-size: 80px;
            }


            .principal {

                padding: 25px;
            }

        }

    </style>

</head>


<body>


<div class="contenedor">


    <!-- =========================
         ENCABEZADO
    ========================== -->

    <div class="encabezado">


        <div class="titulo">

            <h1>
                🌦️ Estación Meteorológica UDEO 2026 Tele-Datos 2
            </h1>

            <p>
                Sistema de monitoreo ambiental en tiempo real
            </p>

        </div>


        <div class="estado">

            ESP32-S3

            <span id="estado-superior"
                  class="offline">

                ● DESCONECTADO

            </span>

        </div>


    </div>


    <!-- =========================
         TEMPERATURA
    ========================== -->

    <div class="principal">


        <div class="principal-info">


            <h2>
                Temperatura actual
            </h2>


            <div class="temperatura">

                <span id="temperatura">
                    {{ temperatura }}
                </span>

                °C

            </div>


            <div class="clima">

                🌤️ Condiciones ambientales actuales

            </div>


        </div>


        <div class="principal-icono">

            🌤️

        </div>


    </div>


    <!-- =========================
         TARJETAS
    ========================== -->

    <div class="tarjetas">


        <!-- HUMEDAD -->

        <div class="tarjeta humedad">


            <div class="icono">

                💧

            </div>


            <h3>

                Humedad relativa

            </h3>


            <div class="dato">

                <span id="humedad">

                    {{ humedad }}

                </span>

                <span class="unidad">

                    %

                </span>

            </div>


            <div class="sensor">

                Higrómetro • BME280

            </div>


        </div>


        <!-- PRESIÓN -->

        <div class="tarjeta presion">


            <div class="icono">

                🌬️

            </div>


            <h3>

                Presión atmosférica

            </h3>


            <div class="dato">

                <span id="presion">

                    {{ presion }}

                </span>


                <span class="unidad">

                    hPa

                </span>

            </div>


            <div class="sensor">

                Barómetro • BME280

            </div>


        </div>


        <!-- VELOCIDAD DEL VIENTO -->

        <div class="tarjeta viento">


            <div class="icono">

                💨

            </div>


            <h3>

                Velocidad del viento

            </h3>


            <div class="dato">

                <span id="velocidad_viento">

                    {{ velocidad_viento }}

                </span>


                <span class="unidad">

                    km/h

                </span>

            </div>


            <div class="sensor">

                Anemómetro

            </div>


        </div>


        <!-- DIRECCIÓN DEL VIENTO -->

        <div class="tarjeta direccion">


            <div class="icono">

                🧭

            </div>


            <h3>

                Dirección del viento

            </h3>


            <div class="dato">

                <span id="direccion_viento">

                    {{ direccion_viento }}

                </span>

            </div>


            <div class="sensor">

                Veleta

            </div>


        </div>


        <!-- LLUVIA -->

        <div class="tarjeta lluvia">


            <div class="icono">

                🌧️

            </div>


            <h3>

                Precipitación

            </h3>


            <div class="dato">

                <span id="lluvia">

                    {{ lluvia }}

                </span>


                <span class="unidad">

                    mm

                </span>

            </div>


            <div class="sensor">

                Pluviómetro

            </div>


        </div>


        <!-- SENSACIÓN TÉRMICA -->

        <div class="tarjeta sensacion">


            <div class="icono">

                🌡️

            </div>


            <h3>

                Sensación térmica

            </h3>


            <div class="dato">

                <span id="sensacion">

                    {{ sensacion }}

                </span>


                <span class="unidad">

                    °C

                </span>

            </div>


            <div class="sensor">

                Valor calculado

            </div>


        </div>


    </div>


    <!-- =========================
         INFORMACIÓN DEL SISTEMA
    ========================== -->

    <div class="sistema">


        <div>

            <span>
                Microcontrolador
            </span>

            <strong>
                ESP32-S3 Arduino Mega 
            </strong>

        </div>
            <span>
                Intgrantes:
            </span>

            <strong>
                Darwin Panjoj Chopen
                Keneth Gomez Cifuentes
                Carlos Perez Sanchez
                
            </strong>        


        <div>

            <span>
                Sensor ambiental
            </span>

            <strong>
                BME280
            </strong>

        </div>


        <div>

            <span>
                Estado
            </span>

            <strong id="estado-inferior"
                    class="offline">

                ● Desconectado

            </strong>

        </div>


        <div>

            <span>

                Última actualización

            </span>


            <strong>

                <span id="ultima_actualizacion">

                    {{ hora }}

                </span>

            </strong>

        </div>


    </div>


    <footer>

        Estación Meteorológica • ESP32-S3 • Flask • 2026

    </footer>


</div>


<!-- =====================================================
     JAVASCRIPT
     ACTUALIZACIÓN AUTOMÁTICA
====================================================== -->

<script>


    async function actualizarDatos() {


        try {


            // ==========================================
            // CONSULTAR API
            // ==========================================

            const respuesta =
                await fetch("/api/datos");


            if (!respuesta.ok) {

                throw new Error(
                    "No se pudieron obtener los datos"
                );

            }


            const datos =
                await respuesta.json();


            // ==========================================
            // ACTUALIZAR MEDICIONES
            // ==========================================

            document
                .getElementById("temperatura")
                .textContent =
                datos.temperatura;


            document
                .getElementById("humedad")
                .textContent =
                datos.humedad;


            document
                .getElementById("presion")
                .textContent =
                datos.presion;


            document
                .getElementById("velocidad_viento")
                .textContent =
                datos.velocidad_viento;


            document
                .getElementById("direccion_viento")
                .textContent =
                datos.direccion_viento;


            document
                .getElementById("lluvia")
                .textContent =
                datos.lluvia;


            document
                .getElementById("sensacion")
                .textContent =
                datos.sensacion;


            document
                .getElementById("ultima_actualizacion")
                .textContent =
                datos.ultima_actualizacion;


            // ==========================================
            // ESTADO DEL ESP32
            // ==========================================

            const estadoSuperior =
                document.getElementById(
                    "estado-superior"
                );


            const estadoInferior =
                document.getElementById(
                    "estado-inferior"
                );


            if (datos.conectado) {


                estadoSuperior.textContent =
                    "● EN LÍNEA";


                estadoSuperior.className =
                    "online";


                estadoInferior.textContent =
                    "● Conectado";


                estadoInferior.className =
                    "online";


            }

            else {


                estadoSuperior.textContent =
                    "● DESCONECTADO";


                estadoSuperior.className =
                    "offline";


                estadoInferior.textContent =
                    "● Desconectado";


                estadoInferior.className =
                    "offline";


            }


        }


        catch (error) {


            console.error(
                "Error actualizando datos:",
                error
            );


        }


    }


    // Primera consulta al cargar la página

    actualizarDatos();


    // Consultar nuevamente cada 5 segundos

    setInterval(
        actualizarDatos,
        5000
    );


</script>


</body>

</html>
"""

@app.route("/")
def inicio():

    return render_template_string(

        HTML,

        temperatura=datos_estacion["temperatura"],

        humedad=datos_estacion["humedad"],

        presion=datos_estacion["presion"],

        velocidad_viento=datos_estacion[
            "velocidad_viento"
        ],

        direccion_viento=datos_estacion[
            "direccion_viento"
        ],

        lluvia=datos_estacion["lluvia"],

        sensacion=datos_estacion["sensacion"],

        hora=datos_estacion[
            "ultima_actualizacion"
        ]

    )



@app.route("/api/datos", methods=["GET"])
def obtener_datos():

    conectado = False
    if ultima_recepcion is not None:


        ahora = datetime.now(
            timezone.utc
        )


        segundos_transcurridos = (

            ahora - ultima_recepcion

        ).total_seconds()

        if segundos_transcurridos <= 30:

            conectado = True


    respuesta = datos_estacion.copy()


    respuesta["conectado"] = conectado


    return jsonify(
        respuesta
    )

@app.route("/api/datos", methods=["POST"])
def recibir_datos():

    global ultima_recepcion
    clave_recibida = request.headers.get("X-API-Key")

    if clave_recibida != API_KEY:

        return jsonify({
            "estado": "error",
            "mensaje": "No autorizado"
        }), 401

    nuevos_datos = request.get_json(
        silent=True
    )

    if not nuevos_datos:


        return jsonify({

            "estado": "error",

            "mensaje":
                "No se recibieron datos"

        }), 400

    campos_permitidos = [

        "temperatura",

        "humedad",

        "presion",

        "velocidad_viento",

        "direccion_viento",

        "lluvia",

        "sensacion"

    ]

    for campo in campos_permitidos:


        if campo in nuevos_datos:


            datos_estacion[campo] = \
                nuevos_datos[campo]

    ultima_recepcion = datetime.now(
        timezone.utc
    )

    datos_estacion[
        "ultima_actualizacion"
    ] = datetime.now().strftime(
        "%H:%M:%S"
    )

    return jsonify({

        "estado": "ok",

        "mensaje":
            "Datos recibidos correctamente",

        "datos":
            datos_estacion

    })

if __name__ == "__main__":


    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )

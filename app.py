from flask import Flask, render_template_string
from datetime import datetime

app = Flask(__name__)

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

            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }


        .online {

            color: #86efac;

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


        /* COLORES DE LAS TARJETAS */


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

            background: rgba(255,255,255,0.16);

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


    <!-- ENCABEZADO -->


    <div class="encabezado">


        <div class="titulo">

            <h1>🌦️ Estación Meteorológica</h1>

            <p>
                Sistema de monitoreo ambiental en tiempo real
            </p>

        </div>


        <div class="estado">

            ESP32-S3

            <span class="online">
                ● EN LÍNEA
            </span>

        </div>


    </div>



    <!-- PANEL PRINCIPAL -->


    <div class="principal">


        <div class="principal-info">

            <h2>Temperatura actual</h2>


            <div class="temperatura">

                {{ temperatura }} °C

            </div>


            <div class="clima">

                🌤️ Condiciones ambientales actuales

            </div>


        </div>


        <div class="principal-icono">

            🌤️

        </div>


    </div>



    <!-- TARJETAS -->


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

                {{ humedad }}

                <span class="unidad">
                    %
                </span>

            </div>


            <div class="sensor">

                Higrómetro • BME280

            </div>

        </div>



        <!-- PRESION -->


        <div class="tarjeta presion">

            <div class="icono">
                🌬️
            </div>


            <h3>
                Presión atmosférica
            </h3>


            <div class="dato">

                {{ presion }}

                <span class="unidad">
                    hPa
                </span>

            </div>


            <div class="sensor">

                Barómetro • BME280

            </div>

        </div>



        <!-- VELOCIDAD VIENTO -->


        <div class="tarjeta viento">

            <div class="icono">
                💨
            </div>


            <h3>
                Velocidad del viento
            </h3>


            <div class="dato">

                {{ velocidad_viento }}

                <span class="unidad">
                    km/h
                </span>

            </div>


            <div class="sensor">

                Anemómetro

            </div>

        </div>



        <!-- DIRECCION -->


        <div class="tarjeta direccion">

            <div class="icono">
                🧭
            </div>


            <h3>
                Dirección del viento
            </h3>


            <div class="dato">

                {{ direccion_viento }}

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

                {{ lluvia }}

                <span class="unidad">
                    mm
                </span>

            </div>


            <div class="sensor">

                Pluviómetro

            </div>

        </div>



        <!-- SENSACION TERMICA -->


        <div class="tarjeta sensacion">

            <div class="icono">
                🌡️
            </div>


            <h3>
                Sensación térmica
            </h3>


            <div class="dato">

                {{ sensacion }}

                <span class="unidad">
                    °C
                </span>

            </div>


            <div class="sensor">

                Valor calculado

            </div>

        </div>


    </div>



    <!-- INFORMACION DEL SISTEMA -->


    <div class="sistema">


        <div>

            <span>
                Microcontrolador
            </span>

            <strong>
                ESP32-S3
            </strong>

        </div>


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

            <strong class="online">
                ● Conectado
            </strong>

        </div>


        <div>

            <span>
                Última actualización
            </span>

            <strong>
                {{ hora }}
            </strong>

        </div>


    </div>



    <footer>

        Estación Meteorológica • ESP32-S3 • Flask • 2026

    </footer>


</div>


</body>

</html>
"""


@app.route("/")
def inicio():

    # =====================================
    # DATOS DE PRUEBA
    # Luego serán recibidos desde ESP32-S3
    # =====================================

    temperatura = 24.5

    humedad = 65

    presion = 1013.2

    velocidad_viento = 12.4

    direccion_viento = "NE"

    lluvia = 3.2

    sensacion = 25.1


    hora = datetime.now().strftime("%H:%M:%S")


    return render_template_string(

        HTML,

        temperatura=temperatura,

        humedad=humedad,

        presion=presion,

        velocidad_viento=velocidad_viento,

        direccion_viento=direccion_viento,

        lluvia=lluvia,

        sensacion=sensacion,

        hora=hora

    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
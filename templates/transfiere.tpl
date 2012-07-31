<!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="utf-8">
        <title>Replicador de entornos</title>
        <link rel="stylesheet" type="text/css" href="style.css" />

        <script type='text/javascript' src='jquery-1.7.2.min.js'></script>
        <script type='text/javascript' src='js.js'></script>
    </head>
    <body topmargin="0" leftmargin="0">
        <header>
            <div>
                <h1>Replicador de entornos</h1>
            </div>

            <div>

            </div>
        </header>Genera el codigo HTML de la pagina
        <article>
            <br>
            {{ resultado }}<br>
            {% for arch in archivosCorrecto %}
                <b>{{ arch }}</b><br>
            {% endfor %}
            <br>
            <hr>
            Error al copiar:<br>
            {% for arch in archivosError %}
                <b>{{ arch }}</b><br>
            {% endfor %}
            <br>
            <br>
            <button onclick='javascript:window.location = "/copiador"'>
                REGRESAR AL MENU PRICIPAL
            </button>
        </article>
        <footer>
            <center>
            Develope by marcelo.martinovic@gmail.com - I.T.Y.O.O.L.G 2012
            </center>
        </footer>
    </body>
</html>

<!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="utf-8">
        <title>Replicador de entornos</title>
        <link rel="stylesheet" type="text/css" href="style.css" />
        <script type='text/javascript' src='jquery-1.7.2.min.js'></script>
        <script type='text/javascript' src='js.js'></script>
        <script type="text/javascript" src="noty/jquery.noty.js"></script>
        <script type="text/javascript" src="noty/layouts/center.js"></script>
        <script type="text/javascript" src="noty/themes/default.js"></script>
        <style type="text/css">
            html {height: 100%;
                width: 100%;}
            body {font-family: 'PT Sans', Tahoma, Arial, serif;
                line-height: 13px}
        </style>
        <link rel="stylesheet" type="text/css" href="buttons.css"/>
        <script type="text/javascript">
            function generate(layout, msg, type) {
                var n = noty({
                      text: msg,
                      type: type,
                      dismissQueue: false,
                      layout: layout,
                      theme: 'default'
                });
                console.log('html: '+n.options.id);
            }
        </script>
    </head>
    <body topmargin="0" leftmargin="0">
        <header>
            <form action="limpieza" method="post" name="form1" id="form1">
            <div>
                <h1>Replicador de entornos</h1>
            </div>
            <!-- botones de acciones -->
            <div>
                <input type='submit' value='Iniciar borrado de archivos'
                    name='submit' style='background-color:red;'
                    onclick="generate('center', 'Iniciando la copia...', 'information');">
                <input type='reset' value='Cancelar la seleccion' name='reset'>
                <input type='hidden' value='{{ entornoSeleccionado }}' name='entorno'>
                <input type='hidden' value='{{ filtroSeleccionado }}' name='filtro'>
            </div>
        </header>
        Genera el codigo HTML de la pagina
        <article>
            <center>
                <font color='red' size='+1'>
                DEBE TENER EN CUENTA QUE UNA VEZ QUE<br><br>
                INDIQUE EL BORRADO DE LOS ARCHIVOS NO <br><br>
                PODRAN SER RECUPERADOS
                </font>
            </center>
        </article>
        <article>
            <table width='90%' cellpadding='2' cellspacing='1'>
                <tr>
                    <th>Archivo</th>
                </tr>
                {% for item in lista %}
                <tr>
                    <td>
                        <input type="checkbox"
                        name="filename" value="{{ item.archivo }}">
                            {{ item.archivo }}
                    </td>
                </tr>
                {% endfor %}
            </table>
        </article>
        </form>
        <footer>
            <center>
            Develope by marcelo.martinovic@gmail.com - I.T.Y.O.O.L.G 2012<br>
            Powered by Python
            <img src="imagenes/480px-Logo_Python.png"
                height="25px" align="absmiddle">
            </center>
        </footer>
    </body>
</html>

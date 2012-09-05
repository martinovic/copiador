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
            function generate(layout, msg) {
                var n = noty({
                      text: msg,
                      type: 'alert',
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
            <div>
                <h1>Replicador de entornos</h1>
            </div>

            <div>

            </div>
        </header>Genera el codigo HTML de la pagina
        <article>
            <br>
            {{ resultado }}<br>
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

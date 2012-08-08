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
            <form action="transfiere" method="post" name="form1" id="form1">
            <div>
                <h1>Replicador de entornos</h1>
            </div>
            <!-- botones de acciones -->
            <div>
                <input type='submit' value='Iniciar la copia'
                    name='submit'
                    onclick="generate('center', 'Iniciando la copia...', 'information');">
                <input type='reset' value='Cancelar la seleccion' name='reset'>
                <label for="entorno" style='margin-left:200px;'>
                    Entornos destinos disponibles
                </label>
                <select name='entorno'>
                    <option value='127.0.0.1'
                        {% if entornoSeleccionado == '127.0.0.1' %}
                         selected
                        {% endif %}>Localhost</option>
                    <option value='192.168.0.202'
                        {% if entornoSeleccionado == '192.168.0.202' %}
                         selected
                        {% endif %}>Desarrollo</option>
                    <option value='192.168.0.244'
                        {% if entornoSeleccionado == '192.168.0.244' %}
                         selected
                        {% endif %}>Pre Productivo</option>
                </select>
                <input type='submit'
                    value='Seleccionar entorno'
                    name='entornoBtn'
                    onclick='submitirFormEntorno();'>

                <label for="filtro"  style='margin-left:50px;'>
                    Filtros disponibles
                </label>
                <select name='filtro'>
                    <option value='todos'
                        {% if filtroSeleccionado == 'todos' %}
                         selected
                        {% endif %}>Todos</option>
                    <option value='nuevos'
                        {% if filtroSeleccionado == 'nuevos' %}
                         selected
                        {% endif %}>Nuevos</option>
                    <option value='difieren'
                        {% if filtroSeleccionado == 'difieren' %}
                         selected
                        {% endif %}>Actualizables</option>
                    <option value='difierenynuevos'
                        {% if filtroSeleccionado == 'difierenynuevos' %}
                         selected
                        {% endif %}>Difieren o nuevos</option>
                    <option value='limpieza'
                        {% if filtroSeleccionado == 'limpieza' %}
                         selected
                        {% endif %}>No existen en origen</option>
                </select>
                <input type='submit'
                    value='Filtra'
                    name='filtarBtn'
                    onclick='submitirFiltro();'>
            </div>
        </header>
        Genera el codigo HTML de la pagina
        <article>
            <table width='90%' cellpadding='2' cellspacing='1'>
                <tr>
                    <th>Firma origen</th>
                    <th>Condicion</th>
                    <th>Archivo</th>
                    <th>Fecha Local</th>
                    <th>Fecha Destino</th>
                </tr>
                {% for item in lista %}
                <tr>
                    <td>{{ item.firma_md5}}</td>
                    <td>{{ item.condicion}}</td>
                    <td>
                        <input type="checkbox"
                        name="filename" value="{{ item.archivo }}" >
                            {{ item.archivo }}
                    </td>
                    <td>
                        {{ item.fechaLocal}}
                    </td>
                    <td>
                        {{ item.fechaRemoto }}
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

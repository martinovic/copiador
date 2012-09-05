"""
    App para poder usar WEB Services

    ---------------------------------------------------------------
    Nota:
    Para poder hacer uso de esta parte de la app
    se debe tener instalado web.py

    easy_install web.py

    ---------------------------------------------------------------
    Configuracion para integrarlo con apache 2.2:

    WSGIScriptAlias /copiador /var/www/copiador2/copiador.py
    WSGIScriptAlias /transfiere /var/www/copiador2/transfiere.py
    WSGIScriptAlias /recupera /var/www/copiador2/recuperaListadoArchivosJson.py
    WSGIScriptAlias /limpieza /var/www/copiador2/limpieza.py
    WSGIScriptAlias /limpiezaEjecuta /var/www/copiador2/limpiezaEjecuta.py
    WSGIScriptAlias /appRestService /var/www/copiador2/appRestService.py

    ScriptAlias /cgi-bin/ /usr/lib/cgi-bin/

    Alias /appRestService/static /var/www/copiador2/static
    AddType text/html .py

"""
__prj__ = 'Copiador'
__version__ = '1.0'
__license__ = 'GNU General Public License v3'
__author__ = 'marcelo'
__email__ = 'marcelo.martinovic@gmail.com'
__url__ = ''
__date__ = '2012/08/08'

import web
import json
import os

# Map of URL
urls = (
    '/(.*)', 'appRestService'
)
# Run server app


class appRestService:
    """
        This class conains GET and POST
    """
    def GET(self, name):
        """
            case of get request
        """
        print name
        return 'No allowed GET Method !!!'

    def POST(self, datos):
        """
            case of POST request
        """
        datosPost = json.loads(web.data())

        cantidadOriginal = len(datosPost["archivos"])
        cantidadBorrados = 0
        for toDelete in datosPost["archivos"]:
            try:
                os.remove(toDelete)
                cantidadBorrados += 1
            except:
                pass

        if cantidadOriginal == cantidadBorrados:
            mensaje = "OK"
        elif cantidadBorrados == 0:
            mensaje = "FAIL"
        elif cantidadOriginal > cantidadBorrados and cantidadBorrados >= 1:
            mensaje = "ERROR"
        else:
            mensaje = "UNDEFINED"

        resultadoReturn = {'fecha': datosPost["fecha"], 'estado': mensaje}

        return json.dumps(resultadoReturn)  # return value to test

application = web.application(urls, globals()).wsgifunc()

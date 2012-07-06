#!/usr/bin/python
import os
import hashlib
import sys
sys.path.append('/var/www/copiador2')
import templatesHtml

"""
Copiador de archivos para entornos
    :author: Marcelo Martinovic
    :version: 1.0
    :organization: Marcelo Martinovic
    :license: GPL
    :contact: marcelo dot martinovic at gmail dot com
    :note: Esta es una version para ser ejecutada en python 2.7+ no funciona en
            python3 por los cambios de mejoras del lenguaje
"""
__author__ = "marcelo martinovic"
__date__ = "$09/04/2012 16:53:44$"


def application(environ, start_response):
    """
        inicio
    """
    status = '200 OK'
    directorio = "/var/www/Portal2"
    outputData = generarHtml(directorio, environ)
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(outputData)))]
    start_response(status, response_headers)
    # print >> environ['wsgi.errors'], outputData
    return [outputData]


def md5Checksum(filePath):
    """
        Recover md5 of file content
    """
    fh = open(filePath, 'rb')
    m = hashlib.md5()
    while True:
        data = fh.read(8192)
        if not data:
            break
        m.update(data)
    return m.hexdigest()


def walkDirs(route):
    """
        Walk in dirs of specific route
    """
    dictFiles = {}
    for root, dirs, files in os.walk(route):
        if root.find(".svn") < 0:
            for f in files:
                fileWithRoute = "%s/%s" % (root, f)
                dictFiles[md5Checksum(fileWithRoute)] = fileWithRoute

    return dictFiles


def generarHtml(directorio, environ):
    """
        Generate HTML5 Code of page
        TODO: see the best method to use temples
    """
    outputData = templatesHtml.head
    outputData += """
        <body topmargin="0" leftmargin="0">
            <header>
                <div>
                    <h1>Replicador de entornos</h1>
                </div>

                <div>
                    <form action="transfiere" method="post">
                        <input type='submit'
                            value='Iniciar la copia' name='submit'>
                        <input type='reset'
                            value='Cancelar la seleccion' name='reset'>

                        <label for="entorno" style='margin-left:200px;'>
                            Entornos disponibles
                        </label>
                        <select name='entorno'>
                            <option
                                value='192.168.0.244'>Pre productivo</option>
                            <option
                                value='192.168.0.245'>Productivo</option>
                        </select>
                        <input type='submit'
                            value='Seleccionar entorno' name='entornoBtn'>

                        <label for="filtro"  style='margin-left:50px;'>
                            Filtros disponibles
                        </label>
                        <select name='filtro'>
                            <option
                                value='todos'>Todos</option>
                            <option
                                value='nuevos'>Nuevos</option>
                            <option
                                value='difieren'>Actualizables</option>
                        </select>
                        <input type='submit'
                            value='Filtra' name='filtarBtn'>

                </div>
            </header>Genera el codigo HTML de la pagina
            <article>
            <table>
                <tr>
                    <th>Firma origen</th>
                    <th>Archivo</th>
                </tr>"""

    diccionarioFiles_or = [x for x in walkDirs(directorio).iteritems()]
    diccionarioFiles_or.sort(key=lambda x: x[1])
    for codigo, files in diccionarioFiles_or:
        td = """<tr>
                    <td>%30s</td>
                    <td>
                        <input type="checkbox"
                        name="filename" value="%s" > %s
                    </td>
                </tr>"""
        outputData += (td % (codigo, files, files))

    outputData += """</table></article></form>
    <footer>
        <center>
        Develope by marcelo.martinovic@gmail.com - I.T.Y.O.O.L.G 2012
        </center>
    </footer>
    </body></html>"""
    print >> environ['wsgi.errors'], "application debug #2"
    return outputData

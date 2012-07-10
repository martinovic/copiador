#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import hashlib
import sys
from cgi import parse_qs
import StringIO
import pycurl
import simplejson
sys.path.append('/var/www/copiador2')
import templatesHtml
import configuracion

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
    entorno = ["127.0.0.1"]

    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    if request_body_size != 0:
        # When the method is POST the query string will be sent
        # in the HTTP request body which is passed by the WSGI server
        # in the file like wsgi.input environment variable.
        request_body = environ['wsgi.input'].read(request_body_size)
        d = parse_qs(request_body)
        entorno = d.get('entorno', 0)
        print >> environ['wsgi.errors'], entorno

    outputData = generarHtml(directorio, environ, entorno[0])
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


def walkDirs(environ, route, entorno):
    """
        Walk in dirs of specific route
        and remove specific entry of directory
    """
    dictFiles = {}
    condicion = "Nuevo"
    firmasRemotas, archivosRemotos = recuperaFirmas(peticionJson(entorno,
        environ))
    dirNoListables = configuracion.dirNoListables
    for root, dirs, files in os.walk(route):
        # Quita los directorios especificados
        for dirARemover in dirNoListables:
            if dirARemover in dirs:
                dirs.remove(dirARemover)
        for f in files:
            # Si el archivo es un svn lo ignora
            if f != '.svn':
                fileWithRoute = "%s/%s" % (root, f)
                chkSum = md5Checksum(fileWithRoute)
                if chkSum in firmasRemotas:
                    condicion = "<font color='blue'>IGUALES</font>"
                else:
                    if fileWithRoute in archivosRemotos:
                        condicion = "<font color='red'>UPDATE</font>"
                    else:
                        condicion = "<font color='green'>NUEVO</font>"
                dictFiles[chkSum] = [condicion, fileWithRoute]

    return dictFiles


def generarHtml(directorio, environ, entorno):
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
                <!-- botones de acciones -->
                <div>
                    <form action="transfiere" method="post"
                        name="form1" id="form1">
                        <input type='submit'
                            value='Iniciar la copia' name='submit'>
                        <input type='reset'
                            value='Cancelar la seleccion' name='reset'>

                        <label for="entorno" style='margin-left:200px;'>
                            Entornos disponibles
                        </label>
                        <select name='entorno'>
                            <option
                                value='127.0.0.1'>Localhost</option>
                            <option
                                value='192.168.0.202'>Desarrollo</option>
                            <option
                                value='192.168.0.244'>Pre Productivo</option>
                        </select>
                        <input type='submit'
                            value='Seleccionar entorno'
                            name='entornoBtn'
                            onclick='submitirFormEntorno();'>

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
                    <th>Condicion</th>
                    <th>Archivo</th>
                </tr>"""

    diccionarioFiles_or = [x for x in \
        walkDirs(environ, directorio, entorno).iteritems()]
    diccionarioFiles_or.sort(key=lambda x: x[1])
    for codigo, files in diccionarioFiles_or:
        td = """<tr>
                    <td>%30s</td>
                    <td>%s</td>
                    <td>
                        <input type="checkbox"
                        name="filename" value="%s" > %s
                    </td>
                </tr>"""
        outputData += (td % (codigo, files[0], files[1], files[1]))

    outputData += """</table></article></form>
    <footer>
        <center>
        Develope by marcelo.martinovic@gmail.com - I.T.Y.O.O.L.G 2012<br>
        Powered by Python
        <img src="imagenes/480px-Logo_Python.png"
            height="25px" align="absmiddle">
        </center>
    </footer>
    </body></html>"""
    return outputData


def peticionJson(entorno, environ):
    """
        :param peticion: peticion REST formada
    """
    protocolo = 'http'
    server = entorno
    port = '21000'
    peticion = ""

    largo = len(peticion)
    contentLenght = "Content-length: %s" % largo
    header = ["Content-type: application/json; " \
        + "charset=UTF-8", contentLenght, "Accept: application/json"]
    c = pycurl.Curl()
    url = protocolo + '://' + server + ':' + port + '/recupera'

    print >> environ['wsgi.errors'], url

    b = StringIO.StringIO()
    c.setopt(c.URL, url)
    c.setopt(c.HTTPHEADER, header)
    c.setopt(c.POST, True)
    c.setopt(c.POSTFIELDS, peticion)
    c.setopt(c.WRITEFUNCTION, b.write)  # esto es lo que captura los datos
    c.setopt(c.POSTFIELDSIZE, len(peticion))
    c.setopt(c.VERBOSE, False)  # True - Muestra los eventos de JSON
    c.perform()
    source = b.getvalue()
    c.close()
    try:
        resultado = simplejson.loads(source)
    except:
        print("*" * 100)
        print("URL: %s" % (url))
        print("*" * 100)
        print("Peticion: %s" % (peticion))
        print("*" * 100)
        print source
        print("*" * 100)
        raw_input("ha ocurrido un error")
        exit(0)
    return resultado["lista"]


def recuperaFirmas(jsonSource):
    """
        aplana el json y forma una lista para la busqueda
    """
    firmas = []
    archivos = []
    for v in jsonSource:
        firmas.append(v['codigo'])
        archivos.append(v['archivo'])
    return firmas, archivos

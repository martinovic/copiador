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
import configuracion
from jinja2 import Environment, FileSystemLoader


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
    # Trata de usar el entorno guardado si es que existe
    entorno = ["127.0.0.1"]

    filtro = ['todos']

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
        filtro = d.get('filtro', 0)
        print >> environ['wsgi.errors'], filtro

    outputData = generarHtml(directorio, environ, entorno[0], filtro)
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


def walkDirs(environ, route, entorno, filtro):
    """
        Walk in dirs of specific route
        and remove specific entry of directory
    """
    dictFiles = {}
    condicionHtml = "Nuevo"
    condicionFile = ""
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
                    condicionHtml = "<font color='blue'>IGUALES</font>"
                    condicionFile = "todos"
                    if filtro[0] == condicionFile:
                        dictFiles[chkSum] = [condicionHtml, fileWithRoute]
                else:
                    if fileWithRoute in archivosRemotos:
                        condicionHtml = "<font color='red'>UPDATE</font>"
                        condicionFile = "difieren"
                        if filtro[0] == condicionFile:
                            dictFiles[chkSum] = [condicionHtml, fileWithRoute]
                    else:
                        condicionHtml = "<font color='green'>NUEVO</font>"
                        condicionFile = "nuevos"
                        if filtro[0] == condicionFile:
                            dictFiles[chkSum] = [condicionHtml, fileWithRoute]
                if filtro[0] == 'todos':
                    dictFiles[chkSum] = [condicionHtml, fileWithRoute]
    return dictFiles


def generarHtml(directorio, environ, entorno, filtro):
    """
        Generate HTML5 Code of page with jinja2 templates
        :param directorio: directorio
        :param environ: environment
        :param entorno: entorno de destino
    """
    listDatos = []
    dictDatos = {}
    diccionarioFiles_or = [x for x in
        walkDirs(environ, directorio, entorno, filtro).iteritems()]
    diccionarioFiles_or.sort(key=lambda x: x[1])
    # Genera un diccionario con los datos
    # y luego lo agrega a una lista
    for codigo, files in diccionarioFiles_or:
        dictDatos["firma_md5"] = str(codigo)
        dictDatos["condicion"] = str(files[0])
        dictDatos["archivo"] = str(files[1])
        listDatos.append(dictDatos)
        dictDatos = {}

    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR + '/templates',
        encoding='utf-8'))

    outputData = j2_env.get_template('principal.tpl').render(lista=listDatos,
        entornoSeleccionado=entorno,
        filtroSeleccionado=filtro[0])
    # Es importante que este en el encode utf-8 para que no
    # existan errores de byte encode en wsgi
    return outputData.encode("utf-8")


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
    header = ["Content-type: application/json; "
        + "charset=UTF-8", contentLenght, "Accept: application/json"]
    c = pycurl.Curl()
    url = protocolo + '://' + server + ':' + port + '/recupera'

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

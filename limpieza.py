#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import pycurl
import simplejson
import StringIO
from cgi import parse_qs
import json
sys.path.append('/var/www/copiador2')
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
__prj__ = 'Copiador'
__version__ = '1.0'
__license__ = 'GNU General Public License v3'
__author__ = 'marcelo'
__email__ = 'marcelo.martinovic@gmail.com'
__url__ = ''
__date__ = '2012/08/08'


def application(environ, start_response):
    """
        inicio
    """
    status = '200 OK'

    # Trata de usar el entorno guardado si es que existe
    print >> environ['wsgi.errors'], "listaArchivos---------------------------"
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    outputData = "Algo paso..."
    if request_body_size != 0:
        # When the method is POST the query string will be sent
        # in the HTTP request body which is passed by the WSGI server
        # in the file like wsgi.input environment variable.
        request_body = environ['wsgi.input'].read(request_body_size)
        d = parse_qs(request_body)
        listaArchivos = d.get('filename', [])
        entorno = d.get('entorno', 0)
        outputData = resultScreen(listaDeArchivos(environ,
            listaArchivos,
            entorno))
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(outputData)))]
    start_response(status, response_headers)

    return [outputData]


def listaDeArchivos(environ, listToDelete, entorno):
    """
        Arma el listado de archivos
    """
    files = []
    for fileToDelete in listToDelete:
        files.append(fileToDelete)
    restCall = {'fecha': '08-08-2012', 'archivos': files}
    peticion = json.dumps(restCall)
    return peticionJson(entorno, environ, peticion)


def resultScreen(result):
    """
        OutPut Screen
        Esta es la pantalla que ofrece el resultado de la copia
        de los datos
    """
    if result == 'OK':
        stringResultado = "Archivos borrados de manera exitosa."
    elif result == 'FAIL':
        stringResultado = 'No se ha podido borrar ningun archivo.'
    elif result == 'ERROR':
        stringResultado = "Existen Errores en el borrado."

    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR + '/templates',
        encoding='utf-8'))
    outputData = j2_env.get_template('limpiezaEjecutada.tpl').\
        render(resultado=stringResultado)
    # Es importante que este en el encode utf-8 para que no
    # existan errores de byte encode en wsgi
    return outputData.encode("utf-8")


def peticionJson(entorno, environ, peticion):
    """
        :param peticion: peticion REST formada
    """
    protocolo = 'http'
    server = entorno[0]
    port = '21000'
    largo = len(peticion)
    contentLenght = "Content-length: %s" % largo
    header = ["Content-type: application/json; "
        + "charset=UTF-8", contentLenght, "Accept: application/json"]
    c = pycurl.Curl()
    url = protocolo + '://' + server + ':' + port + "/appRestService/"
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
        print >> environ['wsgi.errors'], url
        print >> environ['wsgi.errors'], peticion
        print >> environ['wsgi.errors'], source
        exit(0)

    return resultado["estado"]

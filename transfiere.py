#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import paramiko
import sys
sys.path.append('/var/www/copiador2')
from scp import SCPClient
from cgi import parse_qs
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
    outputData = readFilesToCopy(environ)
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(outputData)))]
    start_response(status, response_headers)
    return [outputData]


def readFilesToCopy(environ):
    """transfiere
        Read the list of files top copy
    """

    archivosCopiadosCorrecto = []
    archivosCopiadosError = []
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    # When the method is POST the query string will be sent
    # in the HTTP request body which is passed by the WSGI server
    # in the file like wsgi.input environment variable.
    request_body = environ['wsgi.input'].read(request_body_size)
    d = parse_qs(request_body)

    archivos = d.get('filename', [])  # Returns a list filename to copy
    entorno = d.get('entorno', 0)
    print >> environ['wsgi.errors'], "copiando a: %s " % str(entorno[0])
    # Inicia la copia de cada archivo via ssh
    for source in archivos:
        target = source
        try:
            copyFilesWithSSH(source, target, entorno)
            archivosCopiadosCorrecto.append(source)
        except:
            archivosCopiadosError.append(source)

    return resultScreen(True, archivosCopiadosCorrecto, archivosCopiadosError)


def copyFilesWithSSH(source, target, entorno):
    """
        Copy files using SSH protocol
    """
    #server = "192.168.0.202"
    server = entorno[0]
    port = 22
    user = "root"
    password = "chicago42195"
    ssh = createSSHClient(server, port, user, password)
    scp = SCPClient(ssh.get_transport())
    #scp.put(source, "/")
    scp.put(source, target)


def createSSHClient(server, port, user, password):
    """
        Create client
    """
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client


def resultScreen(result, archivosCopiadosCorrecto, archivosCopiadosError):
    """
        OutPut Screen
        Esta es la pantalla que ofrece el resultado de la copia
        de los datos
    """
    if result is True:
        stringResultado = "Archivos copiados de manera exitosa."
    else:
        stringResultado = "Existen Errores en la copia"

    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR + '/templates',
        encoding='utf-8'))
    outputData = j2_env.get_template('transfiere.tpl').\
        render(resultado=stringResultado,
            archivosCorrecto=archivosCopiadosCorrecto,
            archivosError=archivosCopiadosError)
    # Es importante que este en el encode utf-8 para que no
    # existan errores de byte encode en wsgi
    return outputData.encode("utf-8")

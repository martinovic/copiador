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
__author__ = "marcelo martinovic"
__date__ = "$09/04/2012 16:53:44$"


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
    """
        Read the list of files top copy
    """
    outputData = ""

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

    for listaCopiados in archivos:
        outputData += listaCopiados + "<br>"

    sourceTest = "/var/www/Portal2/SQL_SRC/portal_sql.txt"
    try:
        copyFilesWithSSH(sourceTest)
        return resultScreen(True)
    except:
        return resultScreen(False)


def copyFilesWithSSH(source):
    """
        Copy files using SSH protocol
    """
    server = "192.168.0.202"
    port = 22
    user = "root"
    password = "chicago42195"
    ssh = createSSHClient(server, port, user, password)
    scp = SCPClient(ssh.get_transport())
    scp.put(source, "/")


def createSSHClient(server, port, user, password):
    """
        Create client
    """
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client


def resultScreen(result):
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
        render(resultado=stringResultado)
    # Es importante que este en el encode utf-8 para que no
    # existan errores de byte encode en wsgi
    return outputData.encode("utf-8")

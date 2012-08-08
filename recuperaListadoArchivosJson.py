#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import hashlib
import sys
sys.path.append('/var/www/copiador2')
import configuracion
import time

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
    outputData = generarJson(directorio, environ)
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
        and remove specific entry of directory
    """
    dictFiles = {}
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
                dictFiles[md5Checksum(fileWithRoute)] = fileWithRoute
    return dictFiles


def generarJson(directorio, environ):
    """
        Return Json list with files in server
    """
    json = ""
    diccionarioFiles_or = [x for x in walkDirs(directorio).iteritems()]
    diccionarioFiles_or.sort(key=lambda x: x[1])
    for codigo, files in diccionarioFiles_or:
        created = time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    time.gmtime(os.path.getmtime(files))
                    )
        json += '{"codigo": "%s", "archivo": "%s", "creado": "%s"},' % \
            (codigo, files, created)

    output = '{"lista":[%s]}' % json[:-1]
    return output

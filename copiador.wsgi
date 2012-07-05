#!/usr/bin/python

"""
    Copiador de archivos para entornos
"""

import os


def application(environ, start_response):
    """
        inicio
    """
    status = '200 OK'

    directorio = "/var/www/Portal2"
    listaNivel1 = verDirectorio(directorio)
    outputData = "<html><body>"

    for l1 in listaNivel1:

        outputData += l1 + "<br>"

    outputData += "</body></html>"
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(outputData)))]
    start_response(status, response_headers)

    return [outputData]


def verDirectorio(dir):
    return os.listdir(dir)

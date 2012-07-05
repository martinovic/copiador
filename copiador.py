#!/usr/bin/python

"""
    Copiador de archivos para entornos
"""

import os
import hashlib


def application(environ, start_response):
    """
        inicio
    """
    status = '200 OK'

    directorio = "/var/www/Portal2"
    outputData = """<html><style>td {font-size: 75%;
        font-family: Verdana, sans-serif; }</style>
        <body><table><tr><th>md5</th><th>archivo<th></th></tr>"""
    diccionarioFiles_or = [x for x in walkDirs(directorio).iteritems()]
    diccionarioFiles_or.sort(key=lambda x: x[1])
    for codigo, files in diccionarioFiles_or:
        outputData += ("<tr><td>%30s</td><td>%s</td></tr>" % (codigo, files))

    outputData += "</table></body></html>"
    response_headers = [('Content-type', 'text/html'),
                        ('Content-Length', str(len(outputData)))]
    start_response(status, response_headers)

    return [outputData]


def md5Checksum(filePath):
    """
        doc
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
        doc
    """
    dictFiles = {}
    for root, dirs, files in os.walk(route):
        if root.find(".svn") < 0:
            #if os.path.isfile(root):
            for f in files:
                fileWithRoute = "%s/%s" % (root, f)
                #print(fileWithRoute, md5Checksum(fileWithRoute))
                dictFiles[md5Checksum(fileWithRoute)] = fileWithRoute

    return dictFiles




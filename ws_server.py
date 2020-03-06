# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     ws_server
   Description :  WEBSERVICE服务
   Author :       wdh
   date：          2020-03-05
-------------------------------------------------
   Change Activity:
                   2020-03-05:
-------------------------------------------------
"""

from spyne import Application
from spyne.protocol.soap import Soap11
from app.websrv import WebService
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import logging
from logconf import load_my_logging_cfg

log = logging.getLogger(__name__)
load_my_logging_cfg('webservice')

IP = '0.0.0.0'
PORT = 5000

if __name__ == '__main__':
    soap_app = Application(services=[WebService],
                           tns='ws.greenikon.com',
                           in_protocol=Soap11(validator='lxml'),
                           out_protocol=Soap11(pretty_print=True))
    wsgi_app = WsgiApplication(soap_app)

    log.info("listening to http://%s:%d" % (IP, PORT))
    log.info("wsdl is at: http://%s:%d/?wsdl" % (IP, PORT))
    server = make_server(IP, PORT, wsgi_app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log.info('shutting down the web server')
        server.socket.close()

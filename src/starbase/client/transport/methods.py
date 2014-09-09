__title__ = 'starbase.client.transport.methods'
__author__ = 'Artur Barseghyan'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('GET', 'PUT', 'POST', 'DELETE', 'METHODS', 'DEFAULT_METHOD')

GET = 'GET'
PUT = 'PUT'
POST = 'POST'
DELETE = 'DELETE'
METHODS = (GET, PUT, POST, DELETE)

TOLERATED_RESPONSE_CODES = {
    GET: [],
    PUT: [],
    POST: [],
    DELETE: [500, 503]
}

DEFAULT_METHOD = GET

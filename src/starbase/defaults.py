__title__ = 'starbase.defaults'
__author__ = 'Artur Barseghyan'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('PERFECT_DICT', 'HOST', 'PORT', 'USER', 'PASSWORD', 'DEBUG',)

# If set to True, perfect dict will be enabled.
PERFECT_DICT = True

# Starbase host
HOST = '127.0.0.1'

# Starbase port
PORT = 8000

# Starbase user (in case of HTTP basic auth)
USER = ''

# Starbase password (in case of HTTP basic auth)
PASSWORD = ''

DEBUG = False

__title__ = 'starbase.defaults'
__version__ = '0.2'
__build__ = 0x000002
__author__ = 'Artur Barseghyan'
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

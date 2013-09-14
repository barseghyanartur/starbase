__title__ = 'starbase.exceptions'
__version__ = '0.2'
__build__ = 0x000002
__author__ = 'Artur Barseghyan'
__all__ = ('ImproperlyConfigured', 'InvalidArguments')

class ImproperlyConfigured(Exception):
    """
    Exception raised when developer didn't configure the code properly.
    """

class InvalidArguments(ValueError):
    """
    Exception raised when invalid arguments supplied.
    """

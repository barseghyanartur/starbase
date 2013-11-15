__title__ = 'starbase.exceptions'
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

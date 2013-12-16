__title__ = 'starbase.exceptions'
__author__ = 'Artur Barseghyan'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('ImproperlyConfigured', 'InvalidArguments', 'ParseError', 'DoesNotExist')

class BaseException(Exception):
    """
    Base exception.
    """


class ImproperlyConfigured(BaseException):
    """
    Exception raised when developer didn't configure the code properly.
    """


class InvalidArguments(ValueError, BaseException):
    """
    Exception raised when invalid arguments supplied.
    """


class ParseError(BaseException):
    """
    Raised if the request or response contain malformed data.
    """


class DoesNotExist(BaseException):
    """
    Does not exist.
    """

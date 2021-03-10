"""
    Errors and exceptions for schuaro
"""

class SchuaroException(Exception):
    pass

class UserNotFound(SchuaroException):
    pass

class ClientNotFound(SchuaroException):
    pass

class ClientInvalid(SchuaroException):
    pass

class UserInvalid(SchuaroException):
    pass

class AuthcodeError(SchuaroException):
    pass
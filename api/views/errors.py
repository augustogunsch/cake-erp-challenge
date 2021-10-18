def error(code, type, message, http_code=400):
    return ({
            "code": code,
            "type": type,
            "message": message
    }, http_code)

def ParsingError(message):
    return error(1, "ParsingError", message)

def ConflictingParameters(message):
    return error(2, "ConflictingParameters", message)

def ConflictingResources(message):
    return error(3, "ConflictingResources", message, http_code=409)

def AuthenticationFailure(message):
    return error(4, "AuthenticationFailure", message, http_code=401)

def ForbiddenError(message):
    return error(5, "ForbiddenError", message, http_code=403)

def FetchError(message):
    return error(6, "FetchError", message, http_code=500)

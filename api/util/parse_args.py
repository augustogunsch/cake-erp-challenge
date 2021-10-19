from flask import request

class ParsingException(Exception):
    def __init__(self, message):
        self.message = message

def parse_int(name, minimum):
    try:
        result = int(request.args.get(name, minimum))
    except ValueError:
        raise ParsingException("Couldn't parse {} as integer".format(name))

    if result < minimum:
        raise ParsingException("{} must be greater than {}".format(name, minimum))

    return result

def parse_limit():
    return parse_int("limit", -1)

def parse_offset():
    return parse_int("offset", 0)

def parse_json_obj():
    try:
        json = request.get_json()
    except:
        raise ParsingException("Failed to parse JSON body")

    if type(json) is not dict:
        raise ParsingException("Expected JSON object as body")

    return json

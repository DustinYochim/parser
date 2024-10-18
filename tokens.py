from enum import Enum, auto

operators = ["=", ".le.", ".ge.", ".lt.", ".gt.", "~", ":", ";", "+", "-", "**", "/", "%", "(", ")", ",", "{", "}", "[", "]", "."]

keywords = ["start", "stop", "iterate", "var", "exit", "read", "print", "iff", "then", "set", "func", "program"]

class TokenTypes(Enum):
    KEYWORD = "keyword_token"
    IDENTIFIER = "identifier_token"
    NUMBER = "number_token"
    OPERATOR = "operator_token"
    EOF = "eof_token"



class Token:
    def __init__(self, token_type, token_instance, line_number):
        self.token_type = token_type
        self.token_instance = token_instance
        self.line_number = line_number

    def __str__(self):
        return "{{{}, {}, Line: {}}}".format(self.token_type, self.token_instance, self.line_number)

import re
import sys

from tokens import keywords, TokenTypes, Token, operators


def scanner(word, line_num):
    """
    This scanner takes in a single word and determines whether it is a valid token or an error.
    :param word: A string of text from the input file, no spaces.
    :param line_num: The line number that the word is in.
    :return: a string representation of a token, or an error.
    """
    # EOF Token
    if word == "EOF":
        new_token = Token(TokenTypes.EOF.value, word, line_num)
        return new_token.__str__()
    # Identifier or Keyword Token
    elif re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', word):
        if word in keywords:
            new_token = Token(TokenTypes.KEYWORD.value, word, line_num)
            return new_token.__str__()
        else:
            new_token = Token(TokenTypes.IDENTIFIER.value, word, line_num)
            return new_token.__str__()
    # Number Token
    elif re.match(r'^[0-9]+$', word):
        new_token = Token(TokenTypes.NUMBER.value, word, line_num)
        return new_token.__str__()
    # Operator Token
    elif word in operators:
        new_token = Token(TokenTypes.OPERATOR.value, word, line_num)
        return new_token.__str__()

    ## Comment
    elif re.match(r'^@@.*@$', word):
        return None
    # Error
    else:
        print("LEXICAL ERROR: UNRECOGNIZED TOKEN: " + word + " on line " + str(line_num))
        sys.exit(-1)
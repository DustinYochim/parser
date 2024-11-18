import re
import sys
from tokens import keywords, TokenTypes, Token, operators

def scanner(file_path):
    """
    Generator function that reads an input file and yields tokens.
    :param file_path: The file path for the input file.
    :yield: A string representation of a token, or an error.
    """
    with open(file_path, "r") as f:
        with open('tokens.txt', 'w') as t_f:
            for line_num, line in enumerate(f, start=1):
                for word in line.split():
                    if word == "EOF":
                        new_token = Token(TokenTypes.EOF, word, line_num)
                        t_f.write("{}\n".format(new_token.__str__()))
                        yield new_token
                    elif re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', word):
                        if word in keywords:
                            new_token = Token(TokenTypes.KEYWORD, word, line_num)
                            t_f.write("{}\n".format(new_token.__str__()))
                            yield new_token
                        else:
                            new_token = Token(TokenTypes.IDENTIFIER, word, line_num)
                            t_f.write("{}\n".format(new_token.__str__()))
                            yield new_token
                    elif re.match(r'^[0-9]+$', word):
                        new_token = Token(TokenTypes.NUMBER, word, line_num)
                        t_f.write("{}\n".format(new_token.__str__()))
                        yield new_token
                    elif word in operators:
                        new_token = Token(TokenTypes.OPERATOR, word, line_num)
                        t_f.write("{}\n".format(new_token.__str__()))
                        yield new_token
                    elif re.match(r'^@@.*@$', word):
                        # Skip comments
                        continue
                    else:
                        t_f.write("LEXICAL ERROR: UNRECOGNIZED TOKEN: " + word + " on line " + str(line_num))
                        print("LEXICAL ERROR: UNRECOGNIZED TOKEN: " + word + " on line " + str(line_num))
                        sys.exit(-1)
            # Add EOF token at the end of the file
            new_token = Token(TokenTypes.EOF, "EOF", line_num + 1)
            t_f.write("{}\n".format(new_token.__str__()))
            yield Token(TokenTypes.EOF, "EOF", line_num + 1)

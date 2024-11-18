#!/usr/bin/env python

import os
import sys
import tempfile

from node import Node
from scanner import scanner


class Parser:
    def __init__(self, file_path):
        """
        This constructor function takes in the file path and initializes the scanner and the first token.
        :param file_path: The path to the input file
        """
        self.scan = scanner(file_path)
        self.token = next(self.scan)

    def next_token(self):
        """
        This method sets the current token to the next token returned from the scanner.
        """
        self.token = next(self.scan)

    def parse(self):
        """
        This method starts the parser by calling the program method. All valid programs should end here with
        the EOFTk.
        """
        root = self.program()
        if self.token.token_type == 'eof_token':
            print("Parsed successfully.")
            return root
        else:
            self.error("EOFTk expected.")

    def error(self, message):
        """
        This message takes in a message which contains the expected token and prints an error message and exits.
        :param message: The error message, or the expected token.
        """
        print("Error: {}, received {}".format(message, self.token))
        sys.exit(-1)

    def match(self, expected_instance):
        """
        This method compares the current token instance to the expected instance. If it matches it gets the next token,
        else it will call the error method.
        :param expected_instance: The expected token instance.
        """
        if self.token.token_instance == expected_instance:
            self.next_token()
        else:
            self.error("{} expected".format(expected_instance))

    def program(self):
        """
        <program> -> program <vars> <block>
        """
        node = Node("program")
        if self.token.token_instance != 'program':
            self.error("Program expected")
        self.next_token()
        node.add_child(self.vars())
        node.add_child(self.block())
        return node

    def vars(self):
        """
        <vars> -> empty | var <varList>
        """
        if self.token.token_instance == 'var':
            node = Node("vars")
            self.next_token()
            node.add_child(self.var_list())
            return node
        return Node("vars")

    def var_list(self):
        """
        <varList> -> identifier , integer ; | identifier , integer <varList>
        """
        node = Node("var_list")
        if self.token.token_type == 'identifier_token':
            node.add_token("{} {}".format(self.token.token_type, self.token.token_instance))
            # node.add_token(self.token.token_instance)
            self.next_token()

            if self.token.token_instance == ',':
                self.next_token()
                if self.token.token_type == 'number_token':
                    # node.add_token(self.token.token_instance)
                    node.add_token("{} {}".format(self.token.token_type, self.token.token_instance))
                    self.next_token()
                    if self.token.token_instance == ';':
                        self.match(';')
                    else:
                        node.add_child(self.var_list())
                else:
                    self.error("Integer expected but received {}".format(self.token.token_instance))
            else:
                self.error("Comma expected but received {}".format(self.token.token_instance))

        # self.match(';')
        return node

    def block(self):
        """
        <block> -> start <vars> <stats> stop
        """
        node = Node("block")
        self.match('start')
        node.add_child(self.vars())
        node.add_child(self.stats())
        self.match('stop')
        return node

    def stats(self):
        """
        <stats> -> <stat>  <mStat>
        """
        node = Node("stats")
        node.add_child(self.stat())
        node.add_child(self.m_stat())
        return node

    def m_stat(self):
        """
        <mStat> -> empty |  <stat>  <mStat>
        """
        node = Node("m_stat")
        if self.token.token_instance in ['read', 'print', 'start', 'iff', 'iterate', 'set']:
            node.add_child(self.stat())
            node.add_child(self.m_stat())
        return node

    def stat(self):
        """
        <stat> -> <read>   | <print>   | <block> | <cond>  | <iter>  | <assign>
        """
        node = Node("stat")
        if self.token.token_instance == 'read':
            node.add_child(self.read())
        elif self.token.token_instance == 'print':
            node.add_child(self.Print())
        elif self.token.token_instance == 'start':
            node.add_child(self.block())
        elif self.token.token_instance == 'iff':
            node.add_child(self.cond())
        elif self.token.token_instance == 'iterate':
            node.add_child(self.iter())
        elif self.token.token_instance == 'set':
            node.add_child(self.assign())
        else:
            self.error("Unexpected token in <stat>")
        return node

    def read(self):
        """
        <read> -> read identifier ;
        """
        node = Node("read")
        self.match('read')
        if self.token.token_type == 'identifier_token':
            node.add_token("{} {}".format(self.token.token_type, self.token.token_instance))
            # node.add_token(self.token.token_instance)
            self.next_token()
            self.match(';')
        else:
            self.error("Identifier expected after 'read'")
        return node

    def Print(self):
        """
        <print> -> print <exp> ;
        """
        node = Node("print")
        self.match('print')
        node.add_child(self.exp())
        self.match(';')
        return node

    def cond(self):
        """
        <cond>  -> iff [ <exp> <relational> <exp> ] <stat>
        """
        node = Node("cond")
        self.match('iff')
        self.match('[')
        node.add_child(self.exp())
        node.add_child(self.relational())
        node.add_child(self.exp())
        self.match(']')
        node.add_child(self.stat())
        return node

    def iter(self):
        """
        <iter> -> iterate [ <exp> <relational> <exp> ]  <stat>
        """
        node = Node("iter")
        self.match('iterate')
        self.match('[')
        node.add_child(self.exp())
        node.add_child(self.relational())
        node.add_child(self.exp())
        self.match(']')
        node.add_child(self.stat())
        return node

    def assign(self):
        """
        <assign> -> set identifier <exp> ;
        """
        node = Node("assign")
        self.match('set')
        if self.token.token_type == 'identifier_token':
            node.add_token("{} {}".format(self.token.token_type, self.token.token_instance))
            # node.add_token(self.token.token_instance)
            self.next_token()
            node.add_child(self.exp())
            self.match(';')
        else:
            self.error("Identifier expected after 'set'")
        return node

    def relational(self):
        """
        <relational> -> .le.  | .ge. | .lt. | .gt. | ** | ~
        """
        node = Node("relational")
        if self.token.token_instance in ['.le.', '.ge.', '.lt.', '.gt.', '**', '~']:
            # node.add_token(self.token.token_instance)
            node.add_token("{} {}".format(self.token.token_type, self.token.token_instance))
            self.next_token()
        else:
            self.error("Relational operator expected")
        return node

    def exp(self):
        """
        <exp> -> <M> + <exp> | <M> - <exp> | <M>
        """
        node = Node("exp")
        node.add_child(self.M())
        while self.token.token_instance in ['+', '-']:
            # node.add_token(self.token.token_instance)
            node.add_token("{} {}".format(self.token.token_type, self.token.token_instance))
            self.next_token()
            node.add_child(self.M())
        return node

    def M(self):
        """
        <M> -> <N> % <M> | <N>
        """
        node = Node("m")
        node.add_child(self.N())
        while self.token.token_instance == '%':
            node.add_token("{} {}".format(self.token.token_type, self.token.token_instance))
            # node.add_token(self.token.token_instance)
            self.next_token()
            node.add_child(self.N())
        return node

    def N(self):
        """
        <N> -> <R> / <N> | - <N> |  <R>
        """
        node = Node("n")
        node.add_child(self.R())
        while self.token.token_instance in ['/', '-']:
            node.add_token("{} {}".format(self.token.token_type, self.token.token_instance))
            # node.add_token(self.token.token_instance)
            self.next_token()
            node.add_child(self.R())
        return node

    def R(self):
        """
        <R> -> ( <exp> )  | identifier | integer
        """
        node = Node("r")
        if self.token.token_instance == '(':
            self.next_token()
            node.add_child(self.exp())
            self.match(')')
        elif self.token.token_instance == '-':
            # node.add_token(self.token.token_instance)
            node.add_token("{} {}".format(self.token.token_type, self.token.token_instance))
            self.next_token()
            if self.token.token_type in ['identifier_token', 'number_token']:
                node.add_token("{} {}".format(self.token.token_type, self.token.token_instance))
                # node.add_token(self.token.token_instance)
                self.next_token()
            else:
                self.error("Identifier or number expected after unary '-'")
        elif self.token.token_type == 'identifier_token':
            # node.add_token(self.token.token_instance)
            node.add_token("{} {}".format(self.token.token_type, self.token.token_instance))
            self.next_token()
        elif self.token.token_type == 'number_token':
            # node.add_token(self.token.token_instance)
            node.add_token("{} {}".format(self.token.token_type, self.token.token_instance))
            self.next_token()
        else:
            self.error("Expected '(', identifier, or number")
        return node

def print_tree_in_preorder(node, level=0):
    if node is None:
        return

    tokens_str = ", ".join(node.tokens)  if node.tokens else ''
    # print("{}{} {}".format((' ' * (level * 2)), node.label, tokens_str))
    print("{}{} {}".format((' ' * (level * 2)), node.label, tokens_str))
    # print("{}{}".format((' ' * (level * 2)), node.print_self()))

    for child in node.children:
        print_tree_in_preorder(child, level + 1)

def read_stdin_into_file():
    """
    This method reads stdin into a temporary file to be processed by the scanner/parser.
    :return: the temporary file name.
    """
    with tempfile.NamedTemporaryFile(delete=False, mode='w+', suffix='.txt') as temp_file:
        try:
            for line in sys.stdin:
                temp_file.write(line)
        except IOError as e:
            print("Error writing to temporary file: " + str(e))
            sys.exit(1)
        return temp_file.name

def check_file_exists(file_path=None):
    """
    Checks whether the file at the given path exists.
    :param file_path: the path to the file.
    :return: whether the file at file_path exists or not.
    """
    return os.path.exists(file_path)

def main():
    """
    The main function. Processed command line arguments, and calls the parser with the input file.
    """
    file_path = ""

    if len(sys.argv) == 1:
        file_path = read_stdin_into_file()
    elif len(sys.argv) == 2:
        file_path = sys.argv[1] + ".4280fs24"
        if check_file_exists(file_path):
            if not os.access(file_path, os.R_OK):
                print("Error with input file.")
                sys.exit(-1)
        else:
            print("File does not exist.")
            sys.exit(-1)
    else:
        print("Error: Expected 0 or 1 command line arguments.")
        sys.exit(1)

    parser = Parser(file_path)
    root = parser.parse()
    print_tree_in_preorder(root)

if __name__ == "__main__":
    """
    The entry point of the program.
    """
    main()

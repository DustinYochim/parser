#!/usr/bin/env python

import sys
import os
import tempfile

from test_scanner import test_scanner


def read_stdin_into_file():
    """
    This function will take input from stdin and write it to a temporary file.
    :return: A string containing the name of the temporary file.
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
    This file will take in a string representing a file_path and check if the file exists or not.
    :param file_path: The file path that you want to check exists.
    :return: boolean: Whether the file exists or not.
    """
    return os.path.exists(file_path)

def main():
    """
    The main function is the entry point of the program and will handle program arguments before
    calling the test scanner.
    """

    file_path = ""

    # If no input file is provided, read input from stdin into temporary file
    if len(sys.argv) == 1:
        file_path = read_stdin_into_file()
    # If additional argument is provided, add file extension, verify file exists and is readable
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

    # call the test scanner
    test_scanner(file_path)

    # delete the temporary file
    del file_path


if __name__ == "__main__":
    main()
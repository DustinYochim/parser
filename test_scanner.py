from scanner import scanner


def test_scanner(file_path):
    """
    This function opens the input file,  calls the scanner on each "word", and prints the token.
    :param file_path: The file path for the input file.
    """
    with open(file_path, "r") as f:
        # Read the file line by line, keeping track of line number
        for line_num, line in enumerate(f, start=1):
            # for each line, split the line into words separated by spaces
            for word in line.split():
                # Create a token from each word, if a valid token print it
                token = scanner(word, line_num)
                if token:
                    print(token)
        # Entire file has been processed, add the EOF token
        eof_token = scanner("EOF", line_num + 1)
        if eof_token:
            print(eof_token)

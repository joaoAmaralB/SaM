from lex import lexer
from parser import Parser, ParserError
from utils import read_code_from_file

codigo = read_code_from_file("code_parser.txt")

lexer.input(codigo)
tokens = list(lexer)

try:
    parser = Parser(tokens)
    parser.parse()
    print("Parsing completed successfully.")
except ParserError as e:
    print("Parsing failed with error:")
    print(e)

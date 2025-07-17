from lex import lexer
from parser import Parser

codigo = '''
int a = 5 + 3
int b = 5 * 4
a + b

str palavra = "teste"
'''
lexer.input(codigo)
parser = Parser(lexer)
parser.parse_code()

# lexer.input(codigo)

# print("Tokens:")
# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     print(f"Tipo: {tok.type}: {tok.value}")

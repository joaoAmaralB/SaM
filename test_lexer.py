from lex import lexer
from utils import read_code_from_file

codigo = read_code_from_file("code_lexer.txt")

lexer.input(codigo)

print("Tokens:")
while True:
    tok = lexer.token()
    if not tok:
        break
    print(f"Tipo: {tok.type}: {tok.value}")

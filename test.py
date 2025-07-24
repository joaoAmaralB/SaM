from lex import lexer
from parser import Parser

codigo = '''
int a;

def quadrado(int n) {
    return n * n;
}

def main() {
    int x;
    x = 4;
    int y;
    y = quadrado(x);
    print(y);
}

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

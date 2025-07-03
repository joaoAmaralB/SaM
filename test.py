from lex import lexer
from sam import SaM

codigo = '''
a = 5 + 3
b = 5 * 4
return a
'''

lexer.input(codigo)

tokens = [lex.type for lex in lexer if lex.type != 'NEWLINE']
tokens = [lex.value for lex in lexer if lex.type != 'ID']

print(tokens)

sam = SaM()

sam.run(code=tokens)
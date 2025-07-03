import ply.lex as lex

tokens = (
    'ID', 'INT', 'FLOAT', 'CHAR', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    'EQ', 'NEQ', 'LT', 'LTE', 'GT', 'GTE',
    'ASSIGN',
    'LPAREN', 'RPAREN', 'LSQUARE', 'RSQUARE', 'COLON', 'COMMA',
    'AND', 'OR', 'NOT',
)

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'elif': 'ELIF',
    'while': 'WHILE',
    'def': 'DEF',
    'return': 'RETURN',
    'True': 'TRUE',
    'False': 'FALSE',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'do': 'DO',
}

tokens += tuple(reserved.values())

token_samcode_map = {
    'PLUS': 'ADD',
    'MINUS': 'SUB',
    'TIMES': 'MUL',
    'DIVIDE': 'DIV',
    'MOD': 'MOD',
    'EQ': 'EQ',
    'NEQ': 'NEQ',
    'GT': 'GT',
    'LT': 'LT',
    'GTE': 'GTE',
    'LTE': 'LTE',
    'AND': 'AND',
    'OR': 'OR',
    'NOT': 'NOT',
    'ASSIGN': 'STORE',
    'RETURN': 'RETURN',
    'IF': 'JUMPIF',
    'ELSE': 'JUMP',
}

t_PLUS     = r'\+'
t_MINUS    = r'-'
t_TIMES    = r'\*'
t_DIVIDE   = r'/'
t_MOD      = r'%'
t_EQ       = r'=='
t_NEQ      = r'!='
t_LT       = r'<'
t_LTE      = r'<='
t_GT       = r'>'
t_GTE      = r'>='
t_ASSIGN   = r'='
t_LPAREN   = r'\('
t_RPAREN   = r'\)'
t_COLON    = r':'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_COMMA = r','

t_ignore = ' \t'

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'(\".*?\"|\'.*?\')'
    t.value = t.value[1:-1]
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    if t.type in token_samcode_map:
        t.value = token_samcode_map[t.type]
    return t

def t_AND(t):
    r'and'
    t.value = 'AND'
    return t

def t_OR(t):
    r'or'
    t.value = 'OR'
    return t

def t_NOT(t):
    r'not'
    t.value = 'NOT'
    return t

def t_RETURN(t):
    r'return'
    t.value = 'RETURN'
    return t

def t_error(t):
    print(f"Caractere ilegal: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

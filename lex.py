import ply.lex as lex

tokens = (
    'ID', 'INT', 'FLOAT', 'CHAR', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
    'EQ', 'NEQ', 'LT', 'LTE', 'GT', 'GTE',
    'ASSIGN', 'COMMA', 'COLON',
    'LPAREN', 'RPAREN', 'LSQUARE', 'RSQUARE',
    'LBRACE', 'RBRACE', 'SEMI',
)

reserved = {
    'if': 'IF', 'else': 'ELSE', 'elif': 'ELIF',
    'while': 'WHILE', 'def': 'DEF', 'True': 'TRUE', 'False': 'FALSE',
    'and': 'AND', 'or': 'OR', 'not': 'NOT', 'do': 'DO',
    'int': 'INT_TYPE', 'str': 'STR_TYPE', 'fl': 'FLOAT_TYPE',
    'return': 'RETURN', 'print': 'PRINT'
}

tokens += tuple(reserved.values())

t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_MOD       = r'%'
t_EQ        = r'=='
t_NEQ       = r'!='
t_LT        = r'<'
t_LTE       = r'<='
t_GT        = r'>'
t_GTE       = r'>='
t_ASSIGN    = r'='
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_COLON     = r':'
t_LSQUARE   = r'\['
t_RSQUARE   = r'\]'
t_COMMA     = r','
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_SEMI      = r';'

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

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
    return t

def t_error(t):
    print(f"Illegal character: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

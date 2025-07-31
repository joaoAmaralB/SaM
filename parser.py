class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current = tokens[0] if tokens else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]
        else:
            self.current = None

    def expect(self, typ):
        if not self.current or self.current.type != typ:
            raise ParserError(f"Expected {typ}, got {self.current}")
        self.advance()

    def parse(self):
        self.programa()
        if self.current is not None:
            raise ParserError("Unexpected token at end")

    # Programa → DeclLista
    def programa(self):
        self.decllista()

    # DeclLista → Decl DeclLista | ε
    def decllista(self):
        while self.current and self.current.type in ('INT_TYPE','FLOAT_TYPE','STR_TYPE','DEF'):
            self.decl()

    # Decl → VarDecl | FuncDecl
    def decl(self):
        if self.current.type in ('INT_TYPE','FLOAT_TYPE','STR_TYPE'):
            self.vardecl()
        elif self.current.type == 'DEF':
            self.funcdecl()
        else:
            raise ParserError("Expected declaration")

    # VarDecl → Tipo ID OpcionalArray ;
    def vardecl(self):
        self.tipo()
        self.expect('ID')
        self.opcionalarray()
        self.expect('SEMI')

    # Tipo → INT_TYPE | FLOAT_TYPE | STR_TYPE
    def tipo(self):
        if self.current.type in ('INT_TYPE','FLOAT_TYPE','STR_TYPE'):
            self.advance()
        else:
            raise ParserError("Expected type")

    # OpcionalArray → LSQUARE INT RSQUARE | ε
    def opcionalarray(self):
        if self.current and self.current.type == 'LSQUARE':
            self.advance()
            self.expect('INT')
            self.expect('RSQUARE')

    # FuncDecl → DEF ID LPAREN Parametros RPAREN Bloco
    def funcdecl(self):
        self.expect('DEF')
        self.expect('ID')
        self.expect('LPAREN')
        self.parametros()
        self.expect('RPAREN')
        self.bloco()

    # Parametros → ParamList | ε
    def parametros(self):
        if self.current and self.current.type in ('INT_TYPE','FLOAT_TYPE','STR_TYPE'):
            self.paramlist()

    # ParamList → Param ParamListCont
    def paramlist(self):
        self.param()
        self.paramlistcont()

    # ParamListCont → COMMA Param ParamListCont | ε
    def paramlistcont(self):
        while self.current and self.current.type == 'COMMA':
            self.advance()
            self.param()

    # Param → Tipo ID OpcionalArray
    def param(self):
        self.tipo()
        self.expect('ID')
        self.opcionalarray()

    # Bloco → { CmdLista }
    def bloco(self):
        self.expect('LBRACE')
        self.cmdlista()
        self.expect('RBRACE')

    # CmdLista → Cmd CmdLista | ε
    def cmdlista(self):
        while self.current and self.current.type in (
            'INT_TYPE','FLOAT_TYPE','STR_TYPE','ID','IF','WHILE','DO','RETURN','PRINT'
        ):
            self.cmd()

    # Cmd → VarDecl | CmdID | IfCmd | WhileCmd | DoWhileCmd | ReturnCmd | PrintCmd
    def cmd(self):
        if self.current.type in ('INT_TYPE','FLOAT_TYPE','STR_TYPE'):
            self.vardecl()
        elif self.current.type == 'ID':
            self.cmdid()
        elif self.current.type == 'IF':
            self.ifcmd()
        elif self.current.type == 'WHILE':
            self.whilecmd()
        elif self.current.type == 'DO':
            self.dowhilecmd()
        elif self.current.type == 'RETURN':
            self.returncmd()
        elif self.current.type == 'PRINT':
            self.printcmd()
        else:
            raise ParserError("Expected command")

    # CmdID → ID CmdIDSufixo
    def cmdid(self):
        self.expect('ID')
        # lookahead to distinguish
        if self.current.type == 'LSQUARE' or self.current.type == 'ASSIGN':
            self.cmdidsufixo()
        elif self.current.type == 'LPAREN':
            self.advance()
            self.argumentos()
            self.expect('RPAREN')
            self.expect('SEMI')
        else:
            raise ParserError("Invalid command suffix")

    # CmdIDSufixo → IndiceOpcional ASSIGN Expr ; | LPAREN Argumentos RPAREN ;
    def cmdidsufixo(self):
        # assignment path
        save = self.current.type
        self.indiceopcional()
        if self.current.type == 'ASSIGN':
            self.advance()
            self.expr()
            self.expect('SEMI')
        else:
            raise ParserError("Expected assign")

    # IndiceOpcional → LSQUARE Expr RSQUARE | ε
    def indiceopcional(self):
        if self.current and self.current.type == 'LSQUARE':
            self.advance()
            self.expr()
            self.expect('RSQUARE')

    # IfCmd → IF Expr Bloco ElseParte
    def ifcmd(self):
        self.expect('IF')
        self.expr()
        self.bloco()
        if self.current and self.current.type == 'ELSE':
            self.advance()
            self.bloco()

    # WhileCmd → WHILE Expr Bloco
    def whilecmd(self):
        self.expect('WHILE')
        self.expr()
        self.bloco()

    # DoWhileCmd → DO Bloco WHILE Expr ;
    def dowhilecmd(self):
        self.expect('DO')
        self.bloco()
        self.expect('WHILE')
        self.expr()
        self.expect('SEMI')

    # ReturnCmd → RETURN ReturnSufixo
    def returncmd(self):
        self.expect('RETURN')
        if self.current.type != 'SEMI':
            self.expr()
        self.expect('SEMI')

    # PrintCmd → PRINT LPAREN Expr RPAREN ;
    def printcmd(self):
        self.expect('PRINT')
        self.expect('LPAREN')
        self.expr()
        self.expect('RPAREN')
        self.expect('SEMI')

    # Argumentos → ArgList | ε
    def argumentos(self):
        if self.current and self.current.type not in ('RPAREN',):
            self.arglist()

    # ArgList → Expr ArgListCont
    def arglist(self):
        self.expr()
        while self.current and self.current.type == 'COMMA':
            self.advance()
            self.expr()

    # Expr → LogicalOr
    def expr(self):
        self.logicalor()

    def logicalor(self):
        self.logicaland()
        while self.current and self.current.type == 'OR':
            self.advance()
            self.logicaland()

    def logicaland(self):
        self.unarynot()
        while self.current and self.current.type == 'AND':
            self.advance()
            self.unarynot()

    def unarynot(self):
        if self.current and self.current.type == 'NOT':
            self.advance()
            self.comparison()
        else:
            self.comparison()

    def comparison(self):
        self.additive()
        if self.current and self.current.type in ('EQ','NEQ','LT','LTE','GT','GTE'):
            self.advance()
            self.additive()

    def additive(self):
        self.multiplicative()
        while self.current and self.current.type in ('PLUS','MINUS'):
            self.advance()
            self.multiplicative()

    def multiplicative(self):
        self.primary()
        while self.current and self.current.type in ('TIMES','DIVIDE','MOD'):
            self.advance()
            self.primary()

    def primary(self):
        if self.current.type in ('INT','FLOAT','STRING'):
            self.advance()
        elif self.current.type == 'ID':
            self.advance()
            self.postfix()
        elif self.current.type == 'LPAREN':
            self.advance()
            self.expr()
            self.expect('RPAREN')
        else:
            raise ParserError("Expected primary")

    def postfix(self):
        if self.current.type == 'LSQUARE':
            self.advance()
            self.expr()
            self.expect('RSQUARE')
        elif self.current.type == 'LPAREN':
            self.advance()
            self.argumentos()
            self.expect('RPAREN')
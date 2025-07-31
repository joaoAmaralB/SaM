EPSILON = 'ε'
ENDMARKER = '$'

grammar = {
    'Programa': [['DeclLista']],
    'DeclLista': [['Decl', 'DeclLista'], ['ε']],
    'Decl': [['VarDecl'], ['FuncDecl']],
    'VarDecl': [['Tipo', 'ID', 'OpcionalArray', ';']],
    'Tipo': [['INT_TYPE'], ['FLOAT_TYPE'], ['STR_TYPE']],
    'OpcionalArray': [['LSQUARE', 'INT', 'RSQUARE'], ['ε']],
    'FuncDecl': [['DEF', 'ID', 'LPAREN', 'Parametros', 'RPAREN', 'Bloco']],
    'Parametros': [['ParamList'], ['ε']],
    'ParamList': [['Param', 'ParamListCont']],
    'ParamListCont': [['COMMA', 'Param', 'ParamListCont'], ['ε']],
    'Param': [['Tipo', 'ID', 'OpcionalArray']],
    'Bloco': [['{', 'CmdLista', '}']],
    'CmdLista': [['Cmd', 'CmdLista'], ['ε']],
    'Cmd': [['VarDecl'], ['CmdID'], ['IfCmd'], ['WhileCmd'], ['DoWhileCmd'], ['ReturnCmd'], ['PrintCmd']],
    'CmdID': [['ID', 'CmdIDSufixo']],
    'CmdIDSufixo': [['IndiceOpcional', 'ASSIGN', 'Expr', ';'], ['LPAREN', 'Argumentos', 'RPAREN', ';']],
    'IndiceOpcional': [['LSQUARE', 'Expr', 'RSQUARE'], ['ε']],
    'IfCmd': [['IF', 'Expr', 'Bloco', 'ElseParte']],
    'ElseParte': [['ELSE', 'Bloco'], ['ε']],
    'WhileCmd': [['WHILE', 'Expr', 'Bloco']],
    'DoWhileCmd': [['DO', 'Bloco', 'WHILE', 'Expr', ';']],
    'ReturnCmd': [['RETURN', 'ReturnSufixo']],
    'ReturnSufixo': [['Expr', ';'], [';']],
    'PrintCmd': [['PRINT', 'LPAREN', 'Expr', 'RPAREN', ';']],
    'Argumentos': [['ArgList'], ['ε']],
    'ArgList': [['Expr', 'ArgListCont']],
    'ArgListCont': [['COMMA', 'Expr', 'ArgListCont'], ['ε']],
    'Expr': [['LogicalOr']],
    'LogicalOr': [['LogicalAnd', 'LogicalOrTail']],
    'LogicalOrTail': [['OR', 'LogicalAnd', 'LogicalOrTail'], ['ε']],
    'LogicalAnd': [['UnaryNot', 'LogicalAndTail']],
    'LogicalAndTail': [['AND', 'UnaryNot', 'LogicalAndTail'], ['ε']],
    'UnaryNot': [['NOT', 'Comparison'], ['Comparison']],
    'Comparison': [['Additive', 'ComparisonTail']],
    'ComparisonTail': [['RelOp', 'Additive'], ['ε']],
    'RelOp': [['EQ'], ['NEQ'], ['LT'], ['LTE'], ['GT'], ['GTE']],
    'Additive': [['Multiplicative', 'AdditiveTail']],
    'AdditiveTail': [['AddOp', 'Multiplicative', 'AdditiveTail'], ['ε']],
    'AddOp': [['PLUS'], ['MINUS']],
    'Multiplicative': [['Primary', 'MultiplicativeTail']],
    'MultiplicativeTail': [['MulOp', 'Primary', 'MultiplicativeTail'], ['ε']],
    'MulOp': [['TIMES'], ['DIVIDE'], ['MOD']],
    'Primary': [['INT'], ['FLOAT'], ['STRING'],
                ['ID', 'Postfix'],
                ['LPAREN', 'Expr', 'RPAREN']],
    'Postfix': [['Indice'], ['FunctionCall'], ['ε']],
    'Indice': [['LSQUARE', 'Expr', 'RSQUARE']],
    'FunctionCall': [['LPAREN', 'Argumentos', 'RPAREN']],
}


terminals = set()
non_terminals = set(grammar.keys())

for prods in grammar.values():
    for prod in prods:
        for symbol in prod:
            if symbol not in grammar and symbol != EPSILON:
                terminals.add(symbol)

def compute_first_sets():
    first = {nt: set() for nt in grammar}
    changed = True
    while changed:
        changed = False
        for nt in grammar:
            for production in grammar[nt]:
                before = len(first[nt])
                if production == [EPSILON]:
                    first[nt].add(EPSILON)
                else:
                    for symbol in production:
                        if symbol in terminals:
                            first[nt].add(symbol)
                            break
                        else:
                            first[nt] |= (first[symbol] - {EPSILON})
                            if EPSILON not in first[symbol]:
                                break
                    else:
                        first[nt].add(EPSILON)
                if len(first[nt]) > before:
                    changed = True
    return first


def compute_follow_sets(first_sets):
    follow = {nt: set() for nt in grammar}
    follow['Programa'].add(ENDMARKER)
    changed = True
    while changed:
        changed = False
        for nt in grammar:
            for production in grammar[nt]:
                trailer = follow[nt].copy()
                for symbol in reversed(production):
                    if symbol in grammar:
                        before = len(follow[symbol])
                        follow[symbol] |= trailer
                        if EPSILON in first_sets[symbol]:
                            trailer |= (first_sets[symbol] - {EPSILON})
                        else:
                            trailer = first_sets[symbol]
                        if len(follow[symbol]) > before:
                            changed = True
                    else:
                        trailer = {symbol}
    return follow


def compute_first_of_string(symbols, first_sets):
    result = set()
    for symbol in symbols:
        if symbol == EPSILON:
            result.add(EPSILON)
            return result
        elif symbol in terminals:
            result.add(symbol)
            return result
        elif symbol in first_sets:
            result |= (first_sets[symbol] - {EPSILON})
            if EPSILON not in first_sets[symbol]:
                return result
        else:
            return result
    result.add(EPSILON)
    return result

def is_ll1(grammar, first_sets, follow_sets):
    for nt in grammar:
        predict_set = set()
        for production in grammar[nt]:
            first_alpha = compute_first_of_string(production, first_sets)
            if EPSILON in first_alpha:
                predict = (first_alpha - {EPSILON}) | follow_sets[nt]
            else:
                predict = first_alpha
            if predict & predict_set:
                print(f"Conflito em {nt}: {predict & predict_set}")
                return False
            predict_set |= predict
    return True


if __name__ == "__main__":
    first_sets = compute_first_sets()
    follow_sets = compute_follow_sets(first_sets)
    
    print("FIRST sets:")
    for nt in first_sets:
        print(f"{nt}: {first_sets[nt]}")

    print("\nFOLLOW sets:")
    for nt in follow_sets:
        print(f"{nt}: {follow_sets[nt]}")

    print("\nVerificando se a gramática é LL(1)...")
    if is_ll1(grammar, first_sets, follow_sets):
        print("✅ A gramática é LL(1)")
    else:
        print("❌ A gramática NÃO é LL(1)")

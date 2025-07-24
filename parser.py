
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.stack = self.stack_lexer()
        self.pointer = 0
        print(self.stack)

    def stack_lexer(self):
        stack = []
        while True:
            token = self.lexer.token()
            if not token:
                break
            stack.append((token.type, token.value))

        return stack

    def step(self):
        if self.pointer < len(self.stack):
            self.pointer += 1

    def redirect(self, position):
        if position < len(self.stack):
            self.pointer = position

    def get_token(self):
        if self.pointer < len(self.stack):
            return self.stack[self.pointer]

    def check_types(self):
        pass

    def parse_code(self):
        pass
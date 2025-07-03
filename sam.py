class SaM:
    def __init__(self):
        self.memory = []
        self.stack = []
        self.pc = 0
        self.running = True
        self.labels = {}
        self.command_actions = {
            "PUSHIMM": self.pushimm,
            "PUSHMMP": self.pushmmp,
            "PUSHLOC": self.pushloc,
            "LOAD": self.load,
            "STORE": self.store,
            "DUP": self.dup,
            "POP": self.pop_op,
            "SWAP": self.swap,
            "ADD": self.add,
            "SUB": self.sub,
            "MUL": self.mul,
            "DIV": self.div,
            "AND": self.and_op,
            "OR": self.or_op,
            "NOT": self.not_op,
            "EQ": self.eq,
            "NE": self.ne,
            "LT": self.lt,
            "LE": self.le,
            "GT": self.gt,
            "GE": self.ge,
            "JUMP": self.jump,
            "JUMPF": self.jumpf,
            "JUMPT": self.jumpt,
            "CALL": self.call,
            "RET": self.ret,
            "DUMP": self.dump,
            "PRINT": self.print_top,
            "READ": self.read,
            "STOP": self.stop
        }

    def pushimm(self):
        value = int(self.tokens[self.pc]); self.pc += 1
        self.stack.append(value)

    def pushmmp(self):
        offset = int(self.tokens[self.pc]); self.pc += 1
        # assume MP = 0 base
        self.stack.append(self.memory[offset])

    def pushloc(self):
        offset = int(self.tokens[self.pc]); self.pc += 1
        self.stack.append(self.memory[offset])

    def load(self):
        addr = int(self.tokens[self.pc]); self.pc += 1
        self.stack.append(self.memory[addr])

    def store(self):
        addr = int(self.tokens[self.pc]); self.pc += 1
        value = self.stack.pop()
        if addr >= len(self.memory):
            self.memory.extend([0] * (addr - len(self.memory) + 1))
        self.memory[addr] = value

    def dup(self):
        self.stack.append(self.stack[-1])

    def pop_op(self):
        self.stack.pop()

    def swap(self):
        a = self.stack.pop(); b = self.stack.pop()
        self.stack.extend([a, b])

    def binary_op(self, fn):
        b = self.stack.pop(); a = self.stack.pop()
        self.stack.append(fn(a, b))

    def add(self):    self.binary_op(lambda a,b: a+b)
    def sub(self):    self.binary_op(lambda a,b: a-b)
    def mul(self):    self.binary_op(lambda a,b: a*b)
    def div(self):    self.binary_op(lambda a,b: a//b)
    def and_op(self): self.binary_op(lambda a,b: 1 if a and b else 0)
    def or_op(self):  self.binary_op(lambda a,b: 1 if a or b else 0)
    def eq(self):     self.binary_op(lambda a,b: 1 if a==b else 0)
    def ne(self):     self.binary_op(lambda a,b: 1 if a!=b else 0)
    def lt(self):     self.binary_op(lambda a,b: 1 if a<b else 0)
    def le(self):     self.binary_op(lambda a,b: 1 if a<=b else 0)
    def gt(self):     self.binary_op(lambda a,b: 1 if a>b else 0)
    def ge(self):     self.binary_op(lambda a,b: 1 if a>=b else 0)

    def jump(self):
        label = self.tokens[self.pc]; self.pc += 1
        self.pc = self.labels[label]

    def jumpf(self):
        label = self.tokens[self.pc]; self.pc += 1
        cond = self.stack.pop()
        if cond == 0:
            self.pc = self.labels[label]

    def jumpt(self):
        label = self.tokens[self.pc]; self.pc += 1
        cond = self.stack.pop()
        if cond != 0:
            self.pc = self.labels[label]

    def call(self):
        label = self.tokens[self.pc]; self.pc += 1
        # empilha retorno
        self.stack.append(self.pc)
        self.pc = self.labels[label]

    def ret(self):
        self.pc = self.stack.pop()

    def dump(self):
        print("STACK:", self.stack)
        print("MEMORY:", self.memory)

    def print_top(self):
        print(self.stack[-1])

    def read(self):
        val = int(input())
        self.stack.append(val)

    def stop(self):
        self.running = False

    def not_op(self):
        a = self.stack.pop()
        self.stack.append(0 if a else 1)

    def run(self, code: str):
        self.memory = []
        self.stack = []
        self.pc = 0
        self.running = True
        self.labels = {}
        self.tokens = code

        while self.running and self.pc < len(self.tokens):
            token = self.tokens[self.pc]; self.pc += 1
            action = self.command_actions.get(token)
            if action:
                action()
            else:
                try:
                    self.stack.append(int(token))
                except ValueError:
                    raise Exception(f"Token desconhecido: {token}")

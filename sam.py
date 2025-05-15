from collections import deque

class SaM:
    def __init__(self):
        self.memory = []
        self.stack = deque()
        self.pc = 0
        self.command_actions = {
            "PUSHIMM": self.declare_int,
            "ADD": self.add,
            "MUL": self.mul,
            "SUB": self.sub,
            "DIV": self.div,
        }

    def add_code_2_stack(self, code):
        self.stack = deque(code.split())
        self.stack.reverse()

    def declare_int(self):
        num = self.stack.pop()
        self.memory.append(int(num))

    def add(self):
        a = int(self.memory.pop())
        b = int(self.memory.pop())
        result = a + b
        self.memory.append(result)

    def sub(self):
        a = int(self.memory.pop())
        b = int(self.memory.pop())
        result = b - a
        self.memory.append(result)

    def mul(self):
        a = int(self.memory.pop())
        b = int(self.memory.pop())
        result = a*b
        self.memory.append(result)

    def div(self):
        a = int(self.memory.pop())
        b = int(self.memory.pop())
        result = int(b/a)
        self.memory.append(result)

    def run(self, code):
        self.add_code_2_stack(code)

        while len(self.stack) != 0:
            command = self.stack.pop()
            func = self.command_actions.get(command)

            if func:
                func()
                print(f"Memory: {self.memory}")

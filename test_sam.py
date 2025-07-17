from sam import SaM

vm = SaM()

with open("teste.txt", "r") as f:
    raw_code = f.read()

code = []
for line in raw_code.splitlines():
    tokens = line.strip().split()
    code.extend(tokens)

vm.run(code)

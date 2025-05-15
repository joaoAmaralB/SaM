
from sam import SaM

vm = SaM()
code = open("teste.txt", "r").read()

vm.run(code)
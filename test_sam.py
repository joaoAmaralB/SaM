
from sam import SaM

vm = SaM()
code = open("teste.txt", "r").read()
breakpoint()
vm.run(code)

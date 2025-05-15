import re

LANG_2_SAM_REGEX = {
    "=": "PUSHMMP",
    "int": "TESTE",
    "x": "xis",
    "y": "ipsilon",
    r"\d+": r"\d+"
}

def convert_stack_2_sam(stack):
    return [LANG_2_SAM_REGEX[inst] for inst in stack]
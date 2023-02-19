TACs = []

class TAC(object):

    def __init__(self, op: str, arg1: int|float|bool = None, arg2: int|float|bool = None, dest = None) -> None:
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.dest = dest

        self.logical_mapping = {
            "and": "&&",
            "or": "||",
        }
        self.comparison_mapping = {
            ">": ">",
            "<": "<",
            ">=": ">=",
            "<=": "<=",
            "==": "==",
            "<>": "!=",
        }

    def to_c_code(self):

        if self.op == "print":
            return f"printf(\"%d\", {self.arg1});"
        elif self.op == "if":
            return f"if ({self.arg1})" + " {\n" + self.arg2 + "}\n"
        elif self.op == "while":
            return f"while ({self.arg1})" + " {\n" + self.arg2 + "}\n"
        elif self.op == "assign":
            return f"{self.dest} = {self.arg1};"
        elif self.op in ("+", "-", "*", "/", "%"):
            return f"{self.dest} = {self.arg1} {self.op} {self.arg2};"
        elif self.op in ("and", "or"):
            return f"{self.dest} = {self.arg1} {self.logical_mapping[self.op]} {self.arg2};"
        elif self.op  == "not":
            return f"{self.dest} = !{self.arg1};"
        elif self.op in ("<", ">", "<=", ">=", "==", "<>"):
            return f"{self.dest} = {self.arg1} {self.comparison_mapping[self.op]} {self.arg2}"

        return f"{self.dest} :: {self.arg1} {self.op} {self.arg2};"
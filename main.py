import re

instruction_set = ["LDA", "STA", "ADD", "SUB",
                   "DAT", "BRP", "BRZ", "BRA", "HLT", "OUT", "INP"]


class LittleManComputer():
    def __init__(self, path: str):
        self.path = path
        self.accumulator = 0
        self.data = []
        self.lines = []
        self.index = 0
        self.current_line = 0
        self.DEBUG = False
        self.execute_LMC()


# Parses the .s file and pushes the data into 2 lists. one for lines, the other for variables
    def parse_LMC(self):
        with open(self.path, "r") as file:
            lines = file.read().split("\n")
            for element in lines:
                try:
                    line = re.sub(r"[\t]", " ", element).split()
                    if not line:
                        continue
                    self.lines.append(line)
                    if line[1].upper() == "DAT":
                        self.data.append({"variable_name": line[0], "value": line[2]})
                except:
                    continue

    def execute_LMC(self):
        self.parse_LMC()
        total_lines = len(self.lines)

        while self.current_line < total_lines:
            line = self.lines[self.current_line]

            if len(line) > 2:
                self.index = 1
            else:
                self.index = 0

            try:
                if line[1] == "OUT":
                    self.index = 1
            except:
                pass

            if line[self.index].upper() == "LDA":
                self.load_variable(line[self.index + 1])

            elif line[self.index].upper() == "ADD":
                self.add(line[self.index + 1])

            elif line[self.index].upper() == "SUB":
                self.sub(line[self.index + 1])

            elif line[self.index].upper() == "STA":
                self.store_data(line[self.index + 1])

            elif line[self.index].upper() == "INP":
                self.get_input()

            elif line[self.index].upper() == "HLT":
                break

            elif line[self.index].upper() == "OUT":
                self.output()

            elif line[self.index].upper() == "BRP":
                self.branch_if_positive(line[self.index + 1])

            elif line[self.index].upper() == "BRA":
                self.branch(line[self.index + 1])

            elif line[self.index].upper() == "BRZ":
                self.branch_if_zero(line[self.index + 1])

            # no DAT since that gets parsed in the parse_LMC method

            if self.DEBUG:
                print(f"[DEBUG]\n    Accumulator: {self.accumulator}\n    Current_line: {self.current_line}\n    Current Instruction: {line[self.index].upper()}\n[DEBUG]")

            self.current_line += 1

# Below are the functions which emulate each opcode

    def load_variable(self, name):
        for dat in self.data:
            if dat["variable_name"].lower() == name.lower():
                self.accumulator = int(dat["value"])

    def add(self, name: str) -> None:
        for dat in self.data:
            if dat["variable_name"].lower() == name.lower():
                self.accumulator += int(dat["value"])

    def sub(self, name: str) -> None:
        for dat in self.data:
            if dat["variable_name"].lower() == name.lower():
                self.accumulator -= int(dat["value"])

    def store_data(self, name):
        for dat in self.data:
            if dat["variable_name"].lower() == name.lower():
                dat["value"] = self.accumulator

    def get_input(self):
        self.accumulator = int(input(">> "))

    def output(self):
        print(self.accumulator)

    def branch(self, identifier: str):
        for idx, elem in enumerate(self.lines):
            if elem[0].upper() == identifier.upper():
                self.current_line = idx - 1

    def branch_if_positive(self, identifier: str):
        if self.accumulator >= 0:
            self.branch(identifier)

    def branch_if_zero(self, identifier: str):
        if self.accumulator == 0:
            self.branch(identifier)


def main():
    LittleManComputer("./sample.s")


main()

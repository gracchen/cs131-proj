
class StateDef():
    def __init__(self, program):
        self.program = program

    def run(self):
        if (self.program[0] == "print"):
            for i in range(1, len(self.program)):
                print(self.program[i])
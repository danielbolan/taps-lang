# A pretty normal brainfuck interpreter, with the addition of one feature.
# Any character input that isn't a normal brainfuck instruction will have
# its last signficiant byte saved to the current cell. This means the
# shortest Hello World program could be something like:
#   H.E.L..O. .W.O.R.L.D.
class Interpreter:
    _TAPE_LENGTH = 30_000

    def __init__(self):
        self.tape = [0] * self._TAPE_LENGTH
        self.pointer = 0
        self.ins_pointer = 0
        self.stack = list()
        self.program = None

        self.fns = {
            ".": self.char_output,
            "+": self.increment,
            "-": self.decrement,
            ">": self.shift_right,
            "<": self.shift_left,
            "[": self.conditional_skip,
            "]": self.conditional_loop,
            "?": self.memory_dump,
        }

    def val(self, new_val=None):
        if new_val is None:
            return self.tape[self.pointer]
        else:
            self.tape[self.pointer] = new_val
            return new_val

    def char_output(self):
        print(chr(self.val()), end="")

    def char_input(self, c):
        self.val(ord(c) % 256)

    def increment(self):
        i = (self.val() + 1) % 256
        self.val(i)

    def decrement(self):
        i = (self.val() - 1) % 256
        self.val(i)

    def shift_right(self):
        self.pointer = (self.pointer + 1) % self._TAPE_LENGTH

    def shift_left(self):
        self.pointer = (self.pointer - 1) % self._TAPE_LENGTH

    def conditional_skip(self):
        self.stack.append(self.ins_pointer)
        start_ins = self.ins_pointer
        if self.val() == 0:
            while self.ins_pointer < len(self.program):
                if self.program[self.ins_pointer] == "]":
                    break
                self.ins_pointer += 1
            else:
                raise ValueError(f"Unmatched bracket at char {start_ins}, maybe?")

    def conditional_loop(self):
        next_ins = self.stack.pop()
        if self.val() != 0:
            self.ins_pointer = next_ins - 1

    def memory_dump(self):
        for i in range(self._TAPE_LENGTH):
            line = f"{i:>5} {self.tape[i]:<3}"

            if ord(" ") <= self.tape[i] <= ord("~"):
                line += f"({chr(self.tape[i])})"
            else:
                line += " " * 3

            if i == self.pointer:
                line += " <--"

            print(line)

    def tick(self):
        c = self.program[self.ins_pointer]
        if c in self.fns:
            self.fns[c]()
        elif c not in ["\n", " "]:
            self.char_input(c)
        self.ins_pointer += 1

    def run(self, program):
        self.__init__()
        self.program = program
        while self.ins_pointer < len(self.program):
            self.tick()


if __name__ == "__main__":
    i = Interpreter()
    i._TAPE_LENGTH = 6
    hello_world = (
        "H.---.[->+>+<<]>>-----[--<<+>>]"
        "L..[->+>+<<]>+++.<W<<.--[---<+>]"
        ">>.>.+++.>.<<<-.<<."
    )
    i.run(hello_world)
    print("-" * 20)
    i.memory_dump()

class Tape:
    def __init__(self, input_list, blank='_'):
        self.tape = {i: ch for i, ch in enumerate(input_list)}
        self.head = 0
        self.blank = blank

    def read(self):
        return self.tape.get(self.head, self.blank)

    def write(self, symbol):
        self.tape[self.head] = symbol

    def move(self, direction):
        if direction == 'R':
            self.head += 1
        elif direction == 'L':
            self.head -= 1
        else:
            raise Exception(f"Direction must be 'R' or 'L', got '{direction}'")

    def content(self):
        if not self.tape:
            return ''
        left = min(self.tape.keys())
        right = max(self.tape.keys())
        return ''.join(self.tape.get(i, self.blank) for i in range(left, right + 1))

    def visualize(self):
        tape_str = self.content()
        head_pos = self.head - min(self.tape.keys())
        print(tape_str)
        print(' ' * head_pos + '^')


class TuringCore:
    def __init__(self, path):
        self.states = {}
        self.alphabet = set()
        self.transitions = {}
        self.start = None
        self.ends = set()
        self._parse(path)

    def _parse(self, filepath):
        section = None
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                if line.startswith('[') and line.endswith(']'):
                    section = line[1:-1].lower()
                    continue

                if section == 'states':
                    parts = line.split()
                    state = parts[0]
                    tag = parts[1] if len(parts) > 1 else None
                    self.states[state] = tag
                    if tag == 'S':
                        self.start = state
                    if tag == 'F':
                        self.ends.add(state)

                elif section == 'sigma':
                    self.alphabet.add(line)

                elif section == 'rules':
                    cs, rs, ns, ws, dir = line.split()
                    self.transitions[(cs, rs)] = (ns, ws, dir)

    def run(self, input_data, max_cycles=10000):
        tape = Tape(input_data)
        current_state = self.start
        cycles = 0

        print("Initial tape:")
        tape.visualize()

        while current_state not in self.ends:
            symbol = tape.read()
            key = (current_state, symbol)

            if key not in self.transitions:
                print("Halted: no rule found.")
                return

            next_state, write_sym, direction = self.transitions[key]
            tape.write(write_sym)
            tape.move(direction)
            current_state = next_state

            cycles += 1
            if cycles > max_cycles:
                print("Halted: step limit exceeded.")
                return

        print("✅ Completed: reached final state.")
        tape.visualize()


# Usage Example
if __name__ == '__main__':
    # You can change the tape and config file as needed
    engine = TuringCore('turing_input.txt')
    engine.run(['1', '0', '1', '1', '_'])


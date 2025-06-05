# Turing Machine Simulator

def parse_turing_file(path):
    from collections import defaultdict

    def preprocess(lines):
        return [line.strip() for line in lines if line.strip() and not line.startswith('#')]

    def gather_blocks(lines):
        content = defaultdict(list)
        label = None

        for line in lines:
            if line.startswith('[') and line.endswith(']'):
                label = line[1:-1]
            elif label:
                content[label].append(line)
        return content

    def parse_blocks(blocks):
        result = {}
        for section, lines in blocks.items():
            if section == 'sigma':
                result[section] = list(dict.fromkeys(lines))  # unique and ordered
            else:
                result[section] = [ln.split() for ln in lines]
        return result

    with open(path) as f:
        raw_lines = f.readlines()

    cleaned = preprocess(raw_lines)
    blocks = gather_blocks(cleaned)
    return parse_blocks(blocks)


def validate_machine(machine):
    required = ['states', 'sigma', 'rules']
    return all(key in machine for key in required)

def rule_is_valid(rule, machine):
    if len(rule) != 5:
        return False
    state_names = {state[0] for state in machine['states']}
    return (rule[0] in state_names and
            rule[2] in state_names and
            rule[1] in machine['sigma'] and
            rule[3] in machine['sigma'] and
            rule[4] in {'R', 'L'})

def check_every_transition(machine):
    return all(rule_is_valid(rule, machine) for rule in machine['rules'])

def symbols_match_alphabet(tape_input, machine):
    return all(symbol in machine['sigma'] for symbol in tape_input)

def simulate_turing_machine():
    machine = parse_turing_file("input_turing.txt")

    if not validate_machine(machine) or not check_every_transition(machine):
        print("Invalid Turing machine definition.")
        return

    tape = input("Enter tape input (space-separated): ").split()
    tape += ['_'] * 100
    if not symbols_match_alphabet(tape, machine):
        print("Invalid tape symbols.")
        return

    # initialize tape and head
    tape += ['_'] * 100
    head = 0

    start_state = None
    final_state = None
    for state, tag in machine['states']:
        if tag == 'S':
            start_state = state
        elif tag == 'F':
            final_state = state

    if not start_state or not final_state:
        print("Start or final state not properly defined.")
        return

    if machine['rules'][0][0] != start_state:
        print("First rule must start with the initial state.")
        return

    current_state = start_state

    while current_state != final_state:
        if head < 0 or head >= len(tape):
            print("Head moved out of tape bounds.")
            break

        transition_found = False
        for rule in machine['rules']:
            state, read_sym, next_state, write_sym, direction = rule
            if state == current_state and tape[head] == read_sym:
                tape[head] = write_sym
                current_state = next_state
                head += 1 if direction == 'R' else -1
                transition_found = True
                break

        if not transition_found:
            print("No applicable transition. Halting.")
            break

    # Show the tape after execution (excluding trailing blanks)
    print("Final tape:")
    print(' '.join(sym for sym in tape if sym != '_'))

simulate_turing_machine()

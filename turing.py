# Turing Machine Simulator

def parse_turing_file(filename):
    machine = {}
    section = None
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('[') and line.endswith(']'):
                section = line[1:-1]
                machine[section] = []
            else:
                tokens = line.split()
                if section == 'sigma':
                    symbol = tokens[0]
                    if symbol not in machine[section]:
                        machine[section].append(symbol)
                elif section:
                    machine[section].append(tokens)
    return machine

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

def all_rules_valid(machine):
    return all(rule_is_valid(rule, machine) for rule in machine['rules'])

def input_is_valid(tape_input, machine):
    return all(symbol in machine['sigma'] for symbol in tape_input)

def simulate_turing_machine():
    machine = parse_turing_file("turing_input2.txt")

    if not validate_machine(machine) or not all_rules_valid(machine):
        print("Invalid Turing machine definition.")
        return

    tape = input("Enter tape input (space-separated): ").split()
    if not input_is_valid(tape, machine):
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

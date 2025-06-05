# This script simulates a Deterministic Finite Automaton (DFA) based on an input file

def read_automaton(filepath):
    from collections import defaultdict

    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    sections = defaultdict(list)
    handlers = {
        'states': lambda ln: ln.split(),
        'sigma': lambda ln: ln.strip(),
        'rules': lambda ln: ln.split()
    }

    key = None
    for line in lines:
        if line.startswith('[') and line.endswith(']'):
            key = line[1:-1]
            continue
        if key in handlers:
            parsed = handlers[key](line)
            if parsed not in sections[key]:
                sections[key].append(parsed)

    return dict(sections)

def validate_automaton(automaton):
    required_parts = ['states', 'sigma', 'rules']
    return all(part in automaton for part in required_parts)

def validate_rule(rule, automaton):
    states = {state[0] for state in automaton['states']}
    return len(rule) == 3 and rule[0] in states and rule[2] in states and rule[1] in automaton['sigma']

def validate_all_rules(automaton):
    return all(validate_rule(rule, automaton) for rule in automaton['rules'])

def check_initial_rule(rule, start_state):
    return rule[0] == start_state

def input_valid(input_list, sigma):
    return all(symbol in sigma for symbol in input_list)

def simulate_dfa():
    automaton = read_automaton("input_dfa.txt")

    if not validate_automaton(automaton) or not validate_all_rules(automaton):
        print("Invalid DFA structure. Please check your file.")
        return

    input_symbols = input("Enter input symbols (space-separated): ").split()
    if not input_valid(input_symbols, automaton['sigma']):
        print("Invalid input symbols.")
        return

    start = None
    finals = []
    for state, label in automaton['states']:
        if label == 'S':
            start = state
        elif label == 'F':
            finals.append(state)

    if not check_initial_rule(automaton['rules'][0], start):
        print("First rule doesn't start from the initial state.")
        return

    current = start
    print(current, end='')

    for i, symbol in enumerate(input_symbols):
        for rule in automaton['rules']:
            if rule[0] == current and rule[1] == symbol:
                current = rule[2]
                print(f" -> {current}", end='' if i < len(input_symbols) - 1 else '\n')
                break
    if current in finals:
        print("DFA input accepted!")
    else:
        print("The automata is not in a final state.")

simulate_dfa()
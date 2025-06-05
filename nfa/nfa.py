# NFA Simulator - Non-deterministic Finite Automaton

def parse_nfa_file(path):
    from collections import defaultdict

    def sanitize(lines):
        return [line.strip() for line in lines if line.strip() and not line.startswith('#')]

    def collect_sections(lines):
        index_map = {}
        for idx, line in enumerate(lines):
            if line.startswith('[') and line.endswith(']'):
                section_name = line[1:-1]
                index_map[section_name] = idx
        return index_map

    with open(path) as file:
        raw_lines = sanitize(file.readlines())

    section_indices = collect_sections(raw_lines)
    result = {}

    sorted_sections = list(section_indices.items())
    for i, (name, start_idx) in enumerate(sorted_sections):
        end_idx = sorted_sections[i + 1][1] if i + 1 < len(sorted_sections) else len(raw_lines)
        content = raw_lines[start_idx + 1:end_idx]

        if name == 'sigma':
            result[name] = list(dict.fromkeys(content))  # preserve order, remove duplicates
        else:
            parsed = [line.split() for line in content if line]
            result[name] = []
            for item in parsed:
                if item not in result[name]:
                    result[name].append(item)

    return result


def is_valid_automaton(nfa):
    required = ['states', 'sigma', 'rules']
    return all(part in nfa for part in required)

def is_valid_rule(rule, nfa):
    states = {state[0] for state in nfa['states']}
    return len(rule) == 3 and rule[0] in states and rule[2] in states and (rule[1] in nfa['sigma'] or rule[1] == 'epsilon')

def validate_rules(nfa):
    return all(is_valid_rule(rule, nfa) for rule in nfa['rules'])

def input_is_valid(input_symbols, sigma):
    return all(symbol in sigma for symbol in input_symbols)

def find_epsilon_transitions(state, rules):
    epsilons = set()
    for rule in rules:
        if rule[0] == state and rule[1] == 'epsilon':
            epsilons.add(rule[2])
    return epsilons

def simulate_nfa():
    nfa = parse_nfa_file("input_nfa.txt")

    if not is_valid_automaton(nfa) or not validate_rules(nfa):
        print("Invalid NFA structure. Check your input file.")
        return

    input_symbols = input("Enter input symbols (space-separated): ").split()
    if not input_is_valid(input_symbols, nfa['sigma']):
        print("Invalid input symbols.")
        return

    start_state = None
    final_states = set()
    for state, tag in nfa['states']:
        if tag == 'S':
            start_state = state
        elif tag == 'F':
            final_states.add(state)

    current_states = {start_state}
    current_states.update(find_epsilon_transitions(start_state, nfa['rules']))
    print(f"Start states: {sorted(current_states)}")

    for symbol in input_symbols:
        next_states = set()
        for curr in current_states:
            for rule in nfa['rules']:
                if rule[0] == curr and rule[1] == symbol:
                    next_states.add(rule[2])
                    # handle epsilon transitions from new state
                    next_states.update(find_epsilon_transitions(rule[2], nfa['rules']))
        current_states = next_states
        print(f"After input '{symbol}': {sorted(current_states)}")

    if any(state in final_states for state in current_states):
        print("Input accepted!")
    else:
        print("Input rejected.")

simulate_nfa()

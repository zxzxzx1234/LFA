def read_pda_file(path):
    from itertools import groupby

    def clean_lines(lines):
        return [ln.strip() for ln in lines if ln.strip() and not ln.startswith('#')]

    def split_by_section(lines):
        result = {}
        grouped = groupby(lines, key=lambda x: x.startswith('[') and x.endswith(']'))

        current_section = None
        for is_header, group in grouped:
            group = list(group)
            if is_header:
                current_section = group[0][1:-1]
                result[current_section] = []
            else:
                if current_section:
                    for line in group:
                        tokens = line.split()
                        if current_section == 'sigma':
                            for sym in tokens:
                                if sym not in result[current_section]:
                                    result[current_section].append(sym)
                        else:
                            result[current_section].append(tokens)
        return result

    with open(path, 'r') as file:
        all_lines = file.readlines()

    return split_by_section(clean_lines(all_lines))

def is_valid_rule(rule, pda):
    if len(rule) != 5:
        return False
    states = {s[0] for s in pda['states']}
    sigma = set(pda['sigma'])
    return (
        rule[0] in states and rule[4] in states and
        all(sym in sigma for sym in rule[1:4])
    )

def all_rules_valid(pda):
    return all(is_valid_rule(rule, pda) for rule in pda['rules'])

def valid_input(input_list, pda):
    return all(symbol in pda['sigma'] for symbol in input_list)

def simulate_pda():
    pda = read_pda_file("input_pda.txt")

    if not {'states', 'sigma', 'rules'}.issubset(pda.keys()):
        print("Missing section in PDA file.")
        return

    if not all_rules_valid(pda):
        print("One or more invalid rules.")
        return

    input_symbols = input("Enter input symbols (space-separated): ").split()
    if not valid_input(input_symbols, pda):
        print("Invalid input symbols.")
        return

    start_state = None
    final_states = set()
    for state, tag in pda['states']:
        if tag == 'S':
            start_state = state
        if tag == 'F':
            final_states.add(state)

    if not start_state:
        print("No start state defined.")
        return

    if pda['rules'][0][0] != start_state:
        print("First rule must start from the start state.")
        return

    curr_state = start_state
    stack = []
    print(f"{curr_state} ->", end=" ")

    for symbol in input_symbols:
        moved = False

        # Apply any possible epsilon transitions first
        while True:
            epsilon_applied = False
            for rule in pda['rules']:
                if rule[0] == curr_state and rule[1] == 'e':
                    pop = rule[2]
                    push = rule[3]
                    if (pop == 'e') or (stack and stack[-1] == pop):
                        if pop != 'e':
                            stack.pop()
                        if push != 'e':
                            stack.append(push)
                        curr_state = rule[4]
                        print(f"{curr_state} ->", stack)
                        epsilon_applied = True
                        break
            if not epsilon_applied:
                break

        # Try to apply transition for current input symbol
        for rule in pda['rules']:
            if rule[0] == curr_state and rule[1] == symbol:
                pop = rule[2]
                push = rule[3]
                if (pop == 'e') or (stack and stack[-1] == pop):
                    if pop != 'e':
                        stack.pop()
                    if push != 'e':
                        stack.append(push)
                    curr_state = rule[4]
                    print(f"{curr_state} ->", stack)
                    moved = True
                    break

        if not moved:
            print("Not accepted!")
            return

    # Final epsilon transitions after input is consumed
    while True:
        epsilon_applied = False
        for rule in pda['rules']:
            if rule[0] == curr_state and rule[1] == 'e':
                pop = rule[2]
                push = rule[3]
                if (pop == 'e') or (stack and stack[-1] == pop):
                    if pop != 'e':
                        stack.pop()
                    if push != 'e':
                        stack.append(push)
                    curr_state = rule[4]
                    print(f"{curr_state} ->", stack)
                    epsilon_applied = True
                    break
        if not epsilon_applied:
            break

    if curr_state in final_states and not stack:
        print("Input accepted!")
    elif curr_state in final_states:
        print("In final state, but stack not empty.")
    else:
        print("Not accepted!")
    print(f"Stack: {stack}")

simulate_pda()

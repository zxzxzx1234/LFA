# Automata Simulator (DFA / NFA / PDA / TM)

Welcome to the Automata Simulator project! This set of Python tools allows you to experiment with multiple types of automata: Deterministic Finite Automata (DFA), Non-deterministic Finite Automata (NFA), Pushdown Automata (PDA), and Turing Machines (TM).

Each component is independent and reads its setup from a custom `.txt` file. You're in full control of states, transitions, alphabets, and input.

---

## ⚙️ Deterministic Finite Automaton (DFA)

DFA is used to simulate a strict path through states based on an input string. There is exactly one transition per symbol from each state.

### File format (example)
```txt
[states]
q0 S
q1 0
q2 F

[sigma]
a
b

[rules]
q0 a q1
q1 b q2
```

- `S` marks the start state
- `F` marks a final state
- Use one line per transition: `source symbol destination`

### Input:
Enter a space-separated list of input symbols at runtime:
```
a b
```

### Output:
- States the automaton passed through
- Whether input was accepted (final state reached)

---

## 🌀 Non-deterministic Finite Automaton (NFA)

NFA allows multiple or no transitions for a given symbol. It supports `epsilon` transitions which consume no input.

### File format (example)
```txt
[states]
q1 S
q2 0
q3 F

[sigma]
a
b
epsilon

[rules]
q1 epsilon q2
q2 a q3
```

### Input:
Provide symbols separated by space:
```
a
```

### Output:
- Lists current states after each input
- Final verdict: accepted or rejected

---

## 📚 Pushdown Automaton (PDA)

PDA uses a stack in addition to states. Transitions depend on input and top of the stack.

### File format (example)
```txt
[states]
q0 S
q1 0
q2 0
q4 F

[sigma]
a
b
e
$

[rules]
q0 e e $ q1
q1 a e a q1
q1 b a e q2
q2 b a e q2
q2 e $ e q4
```

### Input:
Symbols separated by space:
```
a a b b
```

### Output:
- Stack content
- States visited
- Whether accepted (final state and empty stack)

---

## 🧾 Turing Machine (TM)

Simulates a Turing Machine: reads/writes symbols and moves the tape head.

### File format (example)
```txt
[states]
q0 S
qf F

[sigma]
0
1
_

[rules]
q0 1 q0 0 R
q0 0 q0 1 R
q0 _ qf _ R
```

### Input:
Tape symbols separated by space:
```
1 0 1 1 _
```

### Output:
- Final tape after halting
- State progression (optional)

---

## 📦 Notes
- Each automaton requires a properly formatted input file.
- Comments are accepted. ("#")
- Input must match declared `sigma`.
- Invalid or unreachable transitions will halt execution.

Feel free to test, adapt and extend the automata with your own scenarios!

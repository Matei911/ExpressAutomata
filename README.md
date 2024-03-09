# ExpressAutomata

## Overview

ExpressAutomata is a Python library designed for automata theory, facilitating operations with Deterministic Finite Automata (DFA), Non-deterministic Finite Automata (NFA), and regular expressions (regex). It provides tools to validate DFAs, convert NFAs into DFAs using the subset construction algorithm, and parse regular expressions into NFAs.

## Features

- **DFA Validation:** Check if a given deterministic finite automaton is valid.
- **NFA to DFA Conversion:** Convert a non-deterministic finite automaton into a deterministic one using the subset construction algorithm. Includes validation to ensure the conversion process is correctly implemented.
- **Regex to NFA:** Parse a regular expression into a non-deterministic finite automaton. Includes validation to verify the correctness of the transformation from regex to NFA.
- **Transformation Validations:**
  - **Regex to NFA Validation:** Verify the correctness of parsing regular expressions into NFAs, ensuring that the resulting NFA accurately represents the original regex.
  - **NFA to DFA Validation:** Ensure the accuracy of the NFA to DFA conversion process, validating that the resulting DFA correctly represents the NFA's accepted language.
 
## More Information

For more detailed information about how each feature is implemented and validated, please refer to the comments provided within the codebase. Our documentation within the code offers in-depth explanations and insights into the logic and functionality of each component.


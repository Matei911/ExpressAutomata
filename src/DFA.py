from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class DFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], STATE]
    F: set[STATE]

    def accept(self, word: str) -> bool:
        state = self.q0  # Start from the initial state
        for c in word:
            #check if the word is in the alphabet
            if c not in self.S:
                return False
            if (frozenset(state), c) in self.d:
                state = self.d[(frozenset(state), c)]
        return state in self.F



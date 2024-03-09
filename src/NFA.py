from .DFA import DFA

from dataclasses import dataclass
from collections.abc import Callable

EPSILON = ''  # this is how epsilon is represented by the checker in the transition function of NFAs


@dataclass
class NFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], set[STATE]]
    F: set[STATE]

    def epsilon_closure(self, state: STATE) -> set[STATE]:
        # compute the epsilon closure of a state (you will need this for subset construction)
        # see the EPSILON definition at the top of this file
        eps_states = set()
        eps_states.add(state)
        # start a non-recursive dfs
        stack = []
        stack.append(state)
        while stack:
            curr_state = stack.pop()
            if (curr_state, EPSILON) in self.d:
                for eps_state in self.d[(curr_state, EPSILON)]:
                    if eps_state not in eps_states:
                        eps_states.add(eps_state)
                        stack.append(eps_state)
        return eps_states

    def subset_construction(self) -> DFA[frozenset[STATE]]:
        # convert this nfa to a dfa using the subset construction algorithm
        # add the initial state of the DFA
        new_q0 = self.epsilon_closure(self.q0)
        new_f = set()
        DFA_STATES = set()
        dfa_state_list = []
        # new DFA dictionary
        new_d = dict()
        dfa_state_list.append(new_q0)
        while len(dfa_state_list) != 0:
            current_state = dfa_state_list.pop(0)
            if current_state not in DFA_STATES:
                # we add the new DFA state
                current_state = frozenset(current_state)
                DFA_STATES.add(current_state)
                # check if it is a final state
                for final_state in self.F:
                    if final_state in current_state:
                        f_s = frozenset(current_state)
                        new_f.add(f_s)
                for symbol in self.S:
                    # find the next DFA state on the given symbol
                    next_state = set()
                    for state in current_state:
                        if (state, symbol) in self.d:
                            stt = self.d[(state, symbol)]
                            for s in stt:
                                # we add the epsilon closure of the next state
                                next_state = next_state.union(self.epsilon_closure(s))
                    # we create the new dictionary for the DFA
                    next_state = frozenset(next_state)
                    new_d[(current_state, symbol)] = next_state
                    if next_state not in dfa_state_list:
                        dfa_state_list.append(next_state)
                    current_state = frozenset(current_state)

        new_q0 = frozenset(new_q0)
        return DFA(self.S, DFA_STATES, new_q0, new_d, new_f)

    def remap_states[OTHER_STATE](self, f: 'Callable[[STATE], OTHER_STATE]') -> 'NFA[OTHER_STATE]':
        # optional, but may be useful for the second stage of the project. Works similarly to 'remap_states'
        # from the DFA class. See the comments there for more details.
        # apply function f to all states in the NFA
        new_states = set(f(state) for state in self.K)
        new_F = set(f(state) for state in self.F)
        new_q0 = f(self.q0)
        new_d = {(f(state), symbol): {f(next_state) for next_state in states}
                 for (state, symbol), states in self.d.items()}
        return NFA(self.S, new_states, new_q0, new_d, new_F)

from .NFA import NFA
from dataclasses import dataclass
import re

EPSILON = ''  # this is how epsilon is represented by the checker in the transition function of NFAs
class Regex:
    def thompson(self) -> NFA[int]:
        raise NotImplementedError('the thompson method of the Regex class should never be called')

# you should extend this class with the type constructors of regular expressions and overwrite the 'thompson' method
# with the specific nfa patterns. for example, parse_regex('ab').thompson() should return something like:

# >(0) --a--> (1) -epsilon-> (2) --b--> ((3))

# extra hint: you can implement each subtype of regex as a @dataclass extending Regex
@dataclass
class UnionRegex(Regex):
    left: Regex
    right: Regex

    def thompson(self) -> NFA[int]:
        left_nfa = self.left.thompson()
        right_nfa = self.right.thompson()
        new_nfa = NFA(set(), set(), 0, dict(), set())

        new_left_nfa = left_nfa.remap_states(lambda x: x + 1)
        new_right_nfa = right_nfa.remap_states(lambda x: x + max(new_left_nfa.K) + 1)

        new_F = max(new_left_nfa.K.union(new_right_nfa.K)) + 1
        new_nfa.S = new_left_nfa.S.union(new_right_nfa.S)
        new_nfa.K = {0, new_F}.union(new_left_nfa.K.union(new_right_nfa.K))
        # add epsilon transition from the initial state to the initial state of the left and right NFA
        new_nfa.d[(0, EPSILON)] = {new_left_nfa.q0, new_right_nfa.q0}
        # add the transitions of the left and right NFA
        new_nfa.d.update(new_left_nfa.d)
        new_nfa.d.update(new_right_nfa.d)
        # add epsilon transition from the final state of the left and right NFA to the final state of the new NFA
        for state in new_left_nfa.F:
            new_nfa.d[(state, EPSILON)] = {new_F}
        for state in new_right_nfa.F:
            new_nfa.d[(state, EPSILON)] = {new_F}
        # add the final state
        new_nfa.F.add(new_F)
        return new_nfa
@dataclass
class ConcatRegex(Regex):
    left: Regex
    right: Regex

    def thompson(self) -> NFA[int]:
        left_nfa = self.left.thompson()
        right_nfa = self.right.thompson()
        new_nfa = NFA(set(), set(), 0, dict(), set())
        new_right_nfa = right_nfa.remap_states(lambda x: x + max(left_nfa.K) + 1)

        new_nfa.S = left_nfa.S.union(new_right_nfa.S)
        new_nfa.K = left_nfa.K.union(new_right_nfa.K)
        new_nfa.q0 = left_nfa.q0
        new_nfa.d.update(left_nfa.d)
        new_nfa.d.update(new_right_nfa.d)

        # add epsilon transition from the final state of the left NFA to the initial state of the right NFA
        for state in left_nfa.F:
            new_nfa.d[(state, EPSILON)] = {new_right_nfa.q0}
        # add the final state
        new_nfa.F = new_right_nfa.F
        return new_nfa
@dataclass
class KleeneStar(Regex):
    char: Regex

    def thompson(self) -> NFA[int]:
        char_nfa = self.char.thompson()

        new_nfa = NFA(set(), set(), 0, dict(), set())
        new_char_nfa = char_nfa.remap_states(lambda x: x + 1)
        # add two new states
        new_nfa.K.add(0)
        new_F = max(new_char_nfa.K) + 1
        new_nfa.K.add(new_F)
        new_nfa.S = new_char_nfa.S
        new_nfa.K = {new_F}.union(new_char_nfa.K)
        new_nfa.K.add(0)
        new_nfa.F.add(new_F)
        # add the initial transition
        new_nfa.d.update(new_char_nfa.d)
        # add epsilon transition from new_char_nfa final state to the initial state of new_char_nfa
        for state in new_char_nfa.F:
            new_nfa.d[(state, EPSILON)] = {new_char_nfa.q0, new_F}

        # from the initial state of new_nfa add epsilon transition to the initial state of new_char_nfa and to the final state of new_nfa
        new_nfa.d[(0, EPSILON)] = {new_char_nfa.q0, new_F}

        return new_nfa
@dataclass
class Question(Regex):
    char: Regex

    def thompson(self) -> NFA[int]:
        new_nfa = NFA(set(), set(), 0, dict(), set())
        char_nfa = self.char.thompson()
        new_char_nfa = char_nfa.remap_states(lambda x: x + 1)
        new_F = max(new_char_nfa.K) + 1
        new_nfa.S = new_char_nfa.S
        new_nfa.K = {0, new_F}.union(new_char_nfa.K)
        new_nfa.F.add(new_F)
        new_nfa.d[(0, EPSILON)] = {new_char_nfa.q0, new_F}
        new_nfa.d.update(new_char_nfa.d)
        for state in new_char_nfa.F:
            new_nfa.d[(state, EPSILON)] = {new_F}
        return new_nfa

@dataclass
class Plus(Regex):
    char: Regex

    def thompson(self) -> NFA[int]:
        new_nfa = NFA(set(), set(), 0, dict(), set())
        char_nfa = self.char.thompson()
        new_char_nfa = char_nfa.remap_states(lambda x: x + 1)
        new_F = max(new_char_nfa.K) + 1
        new_nfa.S = new_char_nfa.S
        new_nfa.K = {0, new_F}.union(new_char_nfa.K)
        new_nfa.F.add(new_F)
        new_nfa.d[(0, EPSILON)] = {new_char_nfa.q0}
        new_nfa.d.update(new_char_nfa.d)
        for state in new_char_nfa.F:
            new_nfa.d[(state, EPSILON)] = {new_F, new_char_nfa.q0}
        return new_nfa
@dataclass
class SingleChar(Regex):
    value: str
    # we create 4 cases
    # 3 for syntactic sugar and 1 for a normal character
    def thompson(self) -> NFA[int]:
        if self.value == '[0-9]':

            new_nfa = NFA(set(), set(), 0, dict(), set())
            for i in range(10):
                new_nfa.S.add(str(i))
            new_nfa.K.add(0)
            new_nfa.K.add(1)
            new_nfa.F.add(1)
            for i in range(10):
                new_nfa.d[(0, str(i))] = {1}
            return new_nfa
        elif self.value == '[a-z]':
            new_nfa = NFA(set(), set(), 0, dict(), set())
            for i in range(26):
                new_nfa.S.add(chr(i+97))
            new_nfa.K.add(0)
            new_nfa.K.add(1)
            new_nfa.F.add(1)
            for i in range(26):
                new_nfa.d[(0, chr(i+97))] = {1}
            return new_nfa
        elif self.value == '[A-Z]':
            new_nfa = NFA(set(), set(), 0, dict(), set())
            for i in range(26):
                new_nfa.S.add(chr(i+65))
            new_nfa.K.add(0)
            new_nfa.K.add(1)
            new_nfa.F.add(1)
            for i in range(26):
                new_nfa.d[(0, chr(i+65))] = {1}
            return new_nfa

        new_nfa = NFA(set(), set(), 0, dict(), set())
        new_nfa.S.add(self.value)
        new_nfa.K.add(0)
        new_nfa.K.add(1)
        new_nfa.F.add(1)
        new_nfa.d[(0, self.value)] = {1}
        return new_nfa


def parse_regex(regex: str) -> Regex:
    # remove all unnecessary spaces from the regex
    regex = re.sub(r'(?<!\\) ', '', regex)
    # helper functions for parsing the regex that are called recursively
    def union_pars():
        # Check for concatenation first
        left = concat_pars()
        if regex and regex[0] == '|':
            regex.pop(0)  # Remove the '|'
            right = union_pars()
            return UnionRegex(left, right)
        return left

    def concat_pars():
        left = symbol_parse()
        while regex and regex[0] not in '|)':
            right = symbol_parse()
            left = ConcatRegex(left, right)
        return left


    def symbol_parse():
        if regex[0] == '(':
            # check if the regex is between brackets
            regex.pop(0)  # Remove '('
            result = union_pars()
            if regex[0] == ')':
                regex.pop(0)  # Remove ')'
                # regex.pop(0)  # Remove the special character
                if regex:
                    if regex[0] == '*':
                        regex.pop(0)
                        return KleeneStar(result)
                    elif regex[0] == '?':
                        regex.pop(0)
                        return Question(result)
                    elif regex[0] == '+':
                        regex.pop(0)
                        return Plus(result)
                return result
        else:
            if regex[0] == '\\':
                regex.pop(0)
                if regex:  # check for characters after '\'
                    char = regex.pop(0)
                    return SingleChar(char)
            else:
                char = regex.pop(0)
                if regex:
                    # regex.pop(0)  # Remove the special character
                    if regex[0] == '*':
                        regex.pop(0)
                        return KleeneStar(SingleChar(char))
                    elif regex[0] == '?':
                        regex.pop(0)
                        return Question(SingleChar(char))
                    elif regex[0] == '+':
                        regex.pop(0)
                        return Plus(SingleChar(char))
                return SingleChar(char)

    # Convert the regex string to a list for easier manipulation
    # if a [ is found the put in the list the whole expression inside the brackets
    stack = []
    i = 0
    while i < len(regex):
        ch = ''
        if regex[i] == '[':
            ch += regex[i]
            ch += regex[i+1]
            ch += regex[i+2]
            ch += regex[i+3]
            ch += regex[i+4]
            i += 5
            stack.append(ch)
        else:
            stack.append(regex[i])
            i += 1
    regex = stack
    return union_pars()
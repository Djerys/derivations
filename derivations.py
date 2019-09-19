import re


def get_rules(string_rules: str):
    string_rules_list = re.findall(r'\w\s*->\s*\w*', string_rules)
    rules = []
    for string_rule in string_rules_list:
        rule_sides = re.split(r'\s*->\s*', string_rule)
        rules.append(Rule(rule_sides[0], rule_sides[1]))
    return rules


class Rule(object):
    def __init__(self, left, right):
        self.left = left
        self._right = '' if right == 'eps' else right

    def __repr__(self):
        return f'{self.left} -> {self.right}'

    @property
    def right(self):
        return 'ε' if not self._right else self._right

    def can_apply_left(self, chain):
        return self._can_apply(self.apply_left, chain)

    def can_apply_right(self, chain):
        return self._can_apply(self.apply_right, chain)

    def can_apply(self, chain):
        return self._can_apply(self.apply_right, chain)

    def apply_left(self, chain):
        return self._apply(chain, 1, True)

    def apply_right(self, chain):
        return self._apply(chain, -1, True)

    def apply(self, chain):
        return self._apply(chain, 1, False)

    def _apply(self, chain: str, direction, should_first):
        for symbol in chain[::direction]:
            if should_first and symbol.isupper() and not self.left == symbol:
                raise CanNotApplyError(
                    f'Can not apply to {chain}: '
                    f'first nonterminal is {symbol}'
                )
            elif self.left == symbol:
                return self._apply_rule(chain, direction)

        raise CanNotApplyError(f'Can not apply to {chain}: no such nonterminal')

    def _apply_rule(self, chain, direction):
        partition = str.partition if direction >= 0 else str.rpartition
        left, _, right = partition(chain, self.left)
        return left + self._right + right

    @staticmethod
    def _can_apply(apply_func, chain):
        try:
            apply_func(chain)
        except CanNotApplyError:
            return False
        return True


class CanNotApplyError(Exception):
    pass

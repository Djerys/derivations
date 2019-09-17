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
        self.right = '' if right == 'eps' else right

    def __repr__(self):
        right = 'ε' if not self.right else self.right
        return f'{self.left} -> {right}'

    def can_apply_left(self, chain):
        return self._can_apply(chain, self.apply_left)

    def can_apply_right(self, chain):
        return self._can_apply(chain, self.apply_right)

    def can_apply(self, chain):
        return self._can_apply(chain, self.apply)

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
                return chain.replace(symbol, self.right)

        raise CanNotApplyError(f'Can not apply to {chain}: no such nonterminal')

    @staticmethod
    def _can_apply(chain, apply_func):
        try:
            apply_func(chain)
        except CanNotApplyError:
            return False
        return True


class CanNotApplyError(Exception):
    pass

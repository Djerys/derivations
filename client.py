from abc import ABC, abstractmethod

import derivations
import trees


class DerivationClient(ABC):
    message_to_end = ('Введите "выход" чтобы закончить, '
                      'либо что-то другое для продолжения: ')
    end = 'выход'
    grammar_input_message = 'Введите КС-грамматику: '

    def loop(self):
        while True:
            message = input(self.message_to_end)
            if message == self.end:
                break
            print(self.grammar_input_message)
            rules = self._get_input_rules()
            self._do_main_work(rules)
            self._print_result()
            print()

    @staticmethod
    def _get_input_rules():
        string_rules = ''
        while True:
            input_rules = input()
            if not input_rules:
                break
            string_rules += f' {input_rules}'
        return derivations.get_rules(string_rules)

    @abstractmethod
    def _do_main_work(self, rules):
        pass

    @abstractmethod
    def _print_result(self):
        pass


class DeterminantClient(DerivationClient):
    def __init__(self):
        self.can_apply_rules = None

    def _do_main_work(self, rules):
        self.chain = 'S'
        string_rules_number = input('Последовательность правил: ')
        rules_number = [int(s) - 1 for s in string_rules_number if s.isdigit()]
        for rule_number in rules_number:
            rule = rules[rule_number]
            if self._can_apply(rule):
                self.chain = self._apply(rule)
            else:
                self.can_apply_rules = False
                return
        self.can_apply_rules = True

    def _print_result(self):
        print('Результат:', end=' ')
        if self.can_apply_rules:
            print('да')
        else:
            print('нет')

    @abstractmethod
    def _apply(self, rule):
        pass

    @abstractmethod
    def _can_apply(self, rule):
        pass


class LeftDerivationClient(DerivationClient):
    def __init__(self):
        self.tree = None
        self.chain = None

    def _do_main_work(self, rules):
        self.chain = 'S'
        self.tree = trees.NonTerminalNode(self.chain)
        while not self.chain.islower():
            print('Промежуточная цепочка:', self.chain)
            print('Можно применить:')
            self.__print_possible_rules(rules)
            rule_number = int(input('Применяем правило: ')) - 1
            try:
                rule = rules[rule_number]
                self.chain = rule.apply_left(self.chain)
                children = [trees.LeafNode(c) if c.islower()
                            else trees.NonTerminalNode(c) for c in rule.right]
                self.tree.add(children)
            except derivations.CanNotApplyError:
                print('Вы ввели номер правила, которое нельзя применить.')
            print()

    def _print_result(self):
        print('Терминальная цепочка:', self.chain)
        print('ЛСФ ДВ:', self.tree)

    def __print_possible_rules(self, rules):
        for index, rule in enumerate(rules, 1):
            if rule.can_apply_left(self.chain):
                print(f'{index}. {rule}')


class DerivationDeterminantClient(DeterminantClient):
    def _apply(self, rule):
        return rule.apply(self.chain)

    def _can_apply(self, rule):
        return rule.can_apply(self.chain)


class LeftDerivationDeterminantClient(DeterminantClient):
    def _apply(self, rule):
        return rule.apply_left(self.chain)

    def _can_apply(self, rule):
        return rule.can_apply_left(self.chain)

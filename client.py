import cf_derivations


class LeftDerivationClient(object):
    def __init__(self):
        self.chain = 'S'

    def loop(self):
        while True:
            message = input(
                'Введите "выход" чтобы закончить, '
                'либо что-то другое для продолжения: ').lower()
            if message == 'выход':
                break
            print('Введите КС-грамматику:')
            rules = cf_derivations.get_rules(self._input_rules())
            self.chain = 'S'
            while not self.chain.islower():
                print('Промежуточная цепочка:', self.chain)
                print('Можно применить:')
                self._print_possible_rules(rules)
                rule_number = int(input('Применяем правило: ')) - 1
                try:
                    self.chain = rules[rule_number].apply_left(self.chain)
                except cf_derivations.CanNotApplyError:
                    print('Вы ввели номер правила, которое нельзя применить.')
                print()
            print('Терминальная цепочка:', self.chain)

    def _input_rules(self):
        string_rules = ''
        while True:
            input_rules = input()
            if not input_rules:
                break
            string_rules += f' {input_rules}'
        return string_rules

    def _print_possible_rules(self, rules):
        for index, rule in enumerate(rules, 1):
            if rule.can_apply_left(self.chain):
                print(f'{index}. {rule}')
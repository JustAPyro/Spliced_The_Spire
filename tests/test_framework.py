from src.Cards.Red import RedStrike


class STSTestCase:
    header = (
        '\tdef test_{test_case_name}(self):'
        '\n\t\t"""'
        '\n\t\t{test_description}'
        '\n\t\t"""\n'
    )

    def __init__(self, test_case_name, test_description):
        self.test_case_name = test_case_name
        self.test_description = test_description

    def suite_imports(self):
        return []

    def setup(self):
        return ''

    def execute(self):
        return ''

    def assertions(self):
        return ''

    def output(self):
        return (STSTestCase.header.format(
            test_case_name=self.test_case_name,
            test_description=self.test_description)
                + '\t\t# Set up\n' + self.setup()
                + '\t\t# Execute\n' + self.execute()
                + '\t\t# Assert\n' + self.assertions())


class TestDealsDamage(STSTestCase):
    def __init__(self, damage):
        self.damage = damage
        super().__init__('use_card', 'test that card does the correct damage')

    def imports(self):
        return ['from src.Cards.Red import RedStrike'] + self.suite_imports()
    def setup(self):
        return (
            f'\t\tmonster = TestMonster(100)\n'
            f'\t\tcard = RedStrike\n'
        )

    def execute(self):
        return (
            '\t\tcard.userCard(monster)\n'
        )

    def assertions(self):
        return f'\t\tself.assertEqual(monster.current_health, {100-self.damage}, Monster health/damage incorrect)\n'


class TestDealsDamageUpgraded():
    pass


class STSTestSuite:
    def __init__(self, card):
        self.card_name = card.__name__
        self.test_suite_name = 'Test' + self.card_name
        self.test_file_name = 'test_' + self.card_name + '.py'
        self.cases = card.get_test_cases()

    def output(self):
        output = 'import unittest\n'
        for test_case in self.cases:
            for importing in test_case.imports():
                output = output + importing + '\n'

        output += f'\n\nclass {self.test_suite_name}(unittest.TestCase):\n'

        if self.cases is None or len(self.cases) < 1:
            output += '\tpass\n'
        else:
            for case in self.cases:
                output += case.output()

        return output

    def create(self):
        with open(self.test_file_name, 'w') as f:
            f.write(self.output())



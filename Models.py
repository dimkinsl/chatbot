from transitions import Machine

# Обработка логики преходов стейт-машины
# Класс для автоматов и хранения переменных
class Matter(object):
    def __init__(self):
        self.set_environments()

    def set_environments(self, size='', pay_options=''):
        self.size = size
        self.pay_options = pay_options

    def get_environments(self):
        return self.size, self.pay_options

lump = Matter()
states = ['start', 'pay', 'yes_no', 'finish']

transitions = [
    {'trigger': 'choice_pizza', 'source': 'start', 'dest': 'pay'},
    {'trigger': 'choice_pay', 'source': 'pay', 'dest': 'yes_no'},
    {'trigger': 'final_question', 'source': 'yes_no', 'dest': 'finish'},
]

machine = Machine(lump, states=states, transitions=transitions, initial='start')


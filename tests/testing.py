class AbstractEnemy:
    def __init__(self, name):
        self.name = name

    def before(self):
        print('before')

    def after(self):
        print('after')

    @staticmethod
    def ability(func):
        def wrapper(self):
            self.before()
            func(self)
            self.after()

        return wrapper


class Child(AbstractEnemy):

    def __init__(self, x, name):
        super().__init__(name)
        self.x = x

    def before(self):
        print('rawr'+str(self.x))

    def after(self):
        print('yum')

    @AbstractEnemy.ability
    def hello(self):
        print('hello')


x = Child(5, 'luke')
x.hello()

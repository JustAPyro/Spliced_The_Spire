class Parent():
    def __init__(self):
        self.name = type(self).__name__


class Child(Parent):
    def __init__(self):
        super().__init__()


x = Child()
print(x.name)

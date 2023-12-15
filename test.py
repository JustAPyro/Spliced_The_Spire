class Parent:
    things_that_have_a_method = []

    def __init__(self):
        if type(self).a_method != Parent.a_method:
            Parent.things_that_have_a_method.append(self)

    def a_method(self):
        pass


class Child(Parent):
    def a_method(self):
        print(f'I am a {type(self)}')


class Child2(Parent):
    pass


a = Child()
b = Child2()
c = Child2()

for x in Parent.things_that_have_a_method:
    x.a_method()


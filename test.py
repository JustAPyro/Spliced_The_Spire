class Parent:
    classes_with_method = []

    def __init__(self):
        print(type(self).method)
        print(Parent.method)
        if type(self).method != Parent.method:
            Parent.classes_with_method.append(self)


    def method(self):
        pass

    def method2(self):
        pass

class ChildWithMethod(Parent):
    def method(self):
        print("Do stuff")

class ChildWithoutMethod(Parent):
    pass

a = ChildWithoutMethod()
c = ChildWithoutMethod()
b = ChildWithMethod()
x = ChildWithMethod()

for x in Parent.classes_with_method:
    x.method()


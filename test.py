class Parent:
    def __init__(self):
        pass

    class Message():
        def __init__(self):
            self.message = NotImplemented

        def set_message(self, message):
            self.message = message

        def has_message(self):
            return self.message is not NotImplemented

    @staticmethod
    def do_twice(func):
        def wrapper_do_twice(*args, **kwargs):
            self = args[0]
            message = Parent.Message()
            func(self, message.set_message)
            if not message.has_message():
                raise Exception(' Didnt init!')

        return wrapper_do_twice


class Child(Parent):
    def __init__(self):
        super().__init__()

    @Parent.do_twice
    def prin(self, var):
        var('hi')
        print('hello!')
        print(var)


c = Child()
c.prin()

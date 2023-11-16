class foo:
    def __init__(self, x):
        self.x = x

    def __str__(self):
        return self.x

a = foo(1)
b = foo(2)
c = foo(2)

l1 = [a, b, c]
l2 = [b, c]
set([l1, l2])
class Obj:
    def __init__(self, i: int):
        self.num = i

one = Obj(1)
two = Obj(2)

s = {one, two}
for x in s:
    print(x.num)
    x.num = 0

for x in s:
    print(x.num)

print('--')
s.remove(one)
for x in s: print(x.num)
print('--')
s.add(Obj(3))
for x in s: print(x.num)



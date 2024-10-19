from functools import cmp_to_key

lines = open("d13.txt").read().split("\n\n")
pairs = [tuple(eval(el) for el in l.split("\n")) for l in lines]

def to_list(a):
    return [a] if type(a) is int else a

def compare(a, b):
    if type(a) is int and type(b) is int:
        return 0 if a == b else -1 if a < b else 1
    a = to_list(a)
    b = to_list(b)
    res = next((res for x, y in zip(a, b) for res in [compare(x, y)] if res is not None), None)
    return res if res is not None else 0 if len(a) == len(b) else -1 if len(a) < len(b) else 1

sum(i + 1 for i, (a, b) in enumerate(pairs) if compare(a, b) == 1)

p1 = [[2]]
p2 = [[6]]
res = sorted([*[p1,p2],*[x for p in pairs for x in p]], key = cmp_to_key(compare))
(res.index(p1) + 1) * (res.index(p2) + 1)

def cmp_to_key2(f):
    def key_func(el):
        pass 
    return key_func
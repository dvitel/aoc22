from collections import deque
from functools import reduce
import operator
import re 
text = open("d11.txt").read()

op_regex = re.compile(r"""Monkey (?P<id>\d+):
  Starting items: (?P<items>.*)
  Operation: new = (?P<expr>.*)
  Test: divisible by (?P<test_v>.*)
    If true: throw to monkey (?P<true_monkey>.*)
    If false: throw to monkey (?P<false_monkey>.*)""")

ops = {"*": operator.mul, "+": operator.add}

monkeys = [(deque(int(s) for s in items.split(",")),
            lambda v,a=a,op=ops[op],b=b: op(v if a == "old" else a, v if b == "old" else b), #op
            lambda v,true_m_num=true_m_num,test_v_num=test_v_num,false_m_num=false_m_num: true_m_num if v % test_v_num == 0 else false_m_num,
            [0], test_v_num) 
        for (_, items, expr, test_v, true_m, false_m) in op_regex.findall(text) 
        for (test_v_num, true_m_num, false_m_num) in [(int(test_v), int(true_m), int(false_m))]
        for a_s, op, b_s in [expr.split(" ")]
        for a, b in [(int(a_s) if a_s != "old" else a_s, int(b_s) if b_s != "old" else b_s)]]
    
monkey_max_val = reduce(operator.mul, [test_v_num for (_, _, _, _, test_v_num) in monkeys])

for _ in range(10000):    
    for (items, op, test, stats, test_v_num) in monkeys:
        while len(items) > 0:
            item = items.popleft()
            worry = op(item) % monkey_max_val #//3
            next_m = test(worry)
            monkeys[next_m][0].append(worry)
            stats[0] += 1

reduce(operator.mul, sorted(n for (_, _, _, [n],_) in monkeys)[-2:])
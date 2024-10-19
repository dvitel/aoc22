from collections import deque

X = 1
def noop():
    pass 

def addx(v):
    global X 
    X += v

cycles = {noop: 1, addx: 2}    

lines = open("d10.txt").read().splitlines()
cmds = deque((fn, [int(arg) for arg in c[1:]], cycles[fn]) for l in lines for c in [l.split(' ')] for fn in [globals()[c[0]]])

# cycle = 20 
# cur_cycle = 0
# res = 0
# while len(cmds) > 0:
#     fn, args, cost = cmds.popleft()
#     cur_cycle += cost 
#     if cur_cycle >= cycle: 
#         print(f"cycle {cycle}, X = {X}")
#         res += X * cycle
#         cycle += 40     
#     fn(*args)

cur_cycle = 0
res = ""
while len(cmds) > 0 and cur_cycle < 240:
    fn, args, cost = cmds.popleft()
    for _ in range(cost):
        crt_pos = cur_cycle % 40 + 1
        res += "#" if (crt_pos - 1) >= X - 1 and (crt_pos - 1) <= X + 1 else "."
        print(f"pos {crt_pos}, X {X}:\n{res}")
        if crt_pos == 40:
            res += "\n"
        cur_cycle += 1
    fn(*args)

print(res)    
import os
lines = open("d7.txt").read().splitlines()

fs = {}
cur_dir = "/"

def get_parent_dirs(cur_dir: str): 
    while cur_dir != "/":
        cur_dir = os.path.dirname(cur_dir)
        yield cur_dir

for line in lines: 
    [sz_or_prompt, cmd_or_name, *path] = line.split()
    if sz_or_prompt != "$" and sz_or_prompt != "dir":        
        sz = int(sz_or_prompt)
        file_name = os.path.join(cur_dir, cmd_or_name)
        if file_name in fs: 
            continue
        fs[file_name] = (sz, "f")
        for parent_dir in get_parent_dirs(file_name):
            fs[parent_dir] = (fs.get(parent_dir, (0, "d"))[0] + sz, "d")
    elif sz_or_prompt == "$" and cmd_or_name == "cd":
        target_dir = path[0]
        if target_dir.startswith("/"):
            cur_dir = target_dir
        elif target_dir == "..":
            cur_dir = os.path.dirname(cur_dir)
        else:
            cur_dir = os.path.join(cur_dir, target_dir)

part1 = sum(sz for _, (sz, flag) in fs.items() if flag == 'd' and sz <= 100000)       

required_size, max_size = 30000000, 70000000
left = required_size - (max_size - fs["/"][0])
dirs = sorted(sz for _, (sz, f) in fs.items() if f == 'd')
part2 = next(d for d in dirs if d >= left)
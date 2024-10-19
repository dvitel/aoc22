jets = open("d17.txt").read()
rocks = [ [ "1111" ], [ ".2.", "222", ".2." ], [ "..3", "..3", "333" ], [ "4", "4", "4", "4" ], [ "55", "55" ] ]

left_appear, bottom_apper = 2, 3
grid = []
grid_w = 7
 
rock_id = jet_id = 0
rock_markers = {}
for i in range(2022):  #range(2022 * 2):    
    start_grid_height = len(grid)
    rock = rocks[rock_id]
    rock_h, rock_w = len(rock), len(rock[0])    
    rock_x, rock_y = 2, 0    
    grid = [ *[list('.' * grid_w) for _ in range(bottom_apper + rock_h)], *grid]    
    def assert_rock():
        assert 0 <= rock_x and (rock_x + rock_w) <= grid_w 
        assert 0 <= rock_y and (rock_y + rock_h) <= len(grid)
        assert all(ch1 == '.' or ch2 == '.' 
                    for l1, l2 in zip(grid[rock_y:rock_y + rock_h], rock) 
                    for ch1, ch2 in zip(l1[rock_x:rock_x + rock_w], l2))    
    while True: #falling 
        jet = jets[jet_id]
        assert jet == '>' or jet == '<'        
        assert_rock()
        jet_id = (jet_id + 1) % len(jets)
        delta_x = -1 if jet == '<' else 1
        new_rock_x = rock_x + delta_x
        if 0 <= new_rock_x <= (grid_w - rock_w):
            grid_part = [line[new_rock_x:new_rock_x+rock_w] for line in grid[rock_y:rock_y + rock_h]]
            if all(ch1 == '.' or ch2 == '.' for l1, l2 in zip(grid_part, rock) for ch1, ch2 in zip(l1, l2)): #can move 
                rock_x = new_rock_x
        assert_rock()
        if (rock_y + rock_h == len(grid)) or any(ch1 != '.' and ch2 != '.' 
                                                    for l1, l2 in zip(rock, grid[rock_y + 1:rock_y + 1 + rock_h])
                                                    for ch1, ch2 in zip(l1, l2[rock_x:rock_x + rock_w])): #stop
            # assert 0 <= rock_y and rock_y + rock_h <= len(grid)
            for line, rock_line in zip(grid[rock_y:rock_y + rock_h], rock):
                # assert 0 <= rock_x and rock_x + rock_w <= grid_w
                # if any(ch1 != '.' and ch2 != '.' for ch1, ch2 in zip(line[rock_x:rock_x + rock_w], rock_line)):
                #     assert all(ch1 == '.' or ch2 == '.' for ch1, ch2 in zip(line[rock_x:rock_x + rock_w], rock_line))
                line[rock_x:rock_x + rock_w] = [ ch1 if ch1 != '.' else ch2 for ch1, ch2 in zip(rock_line, line[rock_x:rock_x + rock_w]) ]            
            # print("jet_id: ", jet_id, "rock_id", rock_id)
            # print("\n".join("".join(l) for l in grid))    
            # print()            
            # assert all(any(ch != '.' for ch in l) for l in grid)
            rock_marker = (rock_id, jet_id, "\n".join("".join(l) for l in grid[0:rock_h]))
            # if rock_marker in rock_markers and period == 0: #period detected 
            #     shift, shift_grow = rock_markers[rock_marker]
            #     period = i - shift
            #     period_grow = len(grid) - shift_grow
            rock_markers.setdefault(rock_marker, []).append((i, start_grid_height))
            break
        else: #move down            
            if all(ch == '.' for ch in grid[0]):
                _ = grid.pop(0)
            else:
                rock_y += 1
            assert_rock()
    rock_id = (rock_id + 1) % len(rocks)

len(grid) #part 1

(first_rock_i, first_rock_height), (next_rock_i, next_rock_height), *_ = min((vs for vs in rock_markers.values() if len(vs) > 1), key = lambda x:x[0][0])
period = next_rock_i - first_rock_i
period_height = next_rock_height - first_rock_height
part_of_period = first_rock_i + (1000000000000 - first_rock_i) % period
shift_i, shift_height = next(vs[0] for vs in rock_markers.values() if vs[0][0] == part_of_period)
shift_height + period_height * (1000000000000 - shift_i) / period #part2
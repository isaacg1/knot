dirs = {
    ' ': set(),
    '│': {0, 2},
    '─': {1, 3},
    '┌': {1, 2},
    '┐': {2, 3},
    '└': {0, 1},
    '┘': {0, 3},
}
    
def all_grids(side):
    grids = [[]]
    for row in range(side):
        grids = [grid + [[]] for grid in grids]
        for col in range(side):
            next_grids = []
            for working_grid in grids:
                # 0 is up, 1 is right, etc.
                allowed_chars = set(' │─┌┐└┘')
                
                # up allowed and required
                if row > 0:
                    if 2 in dirs[working_grid[row-1][col]]:
                        allowed_chars -= set(' ┌┐')
                        if row == side - 1:
                            allowed_chars -= set('─')
                    # Already had a crossing
                    elif (working_grid[row-1][col] == '─' and row > 1
                          and 2 in dirs[working_grid[row-2][col]]):
                        allowed_chars -= set(' ─┌┐')
                    else:
                        allowed_chars -= set('│└┘')
                else:
                    allowed_chars -= set('│└┘')
                # left allowed and required
                if col > 0:
                    if 1 in dirs[working_grid[row][col-1]]:
                        allowed_chars -= set(' ┌└')
                        if col == side - 1:
                            allowed_chars -= set('│')
                    elif (working_grid[row][col-1] == '│' and col > 1
                          and 1 in dirs[working_grid[row][col-2]]):
                        allowed_chars -= set(' │┌└')
                    else:
                        allowed_chars -= set('─┐┘')
                else:
                    allowed_chars -= set('─┐┘')
                # down not allowed
                if row == side - 1:
                    allowed_chars -= set('│┌┐')
                # right not allowed
                if col == side - 1:
                    allowed_chars -= set('─└┌')
                for char in sorted(allowed_chars):
                    new_grid = working_grid[:]
                    new_grid[row] = working_grid[row] + [char]
                    next_grids.append(new_grid)
            print(row, col, len(next_grids))
            grids = next_grids
    return grids

def pretty(grid):
    return '\n'.join(''.join(row) for row in grid)

def advance(pos, dir):
    if dir == 0:
        return pos[0]-1, pos[1]
    if dir == 1:
        return pos[0], pos[1]+1
    if dir == 2:
        return pos[0]+1, pos[1]
    if dir == 3:
        return pos[0], pos[1]-1
    assert False

def notate(grid):
    side = len(grid)
    assert side == len(grid[0])
    color = [[None for _ in range(side)] for _ in range(side)]
    endpoints = []
    pos = None
    dir = None
    for row in range(side):
        for col in range(side):
            if grid[row][col] != ' ':
                pos = row, col
                dir = (sorted(dirs[grid[row][col]])[0] + 2) % 4
                break
        if pos is not None:
            break
    if pos is None:
        return None
    start_pos = pos
    start_dir = dir
    while pos != start_pos or color[pos[0]][pos[1]] is None:
        char = grid[pos[0]][pos[1]]
        # Crossing, end of color
        reverse_dir = (dir + 2) % 4
        if reverse_dir not in dirs[char]:
            endpoints.append(pos)
            # dir doesn't change
            dir = dir
        else:
            color[pos[0]][pos[1]] = len(endpoints)
            new_dirs = dirs[char] - {reverse_dir}
            dir = new_dirs.pop()
            assert not new_dirs
        pos = advance(pos, dir)
        #print(pos, dir)
        #print('\n'.join(''.join(str(cell) if cell is not None else '.' for cell in row) for row in color))
    for row in range(side):
        for col in range(side):
            if grid[row][col] != ' ' and color[row][col] is None:
                # Not a single loop
                return None
    return tuple(color[row][col] % len(endpoints) for row, col in endpoints)


def find_all(max_side):
    for side in range(1, max_side + 1):
        seen = set()
        grids = all_grids(side)
        for grid in grids:
            note = notate(grid)
            if note not in seen:
                seen.add(note)
                print(pretty(grid))
                print(note)
    print(len(seen))

def find(goal_note):
    side = 1
    while True:
        grids = all_grids(side)
        for grid in grids:
            note = notate(grid)
            if note == goal_note:
                return grid
        side += 1


print(pretty(find((2, 3, 0, 1))))

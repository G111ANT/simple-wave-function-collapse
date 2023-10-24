import random
import copy

def collapse(canvas_item:list, target:list, key:dict, target_key:str) -> (list, str):
        possibility_local = []
        [[possibility_local.append(j) for j in key[i][target_key]] for i in canvas_item]
        possibility_local = tuple(set(possibility_local))
        if len(possibility_local) == len(key):
            return(target, 0)
        final_target = [i for i in target if i in possibility_local]
        changes = len(target)-len(final_target)
        return(final_target, changes)

def paste_canvas(canvas:list, cord:list) -> list:
    for y in range(len(canvas[1])):
        for x in range(len(canvas[1][y])):
            canvas[0][cord[1]+y][cord[0]+x] = canvas[1][y][x]
    return(canvas[0])

def copy_canvas(canvas:list, cords:list) -> list:
    return([y[cords[0][0]:cords[1][0]] for y in canvas[cords[0][1]:cords[1][1]]])

def crop_canvas(canvas:list, bounds:list) -> list:
    return([y[bounds[0][0]:-bounds[1][0]] for y in canvas[bounds[0][1]:-bounds[1][1]]])

def wave_function(canvas:list, key:dict, tries=100, iterations=100000, fast_mode=False) -> list:
    canvas = copy.deepcopy(canvas)
    no_enth = len(key)
    canvas_len = (len(canvas[0]), len(canvas))
    canvas_copy = copy.deepcopy(canvas)
    progress = []
    iterations_copy = iterations
    while tries > 0 and iterations > 0:
        changes = 1
        while changes != 0:
            changes = 0
            for y in range(canvas_len[1]):
                for x in range(canvas_len[0]):
                    if y > 0 and len(canvas[y-1][x]) < no_enth:
                        canvas[y][x], ret_change = collapse(canvas[y-1][x], canvas[y][x], key, "north")
                        changes += ret_change
                    if y < canvas_len[1]-1 and len(canvas[y+1][x]) < no_enth:
                        canvas[y][x], ret_change = collapse(canvas[y+1][x], canvas[y][x], key, "south")
                        changes += ret_change
                    if x > 0 and len(canvas[y][x-1]) < no_enth:
                        canvas[y][x], ret_change = collapse(canvas[y][x-1], canvas[y][x], key, "east")
                        changes += ret_change
                    if x < canvas_len[0]-1 and len(canvas[y][x+1]) < no_enth:
                        canvas[y][x], ret_change = collapse(canvas[y][x+1], canvas[y][x], key, "west")
                        changes += ret_change
            iterations -= 1
            if iterations < 0:
                tries -= 1
                if tries < 0:
                    break
                iterations = iterations_copy
        enth = []
        enth_count = []
        for y in range(canvas_len[1]):
            for x in range(canvas_len[0]):
                enth_local_len = len(canvas[y][x])
                if enth_local_len > 1:
                    enth.append([enth_local_len, [x, y]])
                    enth_count_len = [i[0] for i in enth_count]
                    if enth_local_len not in enth_count_len:
                        enth_count.append([enth_local_len, 1])
                    else:
                        enth_count[enth_count_len.index(enth_local_len)][1] += 1
                elif enth_local_len == 0:
                    print("\n".join(["".join([(str(len(x))[1] if len(x) != 1 else x[0]) for x in y]) for y in canvas[::-1]]))
                    canvas = copy.deepcopy(canvas_copy)
                    progress = []
                    iterations = iterations_copy
                    tries -= 1
                    break
            else:
                continue
            break
        else:
            enth.sort()
            enth_count.sort()
            if not fast_mode:
                progress.append(copy.deepcopy(canvas))
            if len(enth) == 0:
                break
            if enth_count[0][1] == 1:
                pick = enth[:enth_count[0][1]][0]
            else:
                pick = random.choice(enth[:enth_count[0][1]])
            canvas[pick[1][1]][pick[1][0]] = [random.choice(canvas[pick[1][1]][pick[1][0]])]
    else:
        return(False)
    if fast_mode:
        return(canvas)
    return(progress)

def wave_function_checker(canvas:list, key:dict, canvas_size=[7, 7], overlap=[2, 2], tries=100, iterations=100000, fast_mode=False) -> list:
    split_len = (round(len(canvas[0])/canvas_size[0]), round(len(canvas)/canvas_size[1]))
    progress = []
    for y in range(split_len[1]):
        for x in range(split_len[0]):
            overlap_bounds = (
                (max((x*canvas_size[0])-overlap[0], 0), max((y*canvas_size[1])-overlap[1], 0)),
                (min(((x+1)*canvas_size[0])+overlap[0], len(canvas[0])-1), min(((y+1)*canvas_size[1])+overlap[1], len(canvas)-1))
            )
            wave = wave_function(copy_canvas(canvas, overlap_bounds), key, tries, iterations, fast_mode)
            if wave:
                if fast_mode:
                    canvas = paste_canvas([canvas, crop_canvas(wave, [[0, 0], overlap])], overlap_bounds[0])
                else:
                    for i in wave:
                        progress.append(copy.deepcopy(paste_canvas([canvas, crop_canvas(i, [[0, 0], overlap])], overlap_bounds[0])))
                    canvas = copy.deepcopy(progress[-1])
            else:
                return(False)
    wave = wave_function(canvas, key, tries, iterations, fast_mode)
    if wave:
        if fast_mode:
            return(wave)
        progress += wave
    else:
        return(False)
    return(progress)
import random
import math
import os
import copy

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def collapse(canvas:list, target:list, key:dict, target_key:str) -> (list, str):
        possibility_local = []
        [[possibility_local.append(j) for j in key[i][target_key]] for i in canvas]
        possibility_local = list(set(possibility_local))
        if len(possibility_local) == len(list(key)):
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

def wave_function(canvas:list, key:dict, tries=100, iterations=100000) -> list:
    canvas = copy.deepcopy(canvas)
    no_enth = len(key.keys())
    canvas_len = (len(canvas[0]), len(canvas))
    canvas_copy = copy.deepcopy(canvas)
    progress = []
    iterations_copy = iterations
    while tries > 0 and iterations > 0:
        changes = math.inf
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
                if len(canvas[y][x]) > 1:
                    enth.append([len(canvas[y][x]), [x, y]])
                    enth_count_len = [i[0] for i in enth_count]
                    if len(canvas[y][x]) not in enth_count_len:
                        enth_count.append([len(canvas[y][x]), 1])
                    else:
                        enth_count[enth_count_len.index(len(canvas[y][x]))][1] += 1
                elif len(canvas[y][x]) == 0:
                    print("\n".join(["".join([(str(len(x)) if len(x) != 1 else x[0]) for x in y]) for y in canvas[::-1]]))
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
            progress.append(copy.deepcopy(canvas))
            if len(enth) == 0:
                break
            pick = random.choice(enth[:enth_count[0][1]])
            canvas[pick[1][1]][pick[1][0]] = [random.choice(canvas[pick[1][1]][pick[1][0]])]
    else:
        return(False)
    return(progress)

def wave_function_checker(canvas:list, key:dict, canvas_size=[7, 7], overlap=[2, 2], tries=100, iterations=100000) -> list:
    split_len = (math.ceil(len(canvas[0])/canvas_size[0]), math.ceil(len(canvas)/canvas_size[1]))
    progress = []
    for y in range(split_len[1]):
        for x in range(split_len[0]):
            overlap_bounds = [
                [max((x*canvas_size[0])-overlap[0], 0), max((y*canvas_size[1])-overlap[1], 0)],
                [min(((x+1)*canvas_size[0])+overlap[0], len(canvas[0])-1), min(((y+1)*canvas_size[1])+overlap[1], len(canvas)-1)]
            ]
            wave = wave_function(copy_canvas(copy.deepcopy(canvas), overlap_bounds), key, tries, iterations)
            if wave:
                for i in wave:
                    progress.append(paste_canvas([copy.deepcopy(canvas), crop_canvas(copy.deepcopy(i), [[0, 0],overlap])], overlap_bounds[0]))
                canvas = copy.deepcopy(progress[-1])
            else:
                return(False)
    wave = wave_function(copy.deepcopy(canvas), key, tries, iterations)
    if wave:
        progress += wave
    else:
        return(False)
    return(progress)
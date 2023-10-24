from main import *
import time
import json
import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

with open("map.json", "r", errors="ignore", encoding="utf-8") as jsonfile:
    key = json.load(jsonfile)

# with open("lines.json", "r", errors="ignore", encoding="utf-8") as jsonfile:
#     key = json.load(jsonfile)

tic = time.time()

y = 30
x = 60
canvas = [[list(key) for j in range(x)]for i in range(y)]
wave = wave_function_checker(canvas, key, canvas_size=[5, 5], overlap=[1, 1])
if wave:
    for i in wave:
        print("\n".join(["".join([(" "+str(hex(len(x))[-1] if len(x) < 16 else " N") if len(x) != 1 else x[0]) for x in y]) for y in i[::-1]]))
        time.sleep(1/60)
        clear_screen()
    print("\n".join(["".join([(str(len(x)) if len(x) != 1 else x[0]) for x in y]) for y in wave[-1][::-1]]))
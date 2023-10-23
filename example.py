from main import *
import time
import json

with open("key.json", "r", errors="ignore", encoding="utf-8") as jsonfile:
    key = json.load(jsonfile)

y = 10
x = 30
canvas = [[[" "]]*x] + [[[" "]] + [list(key) for j in range(x-2)] + [[" "]] for i in range(y)] + [[[" "]]*x]
wave = wave_function_checker(canvas, key)
if wave:
    for i in wave:
        print("\n".join(["".join([(str(len(x)) if len(x) != 1 else x[0]) for x in y]) for y in i[::-1]]))
        time.sleep(1/24)
        clear_screen()
    print("\n".join(["".join([(str(len(x)) if len(x) != 1 else x[0]) for x in y]) for y in wave[-1][::-1]]))
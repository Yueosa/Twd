# 生成世界的散算法
import random as rd
import math

def calculate_probability(input_num: float, k: float = 2) -> float:
    if (input_num > 50):
        return 1.0

    probability = ((input_num - 35) / (50 - 35)) ** k
    return probability

def should_return_false(input_num: float) -> bool:
    probability = calculate_probability(input_num)

    random_val = rd.random()
    return random_val >= probability

def random_the_num(start_x: int, start_y: int) -> tuple[int, int]:
    if (rd.random() <= 0.60):
        x_offset = rd.choice([-1, 0, 1])
        y_offset = rd.choice([-1, 0, 1])
    else:
        x_offset = rd.randint(10, 99)
        y_offset = rd.randint(10, 99)

    start_x = (start_x + x_offset) % 100
    start_y = (start_y + y_offset) % 100

    return start_x, start_y

def theterrain(soil: int, default_soil: int = 100):
    max_soil = default_soil - soil
    terrain_dict = {}
    first_num = 10
    last_num = 10
    rev = 0
    rev_top = 0
    rev_bottom = 0
    go_top = False
    go_bottom = False
    for i in range(4200):
        first_num = last_num
        if go_bottom:
            jump_num = rd.randint(-2, 0)
            rev_bottom += 1
            if rev_bottom % 50 == 0:
                go_bottom = False
        elif go_top:
            jump_num = rd.randint(0, 2)
            rev_top += 1
            if rev_top % 10 == 0:
                go_top = False
        else:
            jump_num = rd.randint(-2,2)
        last_num = first_num + jump_num
        if last_num <= 0:
            rev += 1
            if rev % 20 == 0:
                go_top = True
        if last_num >= 100:
            go_bottom = True
        terrain_dict[i] = last_num
    return terrain_dict

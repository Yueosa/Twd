# 生成世界的散算法
import random as rd


def calculate_probability(input_num: float, k: float = 2) -> float:
    if input_num > 50:
        return 1.0
    
    probability = ((input_num - 35) / (50 - 35)) ** k
    return probability

def should_return_false(input_num: float) -> bool:
    probability = calculate_probability(input_num)
    
    random_val = rd.random()
    return random_val >= probability

def random_the_num(start_x: int, start_y: int) -> tuple[int, int]:
    if rd.random() <= 0.60:
        x_offset = rd.choice([-1, 0, 1])
        y_offset = rd.choice([-1, 0, 1])
    else:
        x_offset = rd.randint(10, 99)
        y_offset = rd.randint(10, 99)

    start_x = (start_x + x_offset) % 100
    start_y = (start_y + y_offset) % 100

    return start_x, start_y

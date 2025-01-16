# 生成世界的散算法
import random as rd


def calculate_probability(input_num: float, k: float = 2) -> float:
    if input_num > 50:
        return 1.0
    
    probability = ((input_num - 40) / (50 - 40)) ** k
    return probability

def should_return_false(input_num: float) -> bool:
    probability = calculate_probability(input_num)
    
    random_val = rd.random()
    return random_val >= probability

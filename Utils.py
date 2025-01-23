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

def theterrain(soil: int, default_soil: int = 100, before: int = 10, after: int = 10):
    max_soil = default_soil - soil
    terrain_dict = {}
    tendency = 0
    
    for i in range(4200):
        if after >= max_soil:
            tendency = -0.2
        elif after <= 0:
            tendency = 0.2
        else:
            tendency = tendency * 0.8
        
        base_change = rd.randint(-2, 2)
        trend_influence = rd.random() * tendency
        height_change = int(base_change + trend_influence)
        
        after = max(0, min(max_soil, after + height_change))
        terrain_dict[i] = after
        
    terrain_dict = smooth(terrain_dict)
    return terrain_dict

def smooth(terrain: dict, iterations: int = 3) -> dict:
    # 第一阶段：基础平滑
    for _ in range(iterations):
        new_terrain = terrain.copy()
        for i in range(1, len(terrain) - 1):
            # 使用移动平均进行平滑
            new_terrain[i] = (terrain[i-1] + terrain[i] * 2 + terrain[i+1]) / 4
        terrain = new_terrain

    # 第二阶段：细分平滑
    refined_terrain = {}
    index = 0
    
    for i in range(len(terrain) - 1):
        current = terrain[i]
        next_val = terrain[i + 1]
        
        # 记录原始点
        refined_terrain[index] = current
        index += 1
        
        # 在两点之间插入中间点
        if abs(current - next_val) > 3:  # 只在高度差较大时插值
            mid_point = (current + next_val) / 2
            # 添加一些随机扰动
            mid_point += rd.uniform(-0.5, 0.5)
            refined_terrain[index] = mid_point
            index += 1
    
    # 添加最后一个点
    refined_terrain[index] = terrain[len(terrain) - 1]
    
    # 第三阶段：最终平滑
    final_terrain = {}
    keys = sorted(refined_terrain.keys())
    
    for i in range(len(keys)):
        key = keys[i]
        if i == 0 or i == len(keys) - 1:
            final_terrain[key] = refined_terrain[key]
            continue
            
        # 使用加权平均进行最终平滑
        prev_val = refined_terrain[keys[i-1]]
        curr_val = refined_terrain[key]
        next_val = refined_terrain[keys[i+1]]
        
        smoothed_val = (prev_val + 2 * curr_val + next_val) / 4
        final_terrain[key] = int(smoothed_val)  # 转换为整数
    
    return final_terrain
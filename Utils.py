# 生成世界的散算法
import random as rd
import math

def Utils_calculate_probability(input_num: float, k: float = 2) -> float:
    """概率计算函数
    原理: 使用幂函数计算概率,  当输入值超过阈值时返回最大概率
    参数: 
        input_num: 输入数值
        k: 幂指数,  控制概率增长的陡峭程度
    返回: 
        概率值(0.0-1.0)
    计算公式: ((x-35)/(50-35))^k
    示例: 
        输入45 -> 返回 ((45-35)/(50-35))^2 ≈ 0.64
        输入>50 -> 返回 1.0
    """
    if (input_num > 50):
        return 1.0

    probability = ((input_num - 35) / (50 - 35)) ** k
    return probability

def Utils_should_return_false(input_num: float) -> bool:
    """概率判定函数
    原理: 根据计算的概率值与随机值比较,  决定是否返回False
    参数: 
        input_num: 输入数值,  用于计算概率
    返回: 
        True: 随机值大于等于计算概率
        False: 随机值小于计算概率
    使用场景: 
        用于各类概率性事件的判定
        概率越高,  返回False的可能性越小
    """
    probability = Utils_calculate_probability(input_num)

    random_val = rd.random()
    return random_val >= probability

def Utils_random_the_num(start_x: int, start_y: int) -> tuple[int, int]:
    """随机坐标生成函数
    原理: 根据概率生成不同范围的偏移量,  实现局部或远距离跳转
    参数: 
        start_x, start_y: 起始坐标
    返回: 
        (新x坐标, 新y坐标)
    特点: 
        60%概率: 小范围移动 (-1,0,1)
        40%概率: 大范围跳转 (10-99)
    坐标系统: 
        使用模100运算确保坐标在0-99范围内循环
    """
    if (rd.random() <= 0.60):
        x_offset = rd.choice([-1, 0, 1])
        y_offset = rd.choice([-1, 0, 1])
    else:
        x_offset = rd.randint(10, 99)
        y_offset = rd.randint(10, 99)

    start_x = (start_x + x_offset) % 100
    start_y = (start_y + y_offset) % 100

    return start_x, start_y

def OraclesTerrain_diffusion_dot(matrix: list, type: str) -> list:
    """扩散点生成函数
    原理: 通过随机游走算法在矩阵中生成扩散点
    参数: 
        matrix: 输入矩阵
        type: 扩散类型('Cave'或'UnderGround')
    特点: 
        - 最大迭代10000次
        - 目标点数5000个
        - 使用随机游走算法确定点位置
        - 根据type类型进行不同的点位转换
    返回: 
        处理后的矩阵
    """
    max_iterations = 10000; target_points = 5000; points_placed = 0; x = -1; y = -1
    
    for _ in range(max_iterations):
        if points_placed >= target_points:
            break
        
        if x == -1 and y == -1:
            x = rd.randint(0, 99);  y = rd.randint(0, 99)

        x, y = Utils_random_the_num(x, y)

        if matrix[x][y] == 4 and type == 'Cave':
            matrix[x][y] = 3; points_placed += 1
        elif matrix[x][y] == 3 and  type == 'UnderGround':
            matrix[x][y] = 4; points_placed += 1
        
        if Utils_should_return_false((points_placed / max_iterations) * 100):
            break
            
    return matrix

def OraclesTerrain_matrix_insert(world: list, new_matrix: list, xt: int, xp: int, yt: int, yp: int, type :str) -> list:
    """矩阵插入函数
    原理: 将新矩阵插入到世界矩阵的指定位置
    参数: 
        world: 世界矩阵
        new_matrix: 待插入的新矩阵
        xt, xp: x轴起始和终止位置
        yt, yp: y轴起始和终止位置
        type: 插入类型('Cave'或'UnderGround')
    特点: 
        - Cave类型在y+420位置插入
        - UnderGround类型在y+300位置插入
    返回: 
        更新后的世界矩阵
    """
    if type == 'Cave':
        for i in range(yt, yp):
            for j in range(xt, xp):
                world[420 +i][j] = new_matrix[i - yt][j - xt]
    elif type == 'UnderGround':
        for i in range(yt, yp):
            for j in range(xt, xp):
                world[300 +i][j] = new_matrix[i - yt][j - xt]
    
    return world

def OraclesTerrain_the_terrain(soil: int, default_soil: int = 100, before: int = 10, after: int = 10, tendency: int = 0.2, rdterrain: int = 2):
    """地形生成函数
    原理: 通过tendency(趋势)控制地形生成方向,  结合随机值生成自然地形
    参数: 
        soil: 土壤基准值
        default_soil: 默认最大高度(100)
        max_soil: 实际最大可用高度(default_soil - soil)
        before: 迭代前的高度值
        after: 迭代后的高度值
        tendency: 修正系数,  越大对方向的修正力度越强
        rdterrain: 变化基本量,  越大变化越明显
    """
    max_soil = default_soil - soil
    terrain_dict = {}
    
    for i in range(4200):
        if after >= max_soil:
            tendency = -tendency
        elif after <= 0:
            tendency = tendency
        else:
            tendency = tendency * 0.8
        
        base_change = rd.randint(-rdterrain, rdterrain)
        trend_influence = rd.random() * tendency
        height_change = int(base_change + trend_influence)
        
        after = max(0, min(max_soil, after + height_change))
        terrain_dict[i] = after
        
    terrain_dict = Utils_terrain_smooth(terrain_dict)
    return terrain_dict

def Utils_terrain_smooth(terrain: dict, iterations: int = 3) -> dict:
    """地形平滑处理函数
    参数: 
        iterations: 细分程度,  越高细分次数越多,  地形越平滑
    采用三阶段平滑算法: 
    1. 基础平滑: 使用移动平均消除极端值
    2. 细分平滑: 处理大落差区域,  插入过渡点
    3. 最终平滑: 对细分后的地形再次平滑处理
    """
    # 第一阶段: 基础平滑
    # 原理: 使用移动加权平均算法 (前点 + 当前点×2 + 后点) / 4
    # 例如: 原始数据[10,15,8,12] -> 第二个点处理后 = (10 + 15×2 + 8) / 4 = 12
    for _ in range(iterations):
        new_terrain = terrain.copy()
        for i in range(1, len(terrain) - 1):
            new_terrain[i] = (terrain[i-1] + terrain[i] * 2 + terrain[i+1]) / 4
        terrain = new_terrain

    # 第二阶段: 细分平滑
    # 原理: 检测大落差(>3)位置,  插入中间过渡点
    # 例如: [10,20](差值10) -> [10, 15±随机值, 20]
    refined_terrain = {}
    index = 0
    
    for i in range(len(terrain) - 1):
        current = terrain[i]
        next_val = terrain[i + 1]
        
        refined_terrain[index] = current
        index += 1
        
        if abs(current - next_val) > 3:
            mid_point = (current + next_val) / 2
            mid_point += rd.uniform(-0.5, 0.5)
            refined_terrain[index] = mid_point
            index += 1
    
    refined_terrain[index] = terrain[len(terrain) - 1]
    
    # 第三阶段: 最终平滑
    # 原理: 对细分后的地形再次应用加权平均,  使过渡更自然
    final_terrain = {}
    keys = sorted(refined_terrain.keys())
    
    for i in range(len(keys)):
        key = keys[i]
        if i == 0 or i == len(keys) - 1:
            final_terrain[key] = refined_terrain[key]
            continue
            
        prev_val = refined_terrain[keys[i-1]]
        curr_val = refined_terrain[key]
        next_val = refined_terrain[keys[i+1]]
        
        smoothed_val = (prev_val + 2 * curr_val + next_val) / 4
        final_terrain[key] = int(smoothed_val)
        # 处理效果示意: 
    # 原始地形:     /\/\/\    (锯齿状)
    # 基础平滑:     /˜/˜/\    (减少极端值)
    # 细分后:       /~~/~~\   (增加过渡点)
    # 最终平滑:     ~~~~~~    (自然过渡)
    return final_terrain

def OraclesDunes_soil_to_dunes(world: list, center: int, maxlength: int, maxwidth: int):
    """沙丘生成函数
    参数: 
        world: 世界矩阵
        center: 沙丘中心位置
        maxlength: 沙丘最大长度,  越大生成的沙丘越宽,  默认50
        maxwidth: 沙丘最大高度,  越大生成的沙丘越高,  默认30
    功能: 将指定区域的土壤(3)转换为沙丘(5)
    """
    length = rd.randint((maxlength - maxwidth), maxlength)
    radius = length // 2
    left = center - radius
    right = center + radius

    top = float('inf')
    for x in range(left, right):
        for y in range(len(world)):
            if world[y][x] == 3:
                if y < top:
                    top = y
                break
    
    if top == float('inf'):
        return
    
    bottom = top + maxwidth
    if bottom >= len(world):
        bottom = len(world) - 1

    print(f"沙丘区域: x=[{left}, {right})-(", right - left, "), 高度范围: {top}~{bottom}-(", bottom - top, ")")
    
    world = Utils_create_dune_shape(world, left, right, top, bottom)
    world = Utils_dunes_smooth(world, left, right, top, bottom)

    return world

def Utils_create_dune_shape(world: list, left: int, right: int, top: int, bottom: int, 
                            wave_segments: int = 8, min_height_factor: float = 0.3, 
                            max_height_factor: float = 1.0, noise_range: float = 2.0):
    """沙丘形状生成函数
    参数: 
        world: 世界矩阵
        left, right: 沙丘横向范围
        top, bottom: 沙丘纵向范围
        wave_segments: 波形分段数,  越大沙丘轮廓越复杂,  默认8
        min_height_factor: 最小高度因子,  控制沙丘最低点,  默认0.3
        max_height_factor: 最大高度因子,  控制沙丘最高点,  默认1.0
        noise_range: 噪声范围,  越大沙丘表面越不规则,  默认2.0
    功能: 生成自然的沙丘波浪形状
    """
    width = right - left
    height = bottom - top
    
    wave_points = []
    segment_size = width // wave_segments
    current_height = height
    
    for i in range(wave_segments + 1):
        if i == 0 or i == wave_segments:
            point_height = height * min_height_factor
        else:
            random_factor = rd.uniform(min_height_factor * 2, max_height_factor)
            point_height = height * random_factor
        wave_points.append(point_height)

    for x in range(left, right):
        segment_index = int((x - left) / segment_size)
        if segment_index >= wave_segments:
            segment_index = wave_segments - 1
            
        segment_progress = ((x - left) % segment_size) / segment_size
        
        height1 = wave_points[segment_index]
        height2 = wave_points[segment_index + 1]
        
        current_height = Utils_cosine_interpolate(height1, height2, segment_progress)
        
        current_height += rd.uniform(-noise_range, noise_range)
        
        current_height = max(min(current_height, height), height * min_height_factor)
        
        for y in range(top, min(top + int(current_height), bottom)):
            if world[y][x] == 3:
                world[y][x] = 5
    
    return world

def Utils_cosine_interpolate(a: float, b: float, x: float) -> float:
    """余弦插值函数
    参数: 
        a: 起始值
        b: 结束值
        x: 插值位置(0-1)
    返回: 在a和b之间进行平滑插值的结果
    功能: 使用余弦函数产生平滑的过渡效果
    """
    ft = x * math.pi
    f = (1 - math.cos(ft)) * 0.5
    return a * (1 - f) + b * f

def Utils_dunes_smooth(world: list, left: int, right: int, bottom: int, top: int, 
                        smooth_radius: int = 2, sand_threshold: float = 0.7):
    """沙丘平滑处理函数
    参数: 
        world: 世界矩阵
        left, right: 处理区域横向范围
        bottom, top: 处理区域纵向范围
        smooth_radius: 平滑半径,  越大平滑效果越明显,  默认2
        sand_threshold: 转换阈值,  控制土壤与沙子转换的难度,  默认0.7
    功能: 平滑沙丘边缘,  使其看起来更自然
    """
    temp_world = [row[:] for row in world]
    
    for x in range(left - smooth_radius, right + smooth_radius):
        for y in range(bottom - smooth_radius, top + smooth_radius):
            if x < 0 or x >= len(world[0]) or y < 0 or y >= len(world):
                continue
            
            neighbors = []
            for dx in range(-smooth_radius, smooth_radius + 1):
                for dy in range(-smooth_radius, smooth_radius + 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < len(world[0]) and 0 <= ny < len(world):
                        neighbors.append(world[ny][nx])
            
            sand_count = neighbors.count(5)
            soil_count = neighbors.count(3)
            total = len(neighbors)
            
            if world[y][x] == 5:
                if soil_count / total > sand_threshold:
                    temp_world[y][x] = 3
            elif world[y][x] == 3:
                if sand_count / total > sand_threshold:
                    temp_world[y][x] = 5
    
    for x in range(left - smooth_radius, right + smooth_radius):
        for y in range(bottom - smooth_radius, top + smooth_radius):
            if 0 <= x < len(world[0]) and 0 <= y < len(world):
                world[y][x] = temp_world[y][x]

    return world

def Utils_create_oceansand_shape(world: list, left: int, right: int, top: int, bottom: int, is_left_side: bool = True):
    """海岸沙地形状生成函数
    参数:
        world: 世界矩阵
        left, right: 区域横向范围
        top, bottom: 区域纵向范围
        is_left_side: 是否为左侧区域(True生成弧形/形状，False生成弧形\形状)
    功能: 生成弧形的海岸沙地形状
    """
    width = right - left
    height = bottom - top
    
    # 计算控制点
    if is_left_side:
        # 左侧弧形: |__/
        p0 = (left, bottom)          # 起点
        p1 = (left + width * 0.6, bottom)  # 控制点：向右偏移60%，保持底部高度
        p2 = (right, top)           # 终点
    else:
        # 右侧弧形: \__|
        p0 = (left, top)            # 起点
        p1 = (right - width * 0.6, bottom)  # 控制点：向左偏移60%，底部
        p2 = (right, bottom)         # 终点

    # 遍历每一列
    for x in range(left, right):
        t = (x - left) / width
        
        # 使用二次贝塞尔曲线计算y坐标
        y_curve = int((1 - t) * (1 - t) * p0[1] + 
                     2 * (1 - t) * t * p1[1] + 
                     t * t * p2[1])
        
        # 添加随机扰动
        noise = rd.randint(-2, 2)
        y_curve += noise
        y_curve = max(top, min(bottom, y_curve))
        
        # 填充沙子
        if is_left_side:
            # 左侧：从顶部到曲线填充沙子
            for y in range(top, y_curve):
                if y < len(world) and world[y][x] == 3:
                    world[y][x] = 5
        else:
            # 右侧：从曲线到底部填充沙子
            for y in range(top, y_curve + 1):
                if y < len(world) and world[y][x] == 3:
                    world[y][x] = 5
    
    return world

def OraclesOceanSand_soil_to_dunes(world: list, length: int, width: int):
    """海洋沙生成函数
    参数:
        world: 世界矩阵
        length: 左侧区域的长度
        width: 生成区域宽度
    返回:
        处理后的世界矩阵
    """
    # 处理左侧区域 (0 to length)
    left_start = 0
    left_end = length
    top = float('inf')

    # 在x=length处寻找最高的土壤方块
    check_x = length - 1  # 因为索引从0开始，所以要减1
    for y in range(len(world)):
        if world[y][check_x] == 3:
            top = y
            break
    
    if top != float('inf'):
        bottom = min(top + width, len(world) - 1)
        print(f"海洋沙区域1: x=[{left_start}, {left_end})-(", left_end - left_start, "), 高度范围: {top}~{bottom}-(", bottom - top, ")")
        world = Utils_create_oceansand_shape(world, left_start, left_end, top, bottom, True)
        world = Utils_dunes_smooth(world, left_start, left_end, bottom, top)
        for x in range(left_start, left_end):
            for y in range(0, top):
                world[y][x] = 1

    # 处理右侧区域 (4200-length to 4200)
    right_start = 4200 - length
    right_end = 4200
    top = float('inf')

    # 在x=(4200-length)处寻找最高的土壤方块
    check_x = right_start  # 直接使用起始位置
    for y in range(len(world)):
        if world[y][check_x] == 3:
            top = y
            break
    
    if top != float('inf'):
        bottom = min(top + width, len(world) - 1)
        print(f"海洋沙区域2: x=[{right_start}, {right_end})-(", right_end - right_start, "), 高度范围: {top}~{bottom}-(", bottom - top, ")")
        world = Utils_create_oceansand_shape(world, right_start, right_end, top, bottom, False)
        world = Utils_dunes_smooth(world, right_start, right_end, bottom, top)
        for x in range(right_start, right_end):
            for y in range(0, top):
                world[y][x] = 1

    return world

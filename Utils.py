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

'''
import math
import random

# 随机生成噪声函数
def random_noise(x, y, seed=42):
    random.seed(x + y * 57 + seed)  # 基于x和y生成一个伪随机数
    return random.uniform(-1, 1)  # 返回[-1, 1]之间的浮动值

# 插值函数：线性插值（lerp）
def lerp(a, b, t):
    return a + t * (b - a)

# 插值函数：平滑插值（Cosine Interpolation）
def smoothstep(t):
    return t * t * (3 - 2 * t)

# 2D噪声生成函数
def perlin_noise(x, y, seed=42, scale=100.0):
    # 将输入的坐标缩放到适合噪声生成的范围
    x_scaled = x / scale
    y_scaled = y / scale

    # 计算格点的整数坐标
    x0 = int(x_scaled)
    y0 = int(y_scaled)
    x1 = x0 + 1
    y1 = y0 + 1

    # 获取四个角落的随机噪声值
    dot00 = random_noise(x0, y0, seed)
    dot10 = random_noise(x1, y0, seed)
    dot01 = random_noise(x0, y1, seed)
    dot11 = random_noise(x1, y1, seed)

    # 计算插值系数
    sx = x_scaled - x0
    sy = y_scaled - y0

    # 插值：通过lerp方法计算四个角的影响
    nx0 = lerp(dot00, dot10, smoothstep(sx))
    nx1 = lerp(dot01, dot11, smoothstep(sx))
    nxy = lerp(nx0, nx1, smoothstep(sy))

    return nxy

# 生成世界地形
def generate_world(width, height, scale=100.0, max_height=100, seed=42):
    world = []

    for y in range(height):
        row = []
        for x in range(width):
            # 生成每个点的噪声值
            noise_value = perlin_noise(x, y, seed, scale)

            # 将噪声值映射到0到30之间，并去掉低于30的部分（平原区域填充）
            if noise_value < 0:
                height_value = 0
            else:
                height_value = int((noise_value + 1) * 0.5 * 30)  # 映射到0到30之间

            # 在平原区域内加入小幅度的起伏
            if height_value < 30:
                # 在平原区间(0-30)内加入随机小幅度的波动
                height_value += int(random_noise(x, y) * 5)  # 这里加入小幅度的波动，-5到5之间

            if height_value > 30:
                height_value += int((noise_value + 1) * 0.5 * 70)  # 30到100之间的随机生成

            # 根据高度值划分地形类型
            if height_value < 30:
                terrain = "平原"  # 0到30为平原（带有小幅度起伏）
            elif height_value < 60:
                terrain = "高原"  # 高原，30到60
            elif height_value < 70:
                terrain = "戈壁"  # 戈壁，60到70
            elif height_value < 85:
                terrain = "悬崖"  # 悬崖，70到85
            else:
                terrain = "山脉"  # 山脉，85到100

            row.append((height_value, terrain))
        world.append(row)

    return world

# 显示部分生成结果
world = generate_world(100, 100, scale=80.0, max_height=100)

# 打印一部分结果
for row in world[:10]:  # 只打印前10行
    print(row[:10])  # 只打印前10列
'''
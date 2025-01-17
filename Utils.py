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

def lerp(a: float, b: float, x: float) -> float:
    "线性插值"
    return a + x * (b - a)

def fade(t: float) -> float:
    "缓动函数"
    return t * t * t * (t * (t * 6 - 15) + 10)

def gradient(hash: int, x: float, y: float) -> float:
    "计算梯度"
    h = hash & 15
    grad = 1 + (h & 7)  # 1, 2, 3, 4, 5, 6, 7, 8
    if (h & 8):
        grad = -grad  # -1, -2, -3, -4, -5, -6, -7, -8
    return grad * x + grad * y  # 计算梯度向量和位置向量的点积

class PerlinNoise:
    """柏林噪声生成器
    
    调参说明：
    - seed: 改变种子值会生成完全不同的地形，但相同的种子会生成相同的地形
    - 在noise()方法中，改变x的系数可以调整地形的"压缩"程度：
      * 值越大，地形起伏越密集
      * 值越小，地形起伏越舒缓
    """
    def __init__(self, seed=None):
        self.p = list(range(256))
        if (seed):
            rd.seed(seed)
        rd.shuffle(self.p)
        self.p += self.p  # 复制一遍，方便索引

    def noise(self, x: float, y: float) -> float:
        "生成2D柏林噪声"
        # 确定坐标所在的方格
        X = int(math.floor(x)) & 255
        Y = int(math.floor(y)) & 255

        # 计算相对坐标
        x -= math.floor(x)
        y -= math.floor(y)

        # 计算缓动曲线
        u = fade(x)
        v = fade(y)

        # 计算四个角的哈希值
        A = self.p[X] + Y
        B = self.p[X + 1] + Y

        # 计算四个角的贡献并插值
        return lerp(
            lerp(gradient(self.p[A], x, y),
                gradient(self.p[B], x - 1, y),
                u),
            lerp(gradient(self.p[A + 1], x, y - 1),
                gradient(self.p[B + 1], x - 1, y - 1),
                u),
            v)

def theterrain(
    soil: int,
    # 主地形参数
    main_scale: float = 0.01,     # 主地形缩放比例，越大地形越密集，越小地形越舒缓
    main_weight: float = 1.0,     # 主地形权重，越大主地形特征越明显
    # 细节层参数
    detail1_scale: float = 0.02,  # 第一细节层缩放，控制中等尺度起伏密度
    detail1_weight: float = 0.5,  # 第一细节层权重，越大中等尺度细节越明显
    detail2_scale: float = 0.04,  # 第二细节层缩放，控制小尺度起伏密度
    detail2_weight: float = 0.25, # 第二细节层权重，越大小尺度细节越明显
    # 高度控制参数
    base_height: int = 15,        # 基础高度限制，决定地形的整体起伏范围
    peak_factor: float = 0.3,     # 峰值系数，控制超出base_height的部分，越大peaks越明显
    smoothing: float = 0.5        # 平滑系数，控制地形过渡的平滑程度，越大越平滑
) -> dict:
    """使用2D柏林噪声生成地形，支持平滑的峰值过渡
    
    参数调节指南：
    1. 整体地形控制：
       - base_height: 基础高度限制(默认15)
         * 增大：整体起伏更大，山峰和峡谷更深
         * 减小：地形更加平缓
       - peak_factor: 峰值系数(默认0.3)
         * 增大(如0.5)：山峰更加突出，过渡更加陡峭
         * 减小(如0.1)：山峰更加圆润，过渡更加平缓
    
    2. 主地形参数：
       - main_scale: 主地形缩放(默认0.01)
         * 增大(如0.02)：主要起伏更密集，山峰间距更近
         * 减小(如0.005)：主要起伏更舒缓，山峰间距更远
       - main_weight: 主地形权重(默认1.0)
         * 增大：主地形特征更明显
         * 减小：主地形特征更模糊
    
    3. 细节控制：
       - detail1_scale/detail2_scale: 细节层缩放
         * 增大：对应尺度的细节更密集
         * 减小：对应尺度的细节更稀疏
       - detail1_weight/detail2_weight: 细节层权重
         * 增大：对应尺度的细节更明显
         * 减小：对应尺度的细节更柔和
    
    4. 平滑控制：
       - smoothing: 平滑系数(默认0.5)
         * 增大(如0.8)：地形过渡更加平滑
         * 减小(如0.2)：地形过渡更加锐利
    
    地形预设示例：
    1. 平缓丘陵：
       theterrain(soil, main_scale=0.008, detail1_scale=0.016, 
                 detail1_weight=0.3, detail2_weight=0.15,
                 base_height=10, peak_factor=0.2)
    
    2. 崎岖山地：
       theterrain(soil, main_scale=0.015, detail1_scale=0.03,
                 detail1_weight=0.6, detail2_weight=0.3,
                 base_height=20, peak_factor=0.4)
    
    3. 平原：
       theterrain(soil, main_scale=0.005, detail1_scale=0.01,
                 detail1_weight=0.2, detail2_weight=0.1,
                 base_height=8, peak_factor=0.15)
    """
    Tdict = {}
    noise = PerlinNoise(seed=rd.randint(0, 10000))
    max_height = min(base_height, 100-soil)

    for x in range(4200):
        # 生成基础高度
        height = noise.noise(x * main_scale, 0) * max_height * main_weight
        # 添加细节层
        height += noise.noise(x * detail1_scale, 0.2) * max_height * detail1_weight
        height += noise.noise(x * detail2_scale, 0.1) * max_height * detail2_weight
        
        # 处理超出基础高度的部分，使用平滑过渡
        if abs(height) > max_height:
            excess = abs(height) - max_height
            # 使用sigmoid类函数实现平滑过渡
            smooth_factor = 1 / (1 + math.exp(smoothing * excess / max_height))
            extra_height = excess * peak_factor * smooth_factor
            height = (max_height + extra_height) * (1 if height > 0 else -1)
        
        Tdict[x] = int(height)

    return Tdict

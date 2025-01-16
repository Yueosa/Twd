# 生成世界的算法集
import random as rd
from tqdm import tqdm


class Reset:
    "世界生成器, 初始化世界"
    def __init__(self) -> None:
        self.world, self.Reset_state = self.CreateWorld()

    @classmethod
    def Create(cls) -> tuple[list, bool]:
        instance = cls()
        return instance.world, instance.Reset_state

    def CreateWorld(self) -> tuple[list, bool]:
        print("正在初始化世界...")
        self.world = [[1 for i in range(4200)] for j in range(1200)]
        if len(self.world) == 1200 and len(self.world[0]) == 4200:
            Reset_state = True
        else:
            Reset_state = False
        return self.world, Reset_state

class Terrain:
    "地形生成器, 生成地形"
    def __init__(self, world: list, Rstate: bool) -> None:
        self.world = world
        self.Rstate = Rstate
        self.Terrain_state = False
        if self.Rstate:
            print("世界初始化成功，开始生成地形...")
            self.Start()
        else:
            print("世界初始化失败，跳过地形生成")

    @classmethod
    def Create(cls, world: list, Rstate: bool) -> tuple[list, bool]:
        instance = cls(world, Rstate)
        return instance.world, instance.Terrain_state

    def Start(self) -> None:
        self.Terrain_state = self.CaveStone()
        self.CaveSoil()

    def CaveStone(self) -> bool:
        try:
            print("开始生成洞穴层...")
            cave_world = self.world[420:]
            for i in range(len(cave_world)):
                for j in range(len(cave_world[i])):
                    cave_world[i][j] = 4
            
            self.world[420:] = cave_world
            
            for i in range(420, len(self.world)):
                if 1 in self.world[i]:
                    print("洞穴层生成失败")
                    return False
            print("洞穴层生成成功")
            return True
            
        except Exception as e:
            print(f"Cave generation failed: {e}")
            return False

    def CaveSoil(self) -> list:
        list_length = len(self.world[0]); list_width = len(self.world)
        x_num = -(list_length // -100); y_num = -(list_width // -100)
        matrix = [[4 for _ in range(100)] for _ in range(100)]
        print("正在向洞穴中添加泥土...")

        for i in tqdm(range(0, y_num)):
            for j in range(0, x_num):
                x_start = j * 100; x_stop = min((j + 1) * 100, list_length)
                y_start = i * 100; y_stop = min((i + 1) * 100, list_width)

                new_matrix = self.DiffusionDot(matrix)
                self.MatrixInsert(new_matrix, x_start, x_stop, y_start, y_stop)


    def DiffusionDot(self, list: list) -> list:
        Pnum = 0; input_num = 0
        while True:
            diffusion = should_return_false(input_num)
            if diffusion:
                x = rd.randint(0, 99); y = rd.randint(0, 99)
                if list[x][y] != 3:
                    list[x][y] = 3
                    Pnum += 1
                    input_num = (Pnum / 10000) * 100
            else:
                break
        return list

    def MatrixInsert(self, new_matrix: list, xt: int, xp: int, yt: int, yp: int) -> list:
        for i in range(yt, yp):
            for j in range(xt, xp):
                self.world[i][j] = new_matrix[i - yt][j - xt]



    def UnderGround(self, world :list) -> list:
        ...

    def CreateWorld(self, world :list, CaveWorld :list, UnderGroundWorld :list) -> tuple[list, bool]:
        ...


def calculate_probability(input_num: float, k: float = 2) -> float:
    if input_num < 35:
        return 0.0
    elif input_num > 50:
        return 1.0
    
    probability = ((input_num - 35) / (50 - 35)) ** k
    return probability

def should_return_false(input_num: float) -> bool:
    probability = calculate_probability(input_num)
    
    random_val = rd.random()
    return random_val >= probability

# 生成世界的算法集
import random as rd
from tqdm import tqdm
import time
import Utils


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
            print("世界初始化失败")

    @classmethod
    def Create(cls, world: list, Rstate: bool) -> tuple[list, bool]:
        instance = cls(world, Rstate)
        return instance.world, instance.Terrain_state

    def Start(self) -> None:
        self.Terrain_state = self.CaveStone()
        self.CaveSoil()
        self.UnderGroundSoil()
        self.UnderGroundStone()

    def CaveStone(self) -> bool:
        cave_world = self.world[420:]
        for i in tqdm(range(len(cave_world)), desc="正在向洞穴层填充石块..."):
            for j in range(len(cave_world[i])):
                cave_world[i][j] = 4
        
        self.world[420:] = cave_world
        
        for i in range(420, len(self.world)):
            if 1 in self.world[i]:
                print("洞穴层生成失败")
                return False
        return True

    def CaveSoil(self) -> list:
        cave_world = self.world[420:]
        list_length = len(cave_world[0]); list_width = len(cave_world)
        x_num = -(list_length // -100); y_num = -(list_width // -100)

        for i in tqdm(range(y_num), desc="正在向洞穴中添加土块..."):
            for j in range(x_num):
                matrix = [[4 for _ in range(100)] for _ in range(100)]
                x_start = j * 100; x_stop = min((j + 1) * 100, list_length)
                y_start = i * 100; y_stop = min((i + 1) * 100, list_width)
                
                new_matrix = self.DiffusionDot(matrix, 'Cave')
                self.MatrixInsert(new_matrix, x_start, x_stop, y_start, y_stop, 'Cave')

    def DiffusionDot(self, matrix: list, type: str) -> list:
        max_iterations = 10000; target_points = 5000; points_placed = 0
        
        for _ in range(max_iterations):
            if points_placed >= target_points:
                break
                
            x = rd.randint(0, 99);  y = rd.randint(0, 99)
            if matrix[x][y] == 4 and type == 'Cave':
                matrix[x][y] = 3; points_placed += 1
            elif matrix[x][y] == 3 and  type == 'UnderGround':
                matrix[x][y] = 4; points_placed += 1
            
            if Utils.should_return_false((points_placed / max_iterations) * 100):
                break
                
        return matrix

    def MatrixInsert(self, new_matrix: list, xt: int, xp: int, yt: int, yp: int, type :str) -> list:
        if type == 'Cave':
            for i in range(yt, yp):
                for j in range(xt, xp):
                    self.world[420 +i][j] = new_matrix[i - yt][j - xt]
        elif type == 'UnderGround':
            for i in range(yt, yp):
                for j in range(xt, xp):
                    self.world[300 +i][j] = new_matrix[i - yt][j - xt]


    def UnderGroundSoil(self) -> list:
        cave_world = self.world[300:420]
        for i in tqdm(range(len(cave_world)), desc="正在向地下层填充土块..."):
            for j in range(len(cave_world[i])):
                cave_world[i][j] = 3
        
        self.world[300:420] = cave_world
        return True

    def UnderGroundStone(self) -> list:
        cave_world = self.world[300:420]
        list_length = len(cave_world[0]); list_width = len(cave_world)
        x_num = -(list_length // -100); y_num = -(list_width // -100)

        for i in tqdm(range(y_num), desc="正在向地下层添加石块..."):
            for j in range(x_num):
                matrix = [[3 for _ in range(100)] for _ in range(100)]
                x_start = j * 100; x_stop = min((j + 1) * 100, list_length)
                y_start = i * 100; y_stop = min((i + 1) * 100, list_width)
                
                new_matrix = self.DiffusionDot(matrix, 'UnderGround')
                self.MatrixInsert(new_matrix, x_start, x_stop, y_start, y_stop, 'UnderGround')

# 生成世界的算法集
import random as rd
from tqdm import tqdm
import time
import Utils
import math


class Reset:
    "世界生成器, 初始化世界"
    def __init__(self) -> None:
        self.world, self.Reset_state = self.CreateWorld()

    @classmethod
    def Create(cls) -> tuple[list, bool]:
        instance = cls()
        return instance.world, instance.Reset_state

    "生成 4200 * 1200 大小的世界"
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
            print("世界初始化成功,  开始生成地形...")
            self.Start()
        else:
            print("世界初始化失败")

    @classmethod
    def Create(cls, world: list, Rstate: bool) -> tuple[list, bool]:
        instance = cls(world, Rstate)
        return instance.world, instance.Terrain_state

    "类方法启动函数"
    def Start(self) -> None:
        self.Terrain_state = self.CaveStone()
        self.CaveSoil()
        self.UnderGroundSoil()
        self.UnderGroundStone()
        self.GroundSoil()

    "向洞穴层填充石块"
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

    "向洞穴层填充土块"
    def CaveSoil(self) -> list:
        cave_world = self.world[420:]
        list_length = len(cave_world[0]); list_width = len(cave_world)
        x_num = -(list_length // -100); y_num = -(list_width // -100)

        for i in tqdm(range(y_num), desc="正在向洞穴中添加土块..."):
            for j in range(x_num):
                matrix = [[4 for _ in range(100)] for _ in range(100)]
                x_start = j * 100; x_stop = min((j + 1) * 100, list_length)
                y_start = i * 100; y_stop = min((i + 1) * 100, list_width)
                
                new_matrix = Utils.OraclesTerrain_diffusion_dot(matrix, 'Cave')
                self.world = Utils.OraclesTerrain_matrix_insert(self.world, new_matrix, x_start, x_stop, y_start, y_stop, 'Cave')

    "向地下层填充土块"
    def UnderGroundSoil(self) -> bool:
        cave_world = self.world[300:420]
        for i in tqdm(range(len(cave_world)), desc="正在向地下层填充土块..."):
            for j in range(len(cave_world[i])):
                cave_world[i][j] = 3
        
        self.world[300:420] = cave_world
        return True

    "向地下层填充石块"
    def UnderGroundStone(self) -> None:
        cave_world = self.world[300:420]
        list_length = len(cave_world[0]); list_width = len(cave_world)
        x_num = -(list_length // -100); y_num = -(list_width // -100)

        for i in tqdm(range(y_num), desc="正在向地下层添加石块..."):
            for j in range(x_num):
                matrix = [[3 for _ in range(100)] for _ in range(100)]
                x_start = j * 100; x_stop = min((j + 1) * 100, list_length)
                y_start = i * 100; y_stop = min((i + 1) * 100, list_width)
                
                new_matrix = Utils.OraclesTerrain_diffusion_dot(matrix, 'UnderGround')
                self.world = Utils.OraclesTerrain_matrix_insert(self.world, new_matrix, x_start, x_stop, y_start, y_stop, 'UnderGround')

    "生成地表土层"
    def GroundSoil(self) -> None:
        soil_thickness = rd.randint(10, 40)
        start_layer = 300 - soil_thickness
        end_layer = 300

        for i in tqdm(range(start_layer, end_layer), desc="正在生成地表土层..."):
            for j in range(4200):
                self.world[i][j] = 3
        
        self.GroundTerrain(soil_thickness)

    "生成地表地形"
    def GroundTerrain(self, soil: int) -> None:
        base_line = 300 - soil
        terrain_dict = Utils.OraclesTerrain_the_terrain(soil)
        
        max_height = max(terrain_dict.values())
        print(f"地形最大隆起高度: {max_height}, 基准线高度: {base_line}")
        
        for key, value in tqdm(terrain_dict.items(), desc='正在使世界变得凹凸...'):
            line = base_line - value
            for j in range(line, base_line):
                self.world[j][key] = 3

class Dunes:
    "沙丘生成器, 生成沙丘"
    def __init__(self, world: list) -> None:
        self.world = world
        self.Start()

    @classmethod
    def Create(cls, world: list) -> list:
        instance = cls(world)
        return instance.world

    "类方法启动函数"
    def Start(self):
        self.TheDunes()

    "控制生成沙丘的个数"
    def DunesNumber(self) -> int:
        return rd.randint(2, 3)

    "控制生成沙丘的范围"
    def SixPoints(self) -> tuple[int, int]:
        left = 4200 // 6
        right = 4200 - left
        return left, right

    "在地表生成沙丘"
    def TheDunes(self, spacing: int = 450, spacelist: list = [], duneslenth: int = 300, duneswidth: int = 80):
        ranum = self.DunesNumber()
        for _ in tqdm(range(ranum), desc='正在生成沙丘...'):
            left, right = self.SixPoints()
            while True:
                location = rd.randint(left + duneslenth, right - duneslenth)
                valid = True
                for existing in spacelist:
                    if abs(location - existing) < spacing:
                        valid = False
                        break
                if valid:
                    break
            spacelist.append(location)
            self.world = Utils.OraclesDunes_soil_to_dunes(self.world, location, duneslenth, duneswidth)

class OceanSand:
    "海洋沙生成器, 生成海洋沙"
    def __init__(self, world: list) -> None:
        self.world = world
        self.Start()

    @classmethod
    def Create(cls, world: list) -> list:
        instance = cls(world)
        return instance.world

    def Start(self):
        self.TheOceanSand()
        self.TheStuff()

    "生成海洋沙"
    def TheOceanSand(self, space: int = 12):
        length = 4200 // space
        self.world = Utils.OraclesOceanSand_soil_to_dunes(self.world, length, length // 3)

    "填充海洋沙高度"
    def TheStuff(self):
        pass

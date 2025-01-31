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
        self.GroundSoil()

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
        max_iterations = 10000; target_points = 5000; points_placed = 0; x = -1; y = -1
        
        for _ in range(max_iterations):
            if points_placed >= target_points:
                break
            
            if x == -1 and y == -1:
                x = rd.randint(0, 99);  y = rd.randint(0, 99)

            x, y = Utils.random_the_num(x, y)

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


    def UnderGroundSoil(self) -> bool:
        cave_world = self.world[300:420]
        for i in tqdm(range(len(cave_world)), desc="正在向地下层填充土块..."):
            for j in range(len(cave_world[i])):
                cave_world[i][j] = 3
        
        self.world[300:420] = cave_world
        return True

    def UnderGroundStone(self) -> None:
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

    def GroundSoil(self) -> None:
        soil_thickness = rd.randint(0, 30)
        start_layer = 300 - soil_thickness
        end_layer = 300

        for i in tqdm(range(start_layer, end_layer), desc="正在生成地表土层..."):
            for j in range(4200):
                self.world[i][j] = 3
        
        self.GroundTerrain(soil_thickness)

    def GroundTerrain(self, soil: int) -> None:
        base_line = 300 - soil
        terrain_dict = Utils.theterrain(soil)
        
        max_height = max(terrain_dict.values())
        print(f"地形最大隆起高度: {max_height}, 基准线高度: {base_line}")
        
        for key, value in tqdm(terrain_dict.items(), desc='正在使世界变得凹凸...'):
            line = base_line - value
            for j in range(line, base_line):
                self.world[j][key] = 3

class Dunes:
    def __init__(self, world: list) -> None:
        self.world = world
        self.Start()

    @classmethod
    def Create(cls, world: list) -> list:
        instance = cls(world)
        return instance.world

    def Start(self):
        self.TheDunes()

    def DunesNumber(self) -> int:
        return rd.randint(2, 3)

    def SixPoints(self) -> tuple[int, int]:
        left = 4200 // 6
        right = 4200 - left
        return left, right

    def TheDunes(self, spacing: int = 450, spacelist: list = [], duneslenth: int = 200, duneswidth: int = 60):
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
            self.soiltodunes(location, duneslenth, duneswidth)
    
    def soiltodunes(self, center: int, maxlength: int, maxwidth: int):
        length = rd.randint(maxlength - (maxwidth // 2), maxlength)
        radius = length // 2
        left = center - radius
        right = center + radius
        
        top = -1
        
        for x in range(left - 1, right + 1):
            for y in range(len(self.world)):
                if self.world[y][x] == 3:
                    if y > top:
                        top = y
                    break
        
        if top == -1:
            return
        
        bottom = top - maxwidth
        if bottom < 0:
            bottom = 0

        print(f"沙丘区域: x=[{left}, {right}), 高度范围: {bottom}~{top}")
        
        for i in range(bottom, top):
            for j in range(left, right):
                if self.world[i][j] == 3:
                    self.world[i][j] = 5

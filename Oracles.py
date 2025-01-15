# 生成世界的算法集
import random


class Reset:
    "世界生成器, 初始化世界"
    def __init__(self) -> None:
        self.world, self.Reset_state = self.CreateWorld()

    @classmethod
    def Create(cls):
        instance = cls()
        return instance.world, instance.Reset_state

    def CreateWorld(self) -> tuple[list, bool]:
        print("正在初始化世界...")
        self.world = [[8 for i in range(4200)] for j in range(1200)]
        if len(self.world) == 1200 and len(self.world[0]) == 4200:
            Reset_state = True
        else:
            Reset_state = False
        return self.world, Reset_state

class Terrain:
    "地形生成器, 生成地形"
    def __init__(self, world: list) -> None:
        self.world = world
        self.Cave()

    @classmethod
    def Create(cls, world: list):
        instance = cls(world)
        return instance.world

    def Cave(self) -> list:
        cave_world = self.world[1470:]
        for i in range(len(cave_world)):
            for j in range(len(cave_world[i])):
                cave_world[i][j] = 7

        x_list = random.choices(range(4201), k=425_0400)
        y_list = random.choices(range(2531), k=425_0400)

        range_num = int((len(cave_world) * 4200) * 0.4)

        for i in range(range_num):
            cave_world[y_list[i] % len(cave_world)][x_list[i] % 4200] = 3

        self.world[1470:] = cave_world


    def UnderGround(self, world :list) -> list:
        ...

    def CreateWorld(self, world :list, CaveWorld :list, UnderGroundWorld :list) -> tuple[list, bool]:
        ...
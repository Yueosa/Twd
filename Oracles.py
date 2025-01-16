# 生成世界的算法集


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
        self.world = [[7 for i in range(4200)] for j in range(1200)]
        if len(self.world) == 1200 and len(self.world[0]) == 4200:
            Reset_state = True
        else:
            Reset_state = False
        return self.world, Reset_state

class Terrain:
    "地形生成器, 生成地形"
    def __init__(self, world: list, state: bool) -> None:
        self.world = world
        self.state = state
        self.Terrain_state = False
        if self.state:
            self.Terrain_state = self.Cave()

    @classmethod
    def Create(cls, world: list, state: bool) -> tuple[list, bool]:
        instance = cls(world, state)
        return instance.world, instance.Terrain_state

    def Cave(self) -> bool:
        try:
            cave_world = self.world[1470:]
            for i in range(len(cave_world)):
                for j in range(len(cave_world[i])):
                        cave_world[i][j] = 4
            
            self.world[1470:] = cave_world
            
            for i in range(1470, len(self.world)):
                if 7 in self.world[i]:
                    return False
            return True
            
        except Exception as e:
            print(f"Cave generation failed: {e}")
            return False

    def Start(self, state: bool) -> None:
        ...

    def UnderGround(self, world :list) -> list:
        ...

    def CreateWorld(self, world :list, CaveWorld :list, UnderGroundWorld :list) -> tuple[list, bool]:
        ...

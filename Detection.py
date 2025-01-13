# 检测工具
class EnvironmentalTesting:
    """用于检测环境的工具包"""
    def __init__(self, block :list= None, world :list= None):
        self.block = block
        self.world = world

        self.world_length = 4200
        self.world_width = 1200
        self.strata = {1: 'Space', 2: 'Surface', 3: 'Underground', 4: 'Cave', 5: 'Hell'}

    def StrataTest(self, high :int) -> tuple[int, str]:
        """查询当前所在地层编号以及名字"""
        if high < 210:
            return self.strata[1].items()
            
        if high >= 210 and high < 1050:
            return self.strata[2].items()

        if high >= 1050 and high < 1470:
            return self.strata[3].items()

        if high >= 1470 and high < 4000:
            return self.strata[4].items()
            
        if high >= 4000:
            return self.strata[5].items()

    def VacancyTest(self, block :list) -> tuple[int, int]:
        """查询当前区块的占有率"""
        possession = 0
        vacancy = 0

        for i in block:
            for j in i:
                if j == 1:
                    vacancy += 1
                if j > 1:
                    possession += 1
        return possession, vacancy 

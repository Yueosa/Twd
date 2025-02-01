import sys
import os

# 添加父目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import Oracles
import Weaving

# 主程序
weave = Weaving.Weave()

# 初始化
Rworld, state = Oracles.Reset.Create()
weave.Save(Weaving.Save_image(weave, Rworld))

# 地形
Tworld, Rstate= Oracles.Terrain.Create(Rworld, state)
weave.Save(Weaving.Save_image(weave, Tworld))

# 沙丘
Dworld = Oracles.Dunes.Create(Tworld)
weave.Save(Weaving.Save_image(weave, Dworld))

# 海洋沙
Oworld = Oracles.OceanSand.Create(Dworld)
weave.Save(Weaving.Save_image(weave, Oworld))

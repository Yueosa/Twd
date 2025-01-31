import sys
import os

# 添加父目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import Oracles
import Weaving

# 主程序
Rworld, state = Oracles.Reset.Create()
Tworld, Rstate= Oracles.Terrain.Create(Rworld, state)
Dworld = Oracles.Dunes.Create(Tworld)

weave = Weaving.Weave()

weave.Save(Weaving.Save_image(weave, Dworld))

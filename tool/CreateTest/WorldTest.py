import sys
import os

# 添加父目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import Oracles
import Weaving

# 主程序
Rworld, state = Oracles.Reset.Create()
Tworld, Rstate= Oracles.Terrain.Create(Rworld, state)
print('正在生成洞穴...')

weave = Weaving.Weave()
print('正在生成世界...')

weave.Save(Weaving.Save_image(weave, Tworld))

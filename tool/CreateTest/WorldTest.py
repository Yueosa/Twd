import Oracles, Weaving


Rworld, state = Oracles.Reset.Create()
Tworld = Oracles.Terrain.Create(Rworld)
print('正在生成洞穴...')
print(Tworld)
weave = Weaving.Weave()
print('正在生成世界...')

weave.Save(Weaving.Save_path(weave), Weaving.Save_image(weave, Tworld))

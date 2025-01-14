# 项目说明
本项目用于自学 **算法** 和 **数据结构**
对原本游戏逻辑进行了简化处理，部分数值设置与真实情况有所偏差
在世界大小上选择了小世界的大小（4200*1200），目前所有代码仅基于这一个世界尺寸开发

# 世界层级

## **太空**
太空占用的空间是地表的 **$ \frac{1}{5} $**，全世界的 **$ \frac{1}{20}$**

太空层的高度为 ***[840, 1050]***，二维列表中为 ***[:210]***

## **地表**
地表从 ***0*** 高度开始，一直持续到太空

地表层的高度为 ***[0, 840]***，二维列表中为 ***[210:1050]***

## **地下**
地下层开始于 ***0*** 高度往下，占有整个世界高度的 ***10%***

地下层的高度为 ***[-420, 0]***，二维列表中为 ***world[1050:1470]***

## **洞穴**
洞穴层的环境比较复杂，他是地下到地狱中间部分的总称
在这个世界大小中：

洞穴层的高度为 ***[-4000, -420]***，二维列表中为 ***[1470:4000]***

## **地狱**
地狱层固定为 ***200*** 固定高度，不因为比例发生变化

地狱层的高度为 ***[-4200, -4000]***，二维列表为 ***world[4000:]***

# 世界生成
###### 参考BiliBili视频[探索泰拉瑞亚世界的奥秘！解析107个世界生成步骤！](https://www.bilibili.com/video/BV1FJcsecEt1?vd_source=af214977129a4a7d5b517650d65b0bfe)
###### 通过整理和简化后的世界生成步骤如下：
     1. 初始化（Reset）
     2. 地形（Terrain）
     3. 沙丘（Dunes）
     4. 海洋沙（OceanSand）
     5. 沙补丁（SandPatch）
     6. 隧道（Tunnel）
     7. 山洞（Cave）
     8. 土中石（StoneInDirt）
     9. 石中土（DirtInStone）
    10. 黏土（Clay）
    11. 小洞（SmallHole）
    12. 土层洞穴（DirtLayerCave）
    13. 石层洞穴（StoneLayerCave）
    14. 地表洞穴（SurfaceCave）
    15. 冰雪群系（SnowBiome）
    16. 丛林群系（JungleBiome）
    17. 沙漠群系（DesertBiome）
    18. 空岛（SkyIsland）
    19. 蘑菇群系（MushroomBiome）
    20. 大理石群系（MarbleBiome）
    21. 花岗岩群系（GraniteBiome）
    22. 淤泥（Silt）
    23. 泥沙（MudSand）
    24. 矿脉（OreVein）
    25. 蛛丝（Cobweb）
    26. 下界（UnderWorld）
    27. 邪恶化（Corruption）
    28. 湖（Lake）
    29. 地牢（Dungeon）
    30. 雪泥（Slush）
    31. 山体洞穴（MountainCave）
    32. 海滩（Beach）
    33. 重力沙（GravitySand）
    34. 海洋洞穴（OceanCave）
    35. 微光（Shimmer）
    36. 金字塔（Pyramid）
    37. 生命树（LifeTree）
    38. 湿润丛林（WetJungle）
    39. 丛林神庙（JungleTemple）
    40. 蜂巢（Beehive）
    41. 移除沙漠水（RemoveDesertWater）
    42. 绿洲（Oasis）
    43. 平滑世界（SmoothWorld）
    44. 瀑布（Waterfall）
    45. 埋藏宝箱（BuriedTreasureChest）
    46. 地表宝箱（SurfaceTreasureChest）
    47. 水下箱（UnderwaterChest）
    48. 蜘蛛洞（SpiderCave）
    49. 神庙丰富（TempleRiches）
    50. 丛林木（JungleWood）
    51. 空岛屋（SkyIslandHouse）
    52. 地表矿脉/石嵌块（SurfaceOreVein）
    53. 出生点（SpawnPoint）
    54. 发光蘑菇补丁（GlowingMushroomPatch）
    55. 蜂后（QueenBee）
    56. 平衡液体（BalanceLiquids）
    57. 仙人掌、棕榈树、珊瑚（CactusPalmCoral）
    58. 丛林蜥蜴祭坛（JungleLizardAltar）
    59. 微型生物群系（MicroBiome）
    60. 最终清理（FinalCleanup）
###### 更详细的信息请查阅 **resource/Create.md**
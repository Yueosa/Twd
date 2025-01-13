# 可视化
import cv2 as cv
import numpy as np
import os
import json
from tqdm import tqdm as tq


class World:
    """处理传入的世界(二维矩阵)"""
    def __init__(self, world):
        self.world = world


class Weave:
    """对矩阵地图进行可视化"""
    def Now_Path(self) -> str :
        """返回当前路径"""
        return os.path.dirname(os.path.abspath(__file__))

    def Save_Path(self, now_dir :str) -> str:
        """拼接Plain路径"""
        return os.path.join(now_dir, 'Plain')

    def Save_Name(self, path :str, filename :str) -> str:
        """拼接文件名"""
        return os.path.join(path, filename)

    def List_NumPy(self, world :list) -> np.ndarray:
        """生成NumPy矩阵"""
        return np.array(world)

    def Read_List(self, world :list) -> tuple[int, int]:
        """读取世界长宽"""
        return len(world[0]), len(world)

    def Read_Json(self) -> dict:
        """读取颜色配置"""
        with open('cornerstone/Prism_OfCreation.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    def Image(self, world_length :int,world_width :int, color_variety :int = 4) ->np.ndarray:
        """生成空地图"""
        return np.zeros((world_width, world_length, color_variety), dtype=np.uint8)

    def NumPy(self, matrix :np.ndarray, color :dict, image :np.ndarray, world_length :int, world_width :int) -> np.ndarray:
        """向空地图里填色"""
        for i in tq(range(world_width)):
            for j in range(world_length):
                image[i, j] = color[matrix[i, j]]
        return image

    def Save(self, path :str, image :np.ndarray, filename :str ='matrix.png') -> None:
        """保存地图为png"""
        save_path = self.Save_Name(path, filename)
        try:
            if cv.imwrite(save_path, image):
                print(f'successfully saved to {save_path}')
            else:
                raise ValueError(f"Save failed")
        except Exception as e:
            print(f"Error: {e}")


def NumPy_matrix(weave :Weave, world :list) -> np.ndarray:
    """集合函数: 生成NumPy矩阵"""
    return weave.List_NumPy(world)


def NumPy_image(weave :Weave, world :list) -> np.ndarray:
    """集合函数: 生成空地图"""
    return weave.Image(*Read_List(world))


def Save_path(weave :Weave) -> str:
    """集合函数: 生成保存路径"""
    return weave.Save_Path(weave.Now_Path())


def Save_image(weave :Weave, world :list) -> np.ndarray:
    """集合函数: 生成保存图片"""
    return weave.NumPy(NumPy_matrix(weave, world), weave.Read_Json(), NumPy_image(weave, world), *weave.Read_List(world))


if __name__=="__main__":
    weave = Weave()
    Save(Save_path(weave), Save_image(weave, world))

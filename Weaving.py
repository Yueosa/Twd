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
    def List_NumPy(self, world :list) -> np.ndarray:
        """生成NumPy矩阵"""
        return np.array(world)

    def Read_List(self, world :list) -> tuple[int, int]:
        """读取世界长宽
        返回: (length, width)，即(列数, 行数)
        """
        return len(world[0]), len(world)  # 返回列数和行数

    def Read_Json(self) -> dict:
        """读取颜色配置"""
        json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cornerstone', 'Prism_Of_Creation.json')
        with open(json_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def Image(self, world_length :int,world_width :int, color_variety :int = 4) ->np.ndarray:
        """根据实际世界尺寸生成空地图
        world_length: 世界列数
        world_width: 世界行数
        color_variety: 颜色通道数 (RGBA)
        """
        print(f"Creating image with dimensions: {world_width}x{world_length}")
        return np.zeros((world_width, world_length, color_variety), dtype=np.uint8)

    def NumPy(self, matrix :np.ndarray, color :dict, image :np.ndarray, world_length :int, world_width :int) -> np.ndarray:
        """向空地图里填色
        matrix: 包含数字的NumPy数组
        color: 颜色字典 (从Prism_Of_Creation.json读取)
        """
        for i in tq(range(world_width)):
            print('the i:', i)
            for j in range(world_length):
                print('the j:', j)
                block_id = str(int(matrix[i, j]))
                print('the block_id:', block_id)
                if block_id in color:
                    rgba = color[block_id]
                    bgra = [rgba[2], rgba[1], rgba[0], rgba[3]]
                    image[i, j] = bgra
                    print(f'Position ({i},{j}) - Block {block_id}: RGBA {color[block_id]} -> BGRA {bgra}')
                else:
                    image[i, j] = [0, 0, 0, 0]
                    print('error')
        return image

    def FileName(self) -> str:
        """生成递增的文件名"""
        if not os.path.exists('Plain'):
            os.makedirs('Plain')
            return 'matrix_0001.png'
        
        files = [f for f in os.listdir('Plain') if f.startswith('matrix_') and f.endswith('.png')]
        if not files:
            return 'matrix_0001.png'
        
        numbers = [int(f.split('_')[1].split('.')[0]) for f in files]
        next_number = max(numbers) + 1
        return f'matrix_{next_number:04d}.png'

    def Save(self, image :np.ndarray) -> None:
        """保存地图为png"""
        filename = self.FileName()
        save_path = os.path.join('Plain', filename)
        try:
            # OpenCV默认使用BGRA格式，所以不需要再转换
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
    return weave.Image(*weave.Read_List(world))


def Save_image(weave :Weave, world :list) -> np.ndarray:
    """集合函数: 生成保存图片"""
    return weave.NumPy(NumPy_matrix(weave, world), weave.Read_Json(), NumPy_image(weave, world), *weave.Read_List(world))


if __name__=="__main__":
    world = [
        [1, 2, 3, 4, 5, 6, 7, 8],
        [9, 10, 11, 12, 13, 14, 15, 16]
    ]
    weave = Weave()
    weave.Save(Save_image(weave, world))

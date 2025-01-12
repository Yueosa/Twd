# 可视化
import cv2 as cv
import numpy as np
import os
import json
from tqdm import tqdm as tq


class World:
    def __init__(self, world):
        self.world = world


class Weave:
    def Now_Path(self) -> str :
        return os.path.dirname(os.path.abspath(__file__))

    def Save_Path(self, now_dir :str) -> str:
        return os.path.join(now_dir, 'Plain')

    def Save_Name(self, path :str, filename :str) -> str:
        return os.path.join(path, filename)

    def List_NumPy(self, world :list) -> np.ndarray:
        return np.array(world)

    def Read_List(self, world :list) -> tuple[int, int]:
        return len(world[0]), len(world)

    def Read_Json(self) -> dict:
        with open('cornerstone/Prism_OfCreation.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    def Image(self, world_length :int,world_width :int, color_variety :int = 4) ->np.ndarray:
        return np.zeros((world_width, world_length, color_variety), dtype=np.uint8)

    def NumPy(self, matrix :np.ndarray, color :dict, image :np.ndarray, world_length :int, world_width :int) -> np.ndarray:
        for i in tq(range(world_width)):
            for j in range(world_length):
                image[i, j] = color[matrix[i, j]]
        return image

    def Save(self, path :str, image :np.ndarray, filename :str ='matrix.png') -> None:
        save_path = self.Save_Name(path, filename)
        try:
            if cv.imwrite(save_path, image):
                print(f'successfully saved to {save_path}')
            else:
                raise ValueError(f"Save failed")
        except Exception as e:
            print(f"Error: {e}")


def NumPy_matrix(weave :Weave, world :list) -> np.ndarray:
    return weave.List_NumPy(world)


def NumPy_image(weave :Weave, world :list) -> np.ndarray:
    return weave.Image(*Read_List(world))


def Save_path(weave :Weave) -> str:
    return weave.Save_Path(weave.Now_Path())


def Save_image(weave :Weave, world :list) -> np.ndarray:
    return weave.NumPy(NumPy_matrix(weave, world), weave.Read_Json(), NumPy_image(weave, world), *weave.Read_List(world))


if __name__=="__main__":
    weave = Weave()
    Save(Save_path(weave), Save_image(weave, world))

import json
import numpy as np
import cv2
import os

# 获取当前脚本的目录
script_dir = os.path.dirname(__file__)
# 构建Color_Lexicon.json的绝对路径
json_path = os.path.join(script_dir, '../../cornerstone/Color_Lexicon.json')

# 读取颜色数据
with open(json_path, 'r', encoding='utf-8') as file:
    color_data = json.load(file)
    print('load data:\n', color_data)

# 创建一个空白画布
height, width = 600, 600
image = np.zeros((height, width, 4), dtype=np.uint8)  # 使用4通道图像

# 计算每个方块的大小
num_colors = len(color_data)
cols = int(np.sqrt(num_colors))
rows = (num_colors + cols - 1) // cols  # 自动计算行数
block_size = min(height // rows, width // cols)  # 每个方块的大小

# 提取所有颜色的RGBA值，并将它们显示在画布上
for i, (key, value) in enumerate(color_data.items()):
    rgba = value['rgba']
    print('the rgba:\n', rgba)
    row = i // cols
    col = i % cols
    top_left = (col * block_size, row * block_size)
    bottom_right = ((col + 1) * block_size, (row + 1) * block_size)
    
    # 为每个颜色创建一个矩形
    image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]] = rgba

# 转换为BGR格式以便显示
image_bgr = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)

# 显示图像
cv2.imshow('Color Map', image_bgr)
cv2.waitKey(0)
cv2.destroyAllWindows()
# 这里的颜色显示似乎与MainPy分支的Weaving文件不同，关联文件：Cornerstone分支的Color_Lexicon.json、Prism_OfCreation

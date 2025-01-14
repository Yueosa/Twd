import os
import json


def read_list(file_path: str) -> list:
    """
    读取list.txt文件，将每一行都放到list里
    :param file_path: list.txt文件路径
    :return: 包含文件内容的列表
    """
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]


def add_to_list(lst: list, item: str) -> tuple[list, bool]:
    """
    尝试将输入添加到列表中，如果存在则返回False，否则返回True
    :param lst: 现有列表
    :param item: 要添加的项目
    :return: 更新后的列表和是否添加的标志
    """
    if item in lst:
        return lst, False
    lst.append(item)
    return lst, True


def save_list(file_path: str, lst: list) -> None:
    """
    将列表内容保存到list.txt文件中
    :param file_path: list.txt文件路径
    :param lst: 要保存的列表
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in lst:
            file.write(item + '\n')


def input_and_add(file_path: str) -> None:
    """
    获取用户输入并尝试添加到列表中，如果存在则提示并询问是否保存
    :param file_path: list.txt文件路径
    """
    lst = read_list(file_path)
    while True:
        item = input("Input: ")
        if item == "":
            choice = input("Save? (y/n): ")
            if choice.lower() == 'y':
                save_list(file_path, lst)
                print("Saved.")
                break
            else:
                print("Not saved.")
                break
        lst, added = add_to_list(lst, item)
        if added:
            print("Added!")
        else:
            print("Already exists!")
            choice = input("Save? (y/n): ")
            if choice.lower() == 'y':
                save_list(file_path, lst)
                print(f"Saved: {item}")
                break
            else:
                print("Not saved.")
                break


def add_from_json(json_path: str, list_path: str) -> None:
    """
    从Color_Lexicon.json中读取所有的“name”，并尝试添加进list.txt
    :param json_path: Color_Lexicon.json文件路径
    :param list_path: list.txt文件路径
    """
    with open(json_path, 'r', encoding='utf-8') as file:
        color_data = json.load(file)
    
    lst = read_list(list_path)
    new_items = []
    for key, value in color_data.items():
        name = value['name']
        lst, added = add_to_list(lst, name)
        if added:
            new_items.append(name)
    
    if new_items:
        save_list(list_path, lst)
        print("New items added:")
        for item in new_items:
            print(item)
    else:
        print("No new items added.")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    list_file_path = os.path.join(script_dir, "list.txt")
    json_file_path = os.path.abspath(os.path.join(script_dir, "../../cornerstone/Color_Lexicon.json"))
    
    # 判断调用哪个函数
    choice = input("Choose mode: 1 for input, 2 for JSON: ")
    if choice == "1":
        # 获取用户输入并添加到列表
        input_and_add(list_file_path)
    elif choice == "2":
        # 从Color_Lexicon.json中读取并添加到列表
        add_from_json(json_file_path, list_file_path)
    else:
        print("Invalid choice.")

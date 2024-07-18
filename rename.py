import os

# 设置源文件夹和目标文件夹路径
source_folder = r'E:\datasets\arcade_3000\Part 6'
target_folder = r'E:\datasets\arcade_3000\Part 6'

# 遍历源文件夹中的所有文件
for filename in os.listdir(source_folder):
    # 确保文件是以'.png'结尾的
    if filename.endswith('.png'):
        # 解析文件名中的数字部分
        number = int(filename.split('.')[0])
        # 新的文件名
        new_filename = str(number + 2000) + '.png'
        # 原始文件路径
        source_path = os.path.join(source_folder, filename)
        # 目标文件路径
        target_path = os.path.join(target_folder, new_filename)
        # 重命名文件
        os.rename(source_path, target_path)

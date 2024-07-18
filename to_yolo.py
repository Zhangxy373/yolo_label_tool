import json

# 加载标签映射字典
dic = {
    1: 1,
    2: 1,
    3: 1,
    4: 1,
    5: 4,
    6: 2,
    7: 2,
    8: 2,
    9: 2,
    10: 2,
    11: 2,
    12: 2,
    13: 3,
    14: 3,
    15: 3,
    16: 3,
    17: 1,
    18: 1,
    19: 1,
    20: 4,
    21: 4,
    22: 4,
    23: 4,
    24: 3,
    25: 1
}

# 加载JSON数据
with open('output.json') as f:
    data = json.load(f)

# 遍历每个图像`
for image in data['images']:
    filename = f"{image['file_name'][:-4]}.txt"
    with open(filename, 'w') as txt_file:
        # 遍历所有注释来查找与当前图像匹配的注释
        for annotation in data['annotations']:
            if annotation['image_id'] == image['id']:
                # 获取对象的类别ID，并通过字典映射为新的类别ID
                #category_id = int(annotation['category_id'])
                #leibie = dic[category_id]
                # 写入新的类别ID
                txt_file.write("0 ")

                # 处理并写入多边形坐标，归一化为 [0, 1] 范围
                for i in range(0, len(annotation['segmentation'][0]), 2):
                    x = round(annotation['segmentation'][0][i] / image['width'], 6)
                    y = round(annotation['segmentation'][0][i + 1] / image['height'], 6)
                    txt_file.write(f"{x} {y} ")

                txt_file.write("\n")

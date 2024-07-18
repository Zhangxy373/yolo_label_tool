import json
from PIL import Image, ImageDraw

# 加载JSON数据
with open(r'E:\datasets\arcade_3000\Part6\annotations\output.json') as f:
    data = json.load(f)

# 遍历每个图像
for image in data['images']:
    # 创建一个黑色背景的新图像
    img = Image.new('1', (image['width'], image['height']), 0)
    draw = ImageDraw.Draw(img)

    # 遍历所有注释来查找与当前图像匹配的注释
    for annotation in data['annotations']:
        if annotation['image_id'] == image['id']:
            # 绘制白色多边形
            polygon = [(annotation['segmentation'][0][i], annotation['segmentation'][0][i+1])
                       for i in range(0, len(annotation['segmentation'][0]), 2)]
            draw.polygon(polygon, fill=1)

    # 保存图像到指定文件夹
    img.save(f'C:/Users/35633/Desktop/data/annotations/image/{image["file_name"][:-4]}_mask.png')

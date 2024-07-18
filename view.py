import os
import cv2
import numpy as np

def load_labels(txt_folder):
    labels = {}
    for file_name in os.listdir(txt_folder):
        if file_name.endswith('.txt'):
            image_id = int(os.path.splitext(file_name)[0])
            print(image_id)
            with open(os.path.join(txt_folder, file_name), 'r') as f:
                labels[image_id] = f.readlines()  # 读取所有行
    return labels
def main(image_folder, txt_folder):
    labels = load_labels(txt_folder)
    for file_name in os.listdir(image_folder):
        if file_name.endswith('.png'):
            image_id = int(os.path.splitext(file_name)[0])
            print(image_id)
            image_path = os.path.join(image_folder, file_name)
            label_lines = labels.get(image_id, [])  # 获取图像的标签行
            print(label_lines)
            # 读取图像
            image = cv2.imread(image_path)
            # 在图像上绘制标签
            for label_line in label_lines:
                label_id, *points = label_line.split()  # 解析标签id和坐标点
                points = [(int(float(x) * image.shape[1]), int(float(y) * image.shape[0])) for x, y in
                          zip(points[::2], points[1::2])]
                if len(points) >= 3:  # Need at least three points to form a valid polygon
                    cv2.polylines(image, [np.array(points)], isClosed=True, color=(0, 255, 0), thickness=2)  # 绘制多边形

            cv2.imshow('Image', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

if __name__ == "__main__":
    image_folder = r'E:\datasets\part6_coco\annotations\image'  # 替换为图像文件夹的路径
    txt_folder = (r'E:\datasets\part6_coco\annotations\yolo')  # 替换为TXT文件夹的路径
    main(image_folder, txt_folder)

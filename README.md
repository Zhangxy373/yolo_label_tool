# README

这是几个自用的小程序，用于处理不同格式的标签数据。我们希望将不同格式的标签转化成被YOLO模型接受的数据，或者在图片上预览标签的效果。我发现现有的工具可能并不能很好的解决这些问题，尤其是当分割的图像出现环状标签的时候。所以我自己开发了几个小程序，旨在解决这些问题。其中，面对有闭环的文件，我在环的最薄处开一个缺口使它转变成多边形。然而这种做法并不一定适合所有的工作，所以请酌情使用。

`rename.py`：文件批量重命名

`to_yolo.py`：将COCO格式的json文件转换成YOLO格式的txt文件

`to_image.py`：将多边形格式的json文件转换成黑白掩膜格式的标签文件

`trans.py`：将RLE格式的json文件转换为多边形格式的json文件

`view.py`：在原图上查看txt格式的标签

These are a few self-used applets for processing label data in different formats. We want to convert the labels in different formats into data that can be accepted by the YOLO model, or preview the effect of the labels on the image. I've found that existing tools may not be able to solve these problems very well, especially when the segmented image is labeled in a ring. So I've developed a couple of mini-programs myself that aim to solve these problems. In the case of a closed-loop file, I cut a gap in the thinnest part of the loop to turn it into a polygon. However, this may not be suitable for all jobs, so use it sparingly.

`rename.py`: Batch rename of files

`to_yolo.py` : converts the COCO json file to the YOLO txt file

`to_image.py`: Convert polygon format json file into black and white mask format label file

`trans.py` : converts the RLE format json file to a polygon format json file

`view.py`: View the txt label on the original image

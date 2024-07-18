import json
import numpy as np
import cv2
from pycocotools.coco import COCO
from pycocotools import mask as mask_utils
from tqdm import tqdm

epsilon_change = 0.0004

def decode_rle_to_mask(rle, height, width):
    """
    Decode RLE mask encoding into a binary mask of dimensions (height, width).
    Handles different cases of RLE encoding, including both list of counts and base64 encoded strings.
    """
    if isinstance(rle, dict):  # Single segmentation
        if 'counts' in rle and isinstance(rle['counts'], list):
            # Convert uncompressed RLE to compressed RLE if necessary
            rle = mask_utils.frPyObjects([rle], height, width)[0]
        # Decode the mask
        mask = mask_utils.decode([rle])
    elif isinstance(rle, list) and all(isinstance(x, dict) for x in rle):  # Multiple segmentations
        # Decode each RLE object and combine the masks
        mask = np.zeros((height, width), dtype=np.uint8)
        for single_rle in rle:
            single_mask = mask_utils.decode([single_rle])
            mask = np.maximum(mask, single_mask)
    else:
        raise ValueError("Invalid RLE format")
    return mask
def find_closest_points(contour1, contour2):
    min_dist = float('inf')
    closest_pair = (None, None)
    idx1, idx2 = -1, -1
    for i, point1 in enumerate(contour1):
        for j, point2 in enumerate(contour2):
            dist = np.linalg.norm(point1[0] - point2[0])
            if dist < min_dist:
                min_dist = dist
                closest_pair = (point1, point2)
                idx1, idx2 = i, j
    return closest_pair, idx1, idx2
def approx_contour(contour):
    global epsilon_change
    epsilon = epsilon_change * cv2.arcLength(contour, True)  # 适应轮廓精度参数
    approx = cv2.approxPolyDP(contour, epsilon, True)
    return approx.reshape(-1, 2)  # 确保轮廓是扁平化处理的
def generate_polygon_points(contour, start_idx, num_points=10):  # 增加点数以提高精度
    points = []
    for i in range(num_points):
        idx = (start_idx + i) % len(contour)  # 环绕索引
        points.append(contour[idx][0].tolist())
    return points


def insert_inner_into_outer(outer_contour, inner_contour):
    closest_outer_idx, closest_inner_idx = find_closest_point_pair(outer_contour, inner_contour)

    # Rotate inner contour so the closest point is first
    rotated_inner_contour = rotate_inner_contour(inner_contour, closest_inner_idx)

    # Insert the whole inner contour into the outer contour at the closest point
    modified_contour = np.insert(outer_contour, closest_outer_idx + 1, rotated_inner_contour, axis=0)

    return modified_contour
def find_closest_point_pair(outer_contour, inner_contour):
    min_dist = np.inf
    closest_outer_idx = -1
    closest_inner_idx = -1

    # Find the closest points between the outer and inner contours
    for outer_idx, outer_point in enumerate(outer_contour):
        for inner_idx, inner_point in enumerate(inner_contour):
            dist = np.linalg.norm(outer_point[0] - inner_point[0])
            if dist < min_dist:
                min_dist = dist
                closest_outer_idx = outer_idx
                closest_inner_idx = inner_idx

    return closest_outer_idx, closest_inner_idx
def rotate_inner_contour(inner_contour, closest_inner_idx):
    # Rotate the inner contour such that the closest point is first
    return np.roll(inner_contour, -closest_inner_idx, axis=0)
def process_contours(mask):
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    # Assuming the largest contour is the outer contour
    contours = list(contours)
    contours.sort(key=cv2.contourArea, reverse=True)
    modified_polygons = []
    outer_contour = contours[0]
    contours.pop(0)

    if len(contours) > 0:  # Check if there are inner contours
        for inner_contour in contours:
            outer_contour = insert_inner_into_outer(outer_contour, inner_contour)
            # Approximate the contour to a polygon and add it to the list
            approx = approx_contour(outer_contour)
        modified_polygons.append(approx.flatten().tolist())
    else:
        # No inner contours, simply approximate the outer contour
        approx = approx_contour(outer_contour)
        modified_polygons.append(approx.flatten().tolist())

    return modified_polygons if modified_polygons else [[]]
def process_annotations(input_json_path, output_json_path):
    with open(input_json_path) as file:
        data = json.load(file)

    coco = COCO(input_json_path)
    annotations = data['annotations']
    for annotation in tqdm(annotations, desc="Processing annotations"):
        img_id = annotation['image_id']
        img_info = coco.loadImgs(img_id)[0]
        mask = decode_rle_to_mask(annotation['segmentation'], img_info['height'], img_info['width'])
        modified_polygons = process_contours(mask)
        annotation['segmentation'] = modified_polygons

    with open(output_json_path, 'w') as file:
        json.dump(data, file, indent=4)
input_json_path = r'E:\datasets\arcade_3000\Part2\annotations\instances_default.json'
output_json_path = r'E:\datasets\arcade_3000\Part2\annotations\output.json'
process_annotations(input_json_path, output_json_path)
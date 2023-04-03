""" 
Sample COCO to YOLO converter
usage: Json to YOLO [-h] in_path image_folder out_path

Convert COCO annotations to YOLO annotations

positional arguments:
  in_path      Path to the directory with input files
  image_folder Path to the directory with image files
  out_path     Path to the output directory

optional arguments:
  -h, --help  show this help message and exit

usage: json2yolo7.py [in path] [image_folder] [out folder path]
"""

import os
import json
import argparse
import numpy as np
import shutil


IM_HEIGHT = 640
IM_WIDTH = 640 


def convert_json2yolo(in_path, image_folder, out_path):
    data = load_json_data(in_path)

    # Per image basis 
    filenames = [file['file_name'] for file in data['images']]
    annotations = data['annotations']

    # Create files. 
    for i, annotation in enumerate(annotations):
        image_id = annotation['image_id']
        label_category = annotation['category_id']
        # If the frame was extracted
        if os.path.exists("{}/{:04d}.jpg".format(image_folder, image_id)):
            bbox = annotation['bbox']
            yl_bbox = convert_bbox(bbox, IM_HEIGHT, IM_WIDTH)

            # If the text file just being created copy the corresponding frame
            if not os.path.exists("{}/labels/{:04d}.txt".format(out_path, image_id)):
                shutil.copyfile("{}/{:04d}.jpg".format(image_folder, image_id), "{}/images/{:04d}.jpg".format(out_path, image_id))

            # Open and write to atxt 
            f = open("{}/labels/{:04d}.txt".format(out_path, image_id),"a")
            f.write(f'{label_category-1} {yl_bbox[0]} {yl_bbox[1]} {yl_bbox[2]} {yl_bbox[3]} \n') # Verify the order later
            f.close()

    print('Done.')

# Define functions
def load_json_data(path):
    file = open(path)
    data = json.load(file)
    file.close()
    return data

def convert_bbox(bbox, im_height, im_width):
    yolo_bbox = []
    xmin = bbox[0]
    ymin = bbox[1]
    width = bbox[2]
    height = bbox[3]

    x_center = ((xmin*2 + width)/2)/im_width
    y_center = ((ymin*2 + height)/2)/im_height

    yolo_bbox.append(x_center)
    yolo_bbox.append(y_center)
    yolo_bbox.append(width/im_width)
    yolo_bbox.append(height/im_height)

    return yolo_bbox

if __name__ == '__main__':
    # Create a parset 
    parser = argparse.ArgumentParser()

    parser.add_argument('in_path', help = 'Path to the directory with input files', type = str)
    parser.add_argument('image_folder', help = 'Path to the directory with image files', type = str)
    parser.add_argument('out_path', help = 'Path to the output directory', type = str)

    args = parser.parse_args()

    # Convert the labels
    convert_json2yolo(args.in_path, args.image_folder, args.out_path)



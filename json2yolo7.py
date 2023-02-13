import os
import json
import argparse
import numpy as np
import shutil

# Create a parset 
parser = argparse.ArgumentParser()

parser.add_argument('in_path', help = 'Path to the directory with input files', type = str)
parser.add_argument('image_folder', help = 'Path to the directory with image files', type = str)
parser.add_argument('out_path', help = 'Path to the output directory', type = str)

args = parser.parse_args()

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

data = load_json_data(args.in_path)

# Per image basis 
filenames = [file['file_name'] for file in data['images']]
annotations = data['annotations']

# Create files. 
for i, annotation in enumerate(annotations):
    image_id = annotation['image_id']
    label_category = annotation['category_id']
    # If the frame was extracted
    if os.path.exists("{}/{:04d}.jpg".format(args.image_folder, image_id)):
        bbox = annotation['bbox']
        yl_bbox = convert_bbox(bbox, 640, 640)

        # If the text file just being created copy the corresponding frame
        if not os.path.exists("{}/labels/{:04d}.txt".format(args.out_path, image_id)):
            shutil.copyfile("{}/{:04d}.jpg".format(args.image_folder, image_id), "{}/images/{:04d}.jpg".format(args.out_path, image_id))

        # Open and write to atxt 
        f = open("{}/labels/{:04d}.txt".format(args.out_path, image_id),"a")
        f.write(f'{label_category-1} {yl_bbox[0]} {yl_bbox[1]} {yl_bbox[2]} {yl_bbox[3]} \n') # Verify the order later
        f.close()

print('Done.')





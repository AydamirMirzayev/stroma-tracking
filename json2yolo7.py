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
        bbox = np.array(annotation['bbox'])/640

        # If the text file just being created copy the corresponding frame
        if not os.path.exists("{}/annotations/{:04d}.txt".format(args.out_path, image_id)):
            shutil.copyfile("{}/{:04d}.jpg".format(args.image_folder, image_id), "{}/images/{:04d}.jpg".format(args.out_path, image_id))

        # Open and write to atxt 
        f= open("{}/annotations/{:04d}.txt".format(args.out_path, image_id),"a")
        f.write(f'{label_category} {bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]} \n') # Verify the order later
        f.close()


print('Done.')






""" Sample Frame Extractor for Video files
usage: Frame Extractor [-h] in_path N out_path

Extracts every n-th frame from the input video

positional arguments:
  in_path     Path to the directory with input files
  N           N - to extract each Nth frame
  out_path    Path to the output directory

optional arguments:
  -h, --help  show this help message and exit

usage: extract_frames.py [in path] [N - for every Nth frame] [out folder path]
"""

import os 
import argparse

# Define parser
parser = argparse.ArgumentParser(
                    prog = 'Frame Extractor',
                    description = 'Extracts every n-th frame from the input video',
                    epilog = 'usage: extract_frames.py [in path] [N - for every Nth frame] [out folder path]')

parser.add_argument('in_path', help = 'Path to the directory with input files', type = str)
parser.add_argument('N', help = 'N - to extract each Nth frame', type = int)
parser.add_argument('out_path', help = 'Path to the output directory', type = str)

# Adjsut the command string 
args = parser.parse_args()
command = f'ffmpeg -i {args.in_path} {args.out_path}/%04d.jpg'

# Execute extraction 
print("Executing...")
print(command)
os.system(command)

# Remove intermediate frames
for filename in os.listdir(args.out_path):
  count = filename.split('.')[0][-4:]
  count = int(count)
  if count % int(args.N) != 0:
    #print(f"{args.out_path}/{filename}")
    os.remove(f"{args.out_path}/{filename}")

print('Done')
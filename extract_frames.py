import os 
import argparse

# Define parser
parser = argparse.ArgumentParser(
                    prog = 'Frame Extractor',
                    description = 'Extracts every n-th frame from the input video',
                    epilog = 'usage: extract_frames.py [in path] [N - for every Nth frame] [out folder path] [filename header]')

parser.add_argument('in_path')
parser.add_argument('N')
parser.add_argument('out_path')
parser.add_argument('header')

# Adjsut the command string 
args = parser.parse_args()
command = f'ffmpeg -i {args.in_path} -vf "select=not(mod(n\,{args.N}))" -vsync vfr {args.out_path}/{args.header}_%04d.png'

# Execute extraction 
print("Executing...")
print(command)
print('ffmpeg -i ./images/test/test.mp4 -vf "select=not(mod(n\,10))" -vsync vfr ./frames/test/test_frame_%04d.png')
os.system(command)

# Correct the naming, to avoid naming conflict start from the end. 
print("Correcting naming...")
filenames = [file for file in os.listdir(args.out_path)]
filenames = filenames[::-1]
for filename in filenames:
	count =  filename.split('.')[0][-4:]
	count = int(count)
	count = count * int(args.N) 
	new_filename = "{}/{}_{:04d}.png".format(args.out_path, args.header, count)
	os.rename( f'{args.out_path}/{filename}', new_filename )

print('Done')
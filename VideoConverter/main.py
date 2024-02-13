# Program that converts video files from one folder, from one format into another
# First ask for four inputs
# 1. the input folder
# 2. the output folder
# 3. the input format
# 4. the output format
# Then convert all the files in the input folder to the output format and save them in the output folder
import os
import sys
import argparse
import ffmpeg

# Define the arguments
parser = argparse.ArgumentParser(description='Convert audio files from one format to another')
parser.add_argument('-i', '--input', help='Input folder', default='input')
parser.add_argument('-o', '--output', help='Output folder', default='output')
parser.add_argument('-if', '--input_format', help='Input format', default='mkv')
parser.add_argument('-of', '--output_format', help='Output format', default='mp4')
args = parser.parse_args()

# Define the input and output folders
input_folder = args.input
output_folder = args.output

# Define the input and output formats
input_format = args.input_format
output_format = args.output_format

# Check if the input folder exists
if not os.path.exists(input_folder):
    print('Input folder does not exist')
    sys.exit(1)

# Check if the output folder exists
if not os.path.exists(output_folder):
    os.mkdir(output_folder)

# Get the list of files in the input folder
files = os.listdir(input_folder)

# Loop through the files
for file in files:
    # Check if the file is an video file
    if file.lower().endswith(input_format.lower()):
        # Get the full path of the file
        full_path = os.path.join(input_folder, file)
        # Load the file
        input_stream = ffmpeg.input(full_path)
        # Get the name of the file without the extension
        name = os.path.splitext(file)[0]
        # Get the full path of the output file
        output_file = os.path.join(output_folder, name + '.' + output_format)
        # Save the file
        output_stream = ffmpeg.output(input_stream, output_file)
        ffmpeg.run(output_stream)

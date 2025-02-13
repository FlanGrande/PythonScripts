# Program that converts images in one folder from one format to another
import os
import sys
import argparse
from PIL import Image

parser = argparse.ArgumentParser()
parser.description = "Convert images from one format to another"
parser.epilog = "Example: python3 main.py input output png jpeg"
parser.add_argument("-i", "--input-folder", help="Input folder", default="input")
parser.add_argument("-o", "--output-folder", help="Output folder", default="output")
parser.add_argument("-s", "--source-format", help="Source format", default="png")
parser.add_argument("-f", "--output-format", help="Output format", default="jpeg")
parser.add_argument("-R", "--resize-width", help="Resizes to given width, respecting aspect ratio", default=1920)
parser.add_argument("-L", "--lossless", action="store_true", help="Lossless compression")
parser.add_argument("-q", "--quality", help="Compression quality, 100 is better quality", default=100)


args = parser.parse_args()
input_folder = args.input_folder
output_folder = args.output_folder
source_format = args.source_format
output_format = args.output_format
resize_width = int(args.resize_width)
lossless = args.lossless
quality = args.quality

def retrieve_images(input_folder):
	images = []
	for root, dirs, files in os.walk(input_folder):
		for file in files:
			if file.endswith(source_format):
				images.append(file)
	return images

def convert_images(images):
	for image in images:
		clean_name = os.path.splitext(image)[0]
		print("Processing " + clean_name + "...")
		img = Image.open(input_folder + "/" + image)
		# if jpeg, convert to RGB
		if output_format.lower() == "jpeg":
			img = img.convert("RGB")
		#if png, convert to RGBA
		if output_format.lower() == "png":
			img = img.convert("RGBA")
		
		# while image width is over 2000px, resize image to half
		# while img.width > 2000 and reduce_size:
		# 	img = resize_image_to_half(img)

		if img.width != resize_to_width:
			img = resize_to_width(img, resize_width)
		
		img.save(output_folder + "/" + clean_name + "." + output_format, output_format, lossless = lossless, method = 4, quality = quality)
		#close image
		img.close()

def resize_to_width(image, width):
	resizing_factor = image.width / width
	#print(resizing_factor)
	return image.resize((int(width), int(image.height / resizing_factor)), Image.Resampling.LANCZOS)

# resize images
def resize_image_to_half(image):
	width, height = image.size
	return image.resize((int(width/2), int(height/2)), Image.Resampling.BILINEAR)

# Main program
if __name__ == "__main__":
	# Folder checks
	if not os.path.exists(input_folder):
		print("Input folder does not exist")
		sys.exit(1)
	
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)
	
	# Sanitize input

	images = retrieve_images(input_folder)
	convert_images(images)

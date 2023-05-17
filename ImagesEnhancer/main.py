# The following program reads images from an "input" folder and creates new version of the images in an "output" folder.
# The new images are created by enhancing the quality of the images.
# The program uses the OpenCV library to read and write images.
# The program uses the Pillow library to enhance the quality of the images.
# The program uses the os library to read and write files.

import cv2
import numpy as np
import os

# Define the path to the input folder
input_path = "input"
# Define the path to the output folder
output_path = "output"

# Create the output folder if it does not exist
if not os.path.exists(output_path):
    os.makedirs(output_path)

# Get the list of files in the input folder
files = os.listdir(input_path)

# Using CUDA
#cv2.cuda.setDevice(0)

total_time = 0
print("")

# Loop through the files in the input folder
for file in files:
    print(f"Enhancing {file}...")

    # Measure time it takes
    start = cv2.getTickCount()

    # Read the image
    image = cv2.imread(input_path + "/" + file)
    im2 = image

    # If height or width is less than 1000, resize the image
    if image.shape[0] <= 1080 or image.shape[1] <= 1080:
        # Super resolution using dnn
        im2 = cv2.dnn_superres.DnnSuperResImpl_create()
        im2.readModel("models/EDSR_x2.pb")
        im2.setModel("edsr", 2)
        im2 = im2.upsample(image)

    # White balance
    #im2 = cv2.xphoto.createGrayworldWB()
    #im2 = im2.balanceWhite(im2)
    
    # Enhance the image
    im2 = cv2.detailEnhance(im2, sigma_s=5, sigma_r=0.1)
    denoise_factor = 0.1;
    denoise_amount_base = cv2.Laplacian(image, cv2.CV_64F).var()
    print(f"Denoise amount before clip: {denoise_amount_base}")
    denoise_amount_clipped = np.clip(denoise_amount_base * denoise_factor, 8, 24)
    print(f"Denoise amount after clip: {denoise_amount_clipped}")

    # Denoise the image
    if denoise_amount_base > 200: 
        im2 = cv2.bilateralFilter(im2, 9, 75, 75)
    
    im2 = cv2.fastNlMeansDenoisingColored(im2, None, 10, denoise_amount_clipped, 7, 21)

    # Measure time it takes
    end = cv2.getTickCount()

    # Save the enhanced image
    cv2.imwrite(output_path + "/" + file, im2)


    '''cv2.namedWindow("Original Image", cv2.WINDOW_NORMAL)
    cv2.namedWindow("Enhanced Image", cv2.WINDOW_NORMAL)

    # Display the original image and the enhanced image
    cv2.imshow("Original Image", image)
    cv2.imshow("Enhanced Image", cv2.imread(output_path + "/" + file))
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''

    print(f"Enhanced {file} in {(end - start) / cv2.getTickFrequency()} seconds!")

    # Calculate total time
    total_time += (end - start) / cv2.getTickFrequency()

    # Free memory
    #del im2

    print("")

# total time in seconds
#total_time = total_time / 60

# Print the total time
print(f"Done in {total_time}!")
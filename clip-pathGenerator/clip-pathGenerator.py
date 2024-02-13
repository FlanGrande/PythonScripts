import cv2
import re

def extract_clip_path(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    # Extract the alpha channel (transparency)
    alpha_channel = image[:, :, 3]

    # Threshold the alpha channel to create a binary mask
    _, binary_mask = cv2.threshold(alpha_channel, 0, 255, cv2.THRESH_BINARY)

    # Find the contours in the mask
    contours, _ = cv2.findContours(binary_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort the contours by area, and get the largest one
    contour = max(contours, key=cv2.contourArea)

    # Approximate the contour to a polygon
    epsilon = 0.02 * cv2.arcLength(contour, True)
    polygon = cv2.approxPolyDP(contour, epsilon, True)

    # Dimensions of the image
    width, height = image.shape[1], image.shape[0]

    # Extract the x and y coordinates of the polygon vertices and convert to percentages
    vertices_percent = [(vertex[0][0] / width * 100, vertex[0][1] / height * 100) for vertex in polygon]

    # Format the coordinates to create the clip-path property
    clip_path = "clip-path: polygon(" + ", ".join(f"{x:.2f}% {y:.2f}%" for x, y in vertices_percent) + ");"

    # Verify the clip-path format
    clip_path_pattern = r'^clip-path: polygon\((-?\d+(\.\d+)?%\s-?\d+(\.\d+)?%(,\s)?)+\);$'
    is_valid_clip_path = bool(re.match(clip_path_pattern, clip_path))
    
    if is_valid_clip_path:
        return clip_path
    else:
        raise ValueError("Generated clip-path is not valid CSS")

if __name__ == "__main__":
    image_path = input("Enter the path to your image: ")
    try:
        result = extract_clip_path(image_path)
        print(result)
    except Exception as e:
        print(f"Error: {e}")

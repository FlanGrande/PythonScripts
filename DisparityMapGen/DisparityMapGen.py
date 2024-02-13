
import cv2
import numpy as np
import zipfile
import os

def compute_disparity(left_image, right_image):
    left_gray = cv2.cvtColor(left_image, cv2.COLOR_RGB2GRAY)
    right_gray = cv2.cvtColor(right_image, cv2.COLOR_RGB2GRAY)
    stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    disparity = stereo.compute(left_gray, right_gray)
    return disparity

def disparity_to_depth(disparity_map):
    depth_map = 1.0 / (disparity_map + 0.0001)
    depth_map = (depth_map - depth_map.min()) / (depth_map.max() - depth_map.min())
    return depth_map

def compute_normal_map(depth_map, step=1):
    height, width = depth_map.shape
    normal_map = np.zeros((height, width, 3), dtype=np.float32)

    for y in range(1, height - 1, step):
        for x in range(1, width - 1, step):
            dzdx = (depth_map[y, x + 1] - depth_map[y, x - 1]) / 2.0
            dzdy = (depth_map[y + 1, x] - depth_map[y - 1, x]) / 2.0
            direction = np.cross([1, 0, dzdx], [0, 1, dzdy])
            magnitude = np.linalg.norm(direction)
            normal_map[y, x] = direction / magnitude
    return (normal_map * 0.5 + 0.5) * 255

def process_image(image_path, output_dir):
    stereo_image = cv2.imread(image_path)
    height, width, _ = stereo_image.shape
    left_image = stereo_image[:, :width//2, :]
    right_image = stereo_image[:, width//2:, :]
    
    disparity_map = compute_disparity(left_image, right_image)
    depth_map = disparity_to_depth(disparity_map)
    height_map = depth_map * 255
    normal_map = compute_normal_map(depth_map)
    
    base_filename = os.path.splitext(os.path.basename(image_path))[0]
    zip_filename = os.path.join(output_dir, f"{base_filename}.zip")
    
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        cv2.imwrite("disparity.png", disparity_map)
        cv2.imwrite("depth_map.png", (depth_map * 255).astype(np.uint8))
        cv2.imwrite("height_map.png", height_map.astype(np.uint8))
        cv2.imwrite("normal_map.png", normal_map.astype(np.uint8))
        
        zipf.write("disparity.png")
        zipf.write("depth_map.png")
        zipf.write("height_map.png")
        zipf.write("normal_map.png")

def main():
    input_dir = "input"
    output_dir = "output"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for image_name in os.listdir(input_dir):
        if image_name.endswith(('.png', '.jpg', '.jpeg')):
            process_image(os.path.join(input_dir, image_name), output_dir)

if __name__ == "__main__":
    main()

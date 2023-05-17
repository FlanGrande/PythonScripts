from PIL import Image, ImageFilter 

current_image = 0
grid_x = 8
grid_y = 16
grid_width = 32
grid_height = 32

background = Image.new('RGBA',(grid_width*grid_x, grid_height*grid_y), (255, 255, 255, 0))

for i in range(0, grid_x * grid_y):

	try:
		path = "./input/" + '{:>04}'.format(i) + ".png"
		print(path)

		image = Image.open(path)

		img_w, img_h = image.size
		bg_w, bg_h = background.size
		coords = (int(i % grid_x), int(i / grid_x)) # coords[0] is x ; coords[1] is y
		offset = (int(coords[0] * img_w), int((coords[1] * img_h)))
		background.paste(image, offset)

		print("Image: " + str(int((i / grid_x) % (grid_x + grid_y))))
		print("Coords: " + str(coords))
		print("Offset: " + str(offset))
		print("\n")

	except FileNotFoundError:
		print("oopps")

background.save("./output/strip.png")
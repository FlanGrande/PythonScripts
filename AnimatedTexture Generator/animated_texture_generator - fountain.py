from PIL import Image, ImageFilter 

initial_frame = 120
frames = 120
fps = 60.0
texture_path = "res://textures/environment/fountain/"
output = "./output/AT_Fountain.tres"
text = ""

text += '[gd_resource type="AnimatedTexture" load_steps=3 format=2]\n\n'

for x in range(initial_frame, initial_frame + frames + 1):
	text += '[ext_resource path="'+ texture_path + '{:>04}'.format(x) + '.png" type="Texture" id=' + str(x) + ']\n'
	print("frame: " + str(x))
	print("\n")

text += "\n[resource]\n"
text += "frames = " + str(frames) + "\n"
text += "fps = " + str(fps) + "\n"

for x in range(initial_frame, initial_frame + frames + 1):
	text += 'frame_' + str(x - initial_frame) + '/texture = ExtResource( ' + str(x) + ' )]\n'
	if(x - 1 > 0):
		text += 'frame_' + str(x - initial_frame) + '/delay_sec = 0.0\n'
		print("frame: " + str(x))
		print("\n")

OutputFile = open(output, "w")
OutputFile.write(text)
OutputFile.close()
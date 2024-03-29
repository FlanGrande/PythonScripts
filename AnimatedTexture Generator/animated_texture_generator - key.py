from PIL import Image, ImageFilter 

frames = 60
fps = 60.0
texture_path = "res://textures/environment/key/"
output = "./output/AT_Key2.tres"
text = ""

text += '[gd_resource type="AnimatedTexture" load_steps=3 format=2]\n\n'

for x in range(1, frames + 1):
	text += '[ext_resource path="'+ texture_path + '{:>04}'.format(x) + '.png" type="Texture" id=' + str(x) + ']\n'

text += "\n[resource]\n"
text += "frames = " + str(frames) + "\n"
text += "fps = " + str(fps) + "\n"

for x in range(1, frames + 1):
	text += 'frame_' + str(x - 1) + '/texture = ExtResource( ' + str(x) + ' )]\n'
	if(x -1 > 0):
		text += 'frame_' + str(x - 1) + '/delay_sec = 0.0\n'

OutputFile = open(output, "w")
OutputFile.write(text)
OutputFile.close()
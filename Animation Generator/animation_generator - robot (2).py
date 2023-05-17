from PIL import Image, ImageFilter 

playback_speed = 0.0
frames = 128
length = 1.6
fps = 60.0
h_frames = 4
v_frames = 4
texture_path = "res://characters/robot/"
output = "./output/AnimationPlayer_Robot.tres"
starting_resource_id = 100
next_resource_id = starting_resource_id

support_text = ""

text = ""
text += '[ext_resource path="' + texture_path + 'strip.png" type="Texture" id=' + str(starting_resource_id) + ']\n\n'
next_resource_id += 1

def getOneLineOfTransitionValues(width):
	ret = ""
	for x in range(0, width):
		ret += str(x / (length*width)) + ","
	return ret[:-1]

def getOneLineOfOnes(width):
	ret = ""
	for x in range(0, width):
		ret += "1,"
	return ret[:-1] #Returns the string minus the last character (a comma)

def getOneLineOfAnimationValues(current_row, width):
	ret = ""
	for x in range(0, width):
		ret += str(x + current_row * h_frames) + ","
	return ret[:-1]

for rows in range(0, v_frames):
	text += '[sub_resource type="Animation" id=' + str(next_resource_id) + ']\n'
	text += 'resource_name = "animation_' + '{:>02}'.format(rows) + '"\n'
	text += 'length = ' + str(length) + '\n'
	text += 'loop = true' + '\n' + '\n'

	#support_text will be used at the end to put all of these values into the Animation Player
	support_text += 'anims/animation_' + '{:>02}'.format(rows) + ' = SubResource(' + str(next_resource_id) + ')' + '\n'

	next_resource_id += 1

	text += 'tracks/0/type = "value"' + '\n'
	text += 'tracks/0/path = NodePath("Sprite:frame")' + '\n'
	text += 'tracks/0/interp = 1' + '\n'
	text += 'tracks/0/loop_wrap = true' + '\n'
	text += 'tracks/0/imported = false' + '\n'
	text += 'tracks/0/enabled = true' + '\n'
	text += 'tracks/0/keys = { ' + '\n' \
			+'"times": PoolRealArray(' + getOneLineOfTransitionValues(h_frames) + '),' + '\n' \
			+'"transitions": PoolRealArray(' + getOneLineOfOnes(h_frames) + '),' + '\n' \
			+'"update": 1,' + '\n' \
			+'"values": [' + getOneLineOfAnimationValues(rows, h_frames) + ']' + '\n' \
		+'}' + '\n' + '\n'

text += '[node name="Sprite" type="Sprite" parent="."]' + '\n'
text += 'texture = ExtResource(' + str(starting_resource_id) + ')' + '\n'
text += 'vframes = ' + str(v_frames) + '\n'
text += 'hframes = ' + str(h_frames) + '\n'
text += 'frame = 0' + '\n' + '\n'

text += '[node name="AnimationPlayer" type="AnimationPlayer" parent="."]' + '\n'
text += 'playback_speed = 1.0' + '\n'
text += support_text + '\n' + '\n'

OutputFile = open(output, "w")
OutputFile.write(text)
OutputFile.close()


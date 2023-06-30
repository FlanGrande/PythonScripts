# Program that grabs a bunch of video files and puts them together in order to make a video
# import video editing libraries
import os
import sys
import argparse
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import AudioClip
from moviepy.editor import concatenate_videoclips,concatenate_audioclips,TextClip,CompositeVideoClip
from moviepy.video.fx.accel_decel import accel_decel
from moviepy.video.fx.blackwhite import blackwhite
from moviepy.video.fx.blink import blink
from moviepy.video.fx.colorx import colorx
from moviepy.video.fx.crop import crop
from moviepy.video.fx.even_size import even_size
from moviepy.video.fx.fadein import fadein
from moviepy.video.fx.fadeout import fadeout
from moviepy.video.fx.freeze import freeze
from moviepy.video.fx.freeze_region import freeze_region
from moviepy.video.fx.gamma_corr import gamma_corr
from moviepy.video.fx.headblur import headblur
from moviepy.video.fx.invert_colors import invert_colors
from moviepy.video.fx.loop import loop
from moviepy.video.fx.lum_contrast import lum_contrast
from moviepy.video.fx.make_loopable import make_loopable
from moviepy.video.fx.margin import margin
from moviepy.video.fx.mask_and import mask_and
from moviepy.video.fx.mask_color import mask_color
from moviepy.video.fx.mask_or import mask_or
from moviepy.video.fx.mirror_x import mirror_x
from moviepy.video.fx.mirror_y import mirror_y
from moviepy.video.fx.painting import painting
from moviepy.video.fx.resize import resize
from moviepy.video.fx.rotate import rotate
from moviepy.video.fx.scroll import scroll
from moviepy.video.fx.speedx import speedx
from moviepy.video.fx.supersample import supersample
from moviepy.video.fx.time_mirror import time_mirror
from moviepy.video.fx.time_symmetrize import time_symmetrize

from moviepy.audio.fx.audio_fadein import audio_fadein
from moviepy.audio.fx.audio_fadeout import audio_fadeout
from moviepy.audio.fx.audio_left_right import audio_left_right
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
from moviepy.audio.fx.volumex import volumex

# grab the arguments
parser = argparse.ArgumentParser()

# add a comment at the top of the help information with an example of the command
parser.description = "Example: python3 main.py -i C:/Users/user/Videos/ -o C:/Users/user/EditedVideos/ -f mp4 -n MyVideo -a C:/Users/user/Music/MySong.mp3"

parser.add_argument("-i", "--inputFolder", help='Folder where the videos are. E.g. "C:/Users/user/Videos/"', default="input")
parser.add_argument("-o", "--outputFolder", help='Folder where the output video will be E.g. "C:/Users/user/EditedVideos/"', default="output")
parser.add_argument("-f", "--format", help='Format of the video. E.g. "mp4"', default="mp4")
parser.add_argument("-n", "--outputName", help='Name of the output video. E.g. "MyVideo"', default="MyVideo")
parser.add_argument("-a", "--audio", help='Audio file to add to the video. E.g. "C:/Users/user/Music/MySong.mp3"', default="noaudio")
args = parser.parse_args()

# make a list of the input video files
def readVideosIntoList():
    # make a list of the files in the input folder sorted by name
    files = os.listdir(args.inputFolder)
    files.sort()
    # make a list of the video files
    videos = []
    for file in files:
        ends_with_format = file.lower().endswith("." + args.format.lower())
        if ends_with_format:
            videos.append(file)
    return videos

def joinVideosFromList(videos):
    # join the videos
    clips = []
    for video in videos:
        clip = VideoFileClip(args.inputFolder + video)
        clips.append(clip)
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(args.outputFolder + args.outputName + "." + args.format)

def createClip():
    # sanitize the input
    if args.inputFolder[-1] != "/": args.inputFolder += "/"
    if args.outputFolder[-1] != "/": args.outputFolder += "/"

    # sanitize the format
    if args.format[0] == ".": args.format = args.format[1:]

    # create output folder if it doesn't exist
    if not os.path.exists(args.outputFolder):
        os.makedirs(args.outputFolder)
    
    videos = readVideosIntoList()
    joinVideosFromList(videos)

if __name__ == "__main__":
    createClip()
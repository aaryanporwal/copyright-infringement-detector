import os
import argparse
from PIL import Image
import imagehash
from extract_frames import FrameExtractor
from make_collage import MakeCollage

parser = argparse.ArgumentParser(
  prog="Hamming Distance Calculator",
  description="Calculate the hamming distance between two videos",
  epilog="python3 ihash.py <src_video> <t_video> -> returns hamming distance",
  add_help=True
)

parser.add_argument("-v1", help="Source Video(FULL PATH)", required=True, type=str)
parser.add_argument("-v2", help="Target Video(FULL PATH)", required=False, type=str)

# Example call: python3 ihash.py -v1 video.mp4 -v2 video_with_markup.mp4


args = parser.parse_args()

src_video = args.v1 # Path to source video
t_video = args.v2 # Path to target video

# Extract frames from videos -> create a collage of frames -> create hash of collage -> calculate hamming distance between hashes

frames_src_output_dir = "frames-v1"
frames_t_output_dir = "frames-v2"
collage_src_path ="collage_src"
collage_t_path ="collage_t"
collage_src_path = os.path.join(collage_src_path, "collage-v1.jpg")
collage_t_path = os.path.join(collage_t_path, "collage-v2.jpg")

FrameExtractor(src_video, frames_src_output_dir)
FrameExtractor(t_video, frames_t_output_dir)

# make a list of all the paths in frames_output_dir
list_of_frames1 = sorted([(os.path.join(frames_src_output_dir, filename))for filename in os.listdir(frames_src_output_dir)])
list_of_frames2 = sorted([(os.path.join(frames_t_output_dir, filename))for filename in os.listdir(frames_t_output_dir)])

# make collage
MakeCollage(
            list_of_frames1,
            collage_src_path,
            collage_image_width=1024,
        )
        
MakeCollage(
            list_of_frames2,
            collage_t_path,
            collage_image_width=1024,
        )
        
src_hash = imagehash.phash(Image.open(os.path.join(collage_src_path)))
t_hash = imagehash.phash(Image.open(os.path.join(collage_t_path)))

print(src_hash - t_hash) # print hamming distance
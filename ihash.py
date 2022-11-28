import os
import argparse
from PIL import Image
import imagehash
from extract_frames import FrameExtractor
from make_collage import MakeCollage

parser = argparse.ArgumentParser(
  prog="Image Hash",
  description="Calculate the hamming distance between two images",
  epilog="python3 ihash.py <srcimg> <t-img> -> returns hamming distance",
  add_help=True
)

parser.add_argument("-v1", help="Source Video(FULL PATH)", required=True, type=str)
parser.add_argument("-v2", help="Target Video(FULL PATH)", required=False, type=str)

args = parser.parse_args()

src_video = args.v1 # Path to source video
t_video = args.v2 # Path to target video

# Extract frames from videos -> create a collage of frames -> create hash of collage -> calculate hamming distance between hashes

frames_output_dir = ".\\frames"
collage_path =""
collage_path = os.path.join(collage_path, "collage.jpg")

FrameExtractor(src_video, frames_output_dir)

# make a list of all the paths in frames_output_dir
list_of_frames = sorted([(os.path.join(frames_output_dir, filename))for filename in os.listdir(frames_output_dir)])

# make collage
MakeCollage(
            list_of_frames,
            collage_path,
            collage_image_width=1024,
        )
# src_hash = imagehash.phash(Image.open(srcimg))
# t_hash = imagehash.phash(Image.open(timg))

# print(src_hash - t_hash)
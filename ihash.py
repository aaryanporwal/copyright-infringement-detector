import argparse
from PIL import Image
import imagehash
from extract_frames import FrameExtractor

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

FrameExtractor(src_video, frames_output_dir)

# src_hash = imagehash.phash(Image.open(srcimg))
# t_hash = imagehash.phash(Image.open(timg))

# print(src_hash - t_hash)
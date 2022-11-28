import os
import argparse
from PIL import Image
from extract_frames import FrameExtractor
from make_collage import MakeCollage
import perceptual_hash

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

def make_collage_from_video(video_path, output_dir):
    frame_extractor = FrameExtractor(video_path, output_dir)
    list_of_frames = sorted([(os.path.join(output_dir, filename))for filename in os.listdir(output_dir)])
    collage_path = os.path.join(output_dir, "collage.jpg")
    MakeCollage(
            list_of_frames,
            collage_path,
            collage_image_width=1024,
        )
    return collage_path

src_hash = perceptual_hash.phash(Image.open(os.path.join(make_collage_from_video(src_video, "frames-v1"))))
t_hash = perceptual_hash.phash(Image.open(os.path.join(make_collage_from_video(t_video, "frames-v2"))))

print(src_hash - t_hash) # print hamming distance

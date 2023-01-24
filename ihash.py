import os
import argparse
from PIL import Image
from extract_frames import FrameExtractor
from make_collage import MakeCollage
import perceptual_hash
import redis
#import env variables from .env
import dotenv
dotenv.load_dotenv()

parser = argparse.ArgumentParser(
  prog="Hamming Distance Calculator",
  description="Find similar videos",
  epilog="python3 ihash.py <t_video> -> returns hamming distance",
  add_help=True
)

# parser.add_argument("-v1", help="Target Video(FULL PATH)", required=True, type=str)
# parser.add_argument("-v1", help="Source Video(FULL PATH)", required=True, type=str) 

# Example call: python3 ihash.py -v1 video.mp4 -v2 video_with_markup.mp4

# args = parser.parse_args()

t_video = "video.mp4" # Path to target video

def make_collage_from_video(video_path, output_dir):
    frame_extractor = FrameExtractor(video_path, output_dir)
    list_of_frames = sorted([(os.path.join(output_dir, filename))for filename in os.listdir(output_dir)])
    collage_path = os.path.join(output_dir, "collage.jpg")
    MakeCollage(
            list_of_frames,
            collage_path,
            collage_image_width=1024,)
    return collage_path

def hamming_distance(str1, str2):
    distance = 0
    L = len(str1)
    for i in range(L):
        if str1[i] != str2[i]:
            distance += 1
    return distance

# src_hash = str(perceptual_hash.phash(Image.open(os.path.join(make_collage_from_video(src_video, "frames-v1")))))
if not os.path.exists("frames-v2"):
    os.makedirs("frames-v2")
    
t_hash = str(perceptual_hash.phash(Image.open(os.path.join(make_collage_from_video(t_video, "frames-v2")))))
print(t_hash)

r = redis.from_url(os.getenv("REDIS_URL"))
# r.rpush("src_hashes", str(src_hash))
# list_of_src_hashes = r.lrange("src_hashes", 0, -1)

SIMILARITY_THRESHOLD = 10
global_min = SIMILARITY_THRESHOLD

# for i in range(r.llen("src_hashes")):
#     # https://stackoverflow.com/questions/25745053/about-char-b-prefix-in-python3-4-1-client-connect-to-redis
#     # print(r.lindex("src_hashes", i).decode("utf-8")) # .decode() because redis is returning bytestring
#     global_min = min(global_min, hamming_distance((r.lindex("src_hashes", i).decode("utf-8")), t_hash))


if global_min >= SIMILARITY_THRESHOLD:
    print("Video you provided is not infringed, with hamming distance: " + str(global_min))
else:
    print("Infringed video found, with hamming distance: " + str(global_min))

# print(global_min)


# print(list_of_src_hashes)

# get src_hash[0] from redis and call hamming_distance(src_hash[0], t_hash)
# hamming_distance(src_hash, t_hash)

# src_hash = perceptual_hash.phash(Image.open(os.path.join(make_collage_from_video(src_video, "frames-v1"))))
# print(src_hash - t_hash) # print hamming distance

import argparse
from PIL import Image
import imagehash

parser = argparse.ArgumentParser(
  prog="Image Hash",
  description="Calculate the hamming distance between two images",
  epilog="python3 ihash.py <srcimg> <t-img> -> returns hamming distance",
  add_help=True
)

parser.add_argument("-i1", help="Source image(FULL PATH)", required=True)
parser.add_argument("-i2", help="Target image(FULL PATH)", required=True)

args = parser.parse_args()

srcimg = args.i1
timg = args.i2

src_hash = imagehash.phash(Image.open(srcimg))
t_hash = imagehash.phash(Image.open(timg))

print(src_hash - t_hash)
import numpy
from PIL import Image
ANTIALIAS = Image.ANTIALIAS

def _binary_array_to_hex(arr):
	"""
	internal function to make a hex string out of a binary array.
	"""
	bit_string = ''.join(str(b) for b in 1 * arr.flatten())
	width = int(numpy.ceil(len(bit_string) / 4))
	return '{:0>{width}x}'.format(int(bit_string, 2), width=width)

"""
You may copy this file, if you keep the copyright information below:


Copyright (c) 2013-2022, Johannes Buchner
https://github.com/JohannesBuchner/imagehash

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.

Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

class ImageHash:
	"""
	Hash encapsulation. Can be used for dictionary keys and comparisons.
	"""

	def __init__(self, binary_array):
		# type: (NDArray) -> None
		self.hash = binary_array  # type: NDArray

	def __str__(self):
		return _binary_array_to_hex(self.hash.flatten())

	def __repr__(self):
		return repr(self.hash)

	def __sub__(self, other):
		# type: (ImageHash) -> int
		if other is None:
			raise TypeError('Other hash must not be None.')
		if self.hash.size != other.hash.size:
			raise TypeError('ImageHashes must be of the same shape.', self.hash.shape, other.hash.shape)
		return numpy.count_nonzero(self.hash.flatten() != other.hash.flatten())

	def __eq__(self, other):
		# type: (object) -> bool
		if other is None:
			return False
		return numpy.array_equal(self.hash.flatten(), other.hash.flatten())  # type: ignore

	def __ne__(self, other):
		# type: (object) -> bool
		if other is None:
			return False
		return not numpy.array_equal(self.hash.flatten(), other.hash.flatten())  # type: ignore

	def __hash__(self):
		# this returns a 8 bit integer, intentionally shortening the information
		return sum([2**(i % 8) for i, v in enumerate(self.hash.flatten()) if v])

	def __len__(self):
		# Returns the bit length of the hash
		return self.hash.size

def phash(image, hash_size=8, highfreq_factor=4):
	# type: (Image.Image, int, int) -> ImageHash
	"""
	Perceptual Hash computation.

	Implementation follows https://web.archive.org/web/20220504165254/https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html

	@image must be a PIL instance.
	"""
	if hash_size < 2:
		raise ValueError('Hash size must be greater than or equal to 2')

	import scipy.fftpack
	img_size = hash_size * highfreq_factor
	image = image.convert('L').resize((img_size, img_size), ANTIALIAS)
	pixels = numpy.asarray(image)
	dct = scipy.fftpack.dct(scipy.fftpack.dct(pixels, axis=0), axis=1)
	dctlowfreq = dct[:hash_size, :hash_size]
	med = numpy.median(dctlowfreq)
	diff = dctlowfreq > med
	return ImageHash(diff)

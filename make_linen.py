from numpy.random import rand, randn
from numpy import ones, zeros, shape
from matplotlib.pyplot import imsave, gray

import pdb

def add_fiber(mask, fiber, pos, horizontal=True):
	"""Add a fiber to mask (with wrap-around).
	
	Args:
		mask: image to add to
		fiber: fiber (1D array of intensitties)
		pos: [x, y] position within the image
		horizontal: set to False for vertical fibers
	"""
	[height, width] = shape(mask)
	fiber_len = len(fiber)
	if (horizontal):
		# diff = pos[0] + fiber_len - width
		# if (diff < 0):
			# diff = 0
		# pdb.set_trace()
		# mask[pos[1], pos[0]:pos[0] + fiber_len - diff] += fiber[:-diff]
		# mask[pos[1], 0:diff] += fiber[-diff:]
		if (width >= pos[0] + fiber_len):
			mask[pos[1], pos[0]:pos[0] + fiber_len] += fiber
		else:
			diff = pos[0] + fiber_len - width
			mask[pos[1], pos[0]:pos[0] + fiber_len - diff] += fiber[:-diff]
			mask[pos[1], 0:diff] += fiber[-diff:]
	else:
		if (height >= pos[1] + fiber_len):
			mask[pos[1]:pos[1] + fiber_len, pos[0]] += fiber
		else:
			diff = pos[1] + fiber_len - height
			mask[pos[1]:pos[1] + fiber_len-diff, pos[0]] += fiber[:-diff]
			mask[0:diff, pos[0]] += fiber[-diff:]


def add_fibers(mask, n_fibers=0, fiber_len = 150, fiber_opacity = 0.1, horizontal=True, opacities={}):
	"""Add the specified number of fibers into the given image."""
	[height, width] = shape(mask)

	for f in range(n_fibers):
		# randomize fiber length slightly
		fiber_len_r = int(fiber_len + randn()*fiber_len/5)
		
		# initialize the fiber
		fiber = ones(fiber_len_r)
		
		# modify the fiber so that it's strong (opaque) in the middle and 
		# fades off towards the edges
		if (not opacities.has_key(fiber_len_r)):
			opacities[fiber_len_r] = ones(fiber_len_r)
			for p in range(fiber_len_r):
				hl = round(fiber_len_r/2)
				opacities[fiber_len_r][p] = (hl - abs(hl - p))/hl
		# apply (slightly randomized) opacity
		fiber = fiber * opacities[fiber_len_r] * fiber_opacity * rand()
		
		# randomize position
		pos = [int(rand() * width), int(rand() * height)] # [x, y]
		
		add_fiber(mask, fiber, pos, horizontal)

	return mask


def make_linen(fiber_len=50, fiber_opacity=0.01, n_fibers=50000, base_intensity=0.1):
	"""Create linen texture image and save as linen.png

	Args
		fiber_len: average lenght of a single fiber
		fiber_opacity: average opacity of a single fiber
		n_fibers: number of fibers in each direction (horizontal and vertical)
		base_intensity: base intensity of the image before adding any fibers
	"""
	im_size = [900, 1440]

	im = ones(im_size) * base_intensity

	mask = zeros(im_size)
	mask = add_fibers(mask, n_fibers, fiber_len, fiber_opacity)
	mask = add_fibers(mask, n_fibers, fiber_len, fiber_opacity, horizontal=False)

	im += mask

	gray()
	imsave('linen.png', im, vmin=0.0, vmax=1.0)


if __name__ == "__main__":
	make_linen()	
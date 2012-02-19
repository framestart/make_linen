from numpy.random import rand, randn
from numpy import ones, zeros, shape
from matplotlib.pyplot import imsave, gray

''' adds a fiber with wrap-around '''
def add_fiber(mask, fiber, pos, horizontal=True):
	[height, width, depth] = shape(mask)
	fiber_len = len(fiber)
	if (horizontal):
		if (width >= pos[0] + fiber_len):
			for ch in range(depth):
				mask[pos[1], pos[0]:pos[0] + fiber_len, ch] += fiber
		else:
			diff = pos[0] + fiber_len - width
			for ch in range(depth):
				mask[pos[1], pos[0]:pos[0] + fiber_len - diff, ch] += fiber[:-diff]
				mask[pos[1], 0:diff, ch] += fiber[-diff:]
	else:
		if (height >= pos[1] + fiber_len):
			for ch in range(depth):
				mask[pos[1]:pos[1] + fiber_len, pos[0], ch] += fiber
		else:
			diff = pos[1] + fiber_len - height
			for ch in range(depth):
				mask[pos[1]:pos[1] + fiber_len-diff, pos[0], ch] += fiber[:-diff]
				mask[0:diff, pos[0], ch] += fiber[-diff:]


def add_fibers(mask, n_fibers=0, fiber_len = 150, fiber_opacity = 0.08, horizontal=True, opacities={}):
	[height, width, depth] = shape(mask)

	for f in range(n_fibers):
		fiber_len_r = int(fiber_len + randn()*fiber_len/5)
		pos_y = 0
		pos_x = 0
		if (horizontal):
			pos_y = int(rand() * height)
			pos_x = int(rand() * width)
		else:
			pos_y = int(rand() * height)
			pos_x = int(rand() * width)
		
		fiber = ones(fiber_len_r) * fiber_opacity
		if (not opacities.has_key(fiber_len_r)):
			opacities[fiber_len_r] = ones(fiber_len_r)
			for p in range(fiber_len_r):
				hl = round(fiber_len_r/2)
				opacities[fiber_len_r][p] = (hl - abs(hl - p))/hl

		fiber = fiber * opacities[fiber_len_r] * fiber_opacity * rand()
		add_fiber(mask, fiber, [pos_x, pos_y], horizontal)

	return mask

# linen parameters
fiber_len = 200			# average lenght of a single fiber
fiber_opacity = 0.06	# average fiber opacity
n_fibers = 50000		# number of horizontal/vertical fibers
base_intensity = 0.03	# base intensity of the image (before adding fibers)

im_size = [900, 1440, 1]

im = ones(im_size) * base_intensity

mask = zeros(im_size)
mask = add_fibers(mask, n_fibers, fiber_len)
mask = add_fibers(mask, n_fibers, fiber_len, horizontal=False)

mask = mask[:,:,0]

for ch in range(shape(im)[2]):
	im[:,:,ch] += mask

gray()
imsave('linen.png', im[:,:,0], vmin=0.0, vmax=1.0)
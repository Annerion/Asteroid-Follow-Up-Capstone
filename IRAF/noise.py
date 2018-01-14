from astropy.io import fits
from pyraf import iraf
import math
import random
import os
import numpy as np
import subprocess
aSize= 0.25 #angular size of a pixel 
source= fits.open('mystars_smeared_21.fits')
image= source[0]
height= image.data.shape[0]
width= image.data.shape[1]
time= 150 #observation duration
sky_mag=20 #magnitude of the sky per arcsec^2
sky_counts=(40.45*10**((20-sky_mag)/2.5))/(14.14)*time #counts of the sky per arcsec^2 over the duration of the exposure
sky_counts_pixel= sky_counts*(aSize**2)#counts of the sky per pixel over the duration of the exposure
temp= np.array([[np.random.poisson(sky_counts_pixel)+0.0 for x in range(width)] for y in range(height)])
for x in xrange(0,height):
	for y in xrange(0,width):
		temp[y][x]= image.data[y][x] + temp[y][x]
try:
	os.remove('test_noise_21.fits')
except OSError:
	pass
fits.writeto('test_noise_21.fits',temp)


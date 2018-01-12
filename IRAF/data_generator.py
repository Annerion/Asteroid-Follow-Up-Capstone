from astropy.io import fits
from pyraf import iraf
import math
import random
import os
import numpy as np
import subprocess
expansion_factor=2
aSize= 0.25 #angular size of a pixel 
aVelocity=20.0/50#angular speed of the source
pVelocity=aVelocity/aSize #pixels crossed per second
time= 150 #observation duration
angle= 0.523 #angle of movment in radians
default_m=22 #default magniutde ofthe source
sky_mag=20 #magnitude of the sky per arcsec^2
sky_counts=(40.45*10**((20-sky_mag)/2.5))/(14.14)*time #counts of the sky per arcsec^2 over the duration of the exposure
sky_counts_pixel= sky_counts*(aSize**2)#counts of the sky per pixel over the duration of the exposure
source= fits.open('mystars.fits')
image= source[0]
height= image.data.shape[0]*expansion_factor
width= image.data.shape[1]*expansion_factor
image.data= [[np.random.poisson(sky_counts_pixel)+0.0 for x in range(width)] for y in range(height)]
def magToCounts(m,t):
	return (40.45*10**((20-m)/2.5))/(14.14)*t
def clear():
	for y in range(0, height):
		for x in range(0, width):
			image.data[y][x]=0
def placeStar(A,s,x0,y0,cutoff=10):
#	print x0, y0
	for y in range(int(y0-cutoff*s), int(y0+cutoff*s)):
		for x in range(int(x0-cutoff*s), int(x0+cutoff*s)):
			if (0<=x<width) and (0<=y<height):
#				image.data[y][x]+=noise(int(A*math.exp(-1*((x-x0)**2+(y-y0)**2)/(2*s**2))))#noises here for now
				image.data[y][x]+=A*math.exp(-1*((x-x0)**2+(y-y0)**2)/(2*s**2))#if I need the version without noise
def makeField():
	stars= open("stars.txt",'r')
	star_list= []
	for line in stars:
		star_list.append(float(line))
	stars.close()
	for star in star_list:
		placeStar((40.45*10**((20-star)/2.5))/(14.14*pVelocity), 1.5, width*random.random(), height*random.random()) #no longer reduces amplitude scaled for expansion factor, as blkavg takes average
def makeSource(m=default_m):
	placeStar((40.45*10**((20-m)/2.5))/(14.14)*time, 1.5, width*random.random(), height*random.random()) #adds the source to the image, does not deal with the expansion factor, given a magnitude m
def save(i):
	if i==0:
		try:
			os.remove('mystars_smeared.fits')
		except OSError:
			pass
		fits.writeto('mystars_smeared.fits',image.data)
	else:
		try:
			os.remove('mystars_smeared_'+str(i)+'.fits')
		except OSError:
			pass
		fits.writeto('mystars_smeared_'+str(i)+'.fits',image.data)
def noise(i):
	return np.random.poisson(i)
def smear():
	steps= int(pVelocity*time*expansion_factor)
#	image.data/=steps
	for y in range(0, height-1):
		for x in range(0, width-1):
			for s in range(1,int(steps)):
				if (x+s<width) and (y+s<height):
					image.data[y][x]+=image.data[y+s*math.sin(angle)][x+s*math.cos(angle)]
def recondense():
	star_map= [[0.0] * int(width/expansion_factor) for i in range(int(height/expansion_factor))]
	for y in range(0, (height-1)/expansion_factor):
		for x in range(0, (width-1)/expansion_factor):
			for yp in range (y*expansion_factor, (y+1)*expansion_factor):
				for xp in range (x*expansion_factor, (x+1)*expansion_factor):
					if yp<height and xp<width:
						star_map[y][x]+=noise(image.data[yp][xp])
	image.data= star_map
def mkNoise():
	p=subprocess.Popen("cl")
	p.communicate("mknoise mystars_smeared.fits")
	p.communicate("log")
for i in xrange(2,3):
	makeField()
	smear()
	#recondense()
	#mkNoise()
	for n in xrange(0,50):
		makeSource(21)
	save(i)
	iraf.blkavg('mystars_smeared_'+str(i)+'.fits','mystars_smeared_'+str(i)+'.fits',expansion_factor,expansion_factor)
#iraf.mknoise('mystars_smeared.fits')

# this version creates a divide by zero error when loaded into ds9


from astropy.io import fits
import math
import random
import os
import numpy as np
expansion_factor=2
aSize= 1.212e-6
aVelocity= 1.212e-6
time= 50
angle= 0.523
source= fits.open('mystars.fits')
image= source[0]
height= image.data.shape[0]*expansion_factor
width= image.data.shape[1]*expansion_factor
image.data= [[0] * width for i in range(height)]
def clear():
	for y in range(0, height):
		for x in range(0, width):
			image.data[y][x]=0
def placeStar(A,s,x0,y0,cutoff=10):
	for y in range(int(y0-cutoff*s), int(y0+cutoff*s)):
		for x in range(int(x0-cutoff*s), int(x0+cutoff*s)):
			if (0<=x<width) and (0<=y<height):
				image.data[y][x]+=int(A*math.exp(-1*((x-x0)**2+(y-y0)**2)/(2*s**2)))
def makeField(count=100):
	for i in range(int(count)-1):
		placeStar(10000*random.random()/expansion_factor**2, 1.5*expansion_factor, width*random.random(), height*random.random())
def save():
	os.remove('mystars_smeared.fits')
	fits.writeto('mystars_smeared.fits',image.data)
def noise(i):
	return np.random.poisson(i)
def smear():
	steps= int(aVelocity*time/aSize*expansion_factor)
	image.data/=steps
	for y in range(0, height-1):
		for x in range(0, width-1):
			for s in range(1,int(steps)):
				if (x+s<width) and (y+s<height):
					image.data[y][x]+=image.data[y+s*math.sin(angle)][x+s*math.cos(angle)]
def recondense():
	star_map= [[1] * int(width/expansion_factor) for i in range(int(height/expansion_factor))]
	for y in range(0, (height-1)/expansion_factor):
		for x in range(0, (width-1)/expansion_factor):
			for yp in range (y*expansion_factor, (y+1)*expansion_factor):
				for xp in range (x*expansion_factor, (x+1)*expansion_factor):
					if yp<height and xp<width:
						star_map[y][x]+=noise(image.data[yp][xp])
	image.data= star_map
#clear()
makeField()
smear()
recondense()
save()

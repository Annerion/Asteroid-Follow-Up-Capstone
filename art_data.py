from astropy.io import fits
import math
import random
import os
source= fits.open('mystars.fits')
image= source[0]
height= image.data.shape[0]
width= image.data.shape[1]
def clear():
	for y in range(0, height):
		for x in range(0, width):
			image.data[y][x]=0.0001
def placeStar(A,s,x0,y0,cutoff=100):
	for y in range(int(y0-cutoff*s), int(y0+cutoff*s)):
		for x in range(int(x0-cutoff*s), int(x0+cutoff*s)):
			if (0<=x<width)&(0<=y<height):
				image.data[y][x]+=A*math.exp(-1*((x-x0)**2+(y-y0)**2)/(2*s**2))
def makeField(count=100):
	for i in range(int(count)-1):
		placeStar(1*random.random(), 3*random.random(), width*random.random(), height*random.random())
def save():
	os.remove('mystarsi.fits')
	fits.writeto('mystarsi.fits',image.data)
clear()
makeField()
save()

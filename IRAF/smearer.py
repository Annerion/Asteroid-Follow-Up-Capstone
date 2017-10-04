from astropy.io import fits
import math
source= fits.open('mystars.fits')
image= source[0]
height= image.data.shape[0]
width= image.data.shape[1]
aSize= 1.212e-6
aVelocity= 1.212e-6
time= 50
steps= aVelocity*time/aSize
print steps
angle= 0.523
image.data/=steps
for y in range(0, height-1):
	for x in range(0, width-1):
		for s in range(1,int(steps)):
			if (x+s<width)&(y+s<height):
				image.data[y][x]+=image.data[y+s*math.sin(angle)][x+s*math.cos(angle)]
destination= ('newmystars.fits')
image.writeto(destination)

import numpy as np
import sys
script= open("script.txt",'w')
fitsName= sys.argv[1]
threshStart= 0.5
threshEnd= 1.5
threshSteps= 6
dblendStart=0.001
dblendEnd=0.5
dbelndSteps= 6
threshSpace={0.5,0.7,0.9,1.1,1.3,1.5}
dblendSpace={0.001,0.005,0.01,0.05,0.1,0.5}
#for thresh in np.linspace(threshStart, threshEnd, threshSteps):
#	for dlbend in np.geomspace(dblendStart, dblendEnd, dblendSteps):
for thresh in threshSpace:
	for dblend in dblendSpace:
		script.write("sextractor "+fitsName+" -c config.txt -CATALOG_NAME= "+str(thresh)+"_"+str(dblend)+".cat -CHECKIMAGE_NAME= "+str(thresh)+"_"+str(dblend)+".obj.fits,"+str(thresh)+"_"+str(dblend)+".filt.fits,"+str(thresh)+"_"+str(dblend)+".seg.fits -DETECT_THRESH "+str(thresh)+" -ANALYSIS_THRESH "+str(thresh)+" -DEBLEND_MINCONT "+str(dblend)+"\n")
		#script.write("sudo sextractor "+fitsName+" -c config.txt -CATALOG_NAME= "+str(thresh)+"_"+str(dblend)+".cat -CHECKIMAGE_NAME= "+str(thresh)+"_"+str(dblend)+".obj.fits -DETECT_THRESH "+str(thresh)+" -ANALYSIS_THRESH "+str(thresh)+" -DEBLEND_MINCONT "+str(dblend)+"\n")
script.close()

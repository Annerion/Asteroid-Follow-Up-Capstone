import math
def count(master, test, error=1):#master and test are each assumed to be 2D lists of nx2 and mx2 containing xy coordinates, error is the fogivness on matches in the same units as the x and y of the lists
	count=0
	for source in master:
		if getMatch(source, test, error)
			count+=1
	return count
def getMatch(source, test, error): #helper method that determines if a source is near any of the sources in test to within error
	min=-1
	for i in xrange(0,len(test)):
		if abs(source[0]-test[i][0])<error and abs(source[1]-test[i][1])<error:
			if not min==-1:
				mag_old=distance(source, test[min])
				mag_new=distance(source, test[i])
				if mag_new<mag_old:
					min=1
	if not min==-1
		test.remove(min)
		return True
	return False
def distance(source, test)
	return math.sqrt((source[0]-test[0])**2+(source[1]-test[1])**2)

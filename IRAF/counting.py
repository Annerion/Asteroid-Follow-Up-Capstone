import math
import sys
def count(master, test, error=9):#master and test are each assumed to be 2D lists of nx2 and mx2 containing xy coordinates, error is the fogivness on matches in the same units as the x and y of the lists
	count=0
	for source in master:
		if getMatch(source, test, error):
			count+=1
	return count
def getMatch(source, test, error): #helper method that determines if a source is near any of the sources in test to within error
	min=-1
	for i in xrange(0,len(test)):
		if math.sqrt((source[0]-test[i][0])**2+(source[1]-test[i][1])**2)<error:
			if not min==-1:
				mag_old=distance(source, test[min])
				mag_new=distance(source, test[i])
				if mag_new<mag_old:
					min=i
			else:
				min=i
	if not min==-1:
		del test[min]
		return True
	return False
def distance(source, test):
	return math.sqrt((source[0]-test[0])**2+(source[1]-test[1])**2)
def getTestFromFile(file_name,x_index,y_index):
	data=open(file_name,'r')
	test=[]
	for line in data:
		temp=line.split()
		if not temp[0]=='#':
			test.append([float(temp[x_index]),float(temp[y_index])])
	return test
def getMasterFromFile(file_name):
	data=open(file_name,'r')
	source=[]
	for line in data:
		temp= line.split()
		source.append([float(temp[0]),float(temp[1])])
	return source
test= getTestFromFile(sys.argv[1],5,6)
master= getMasterFromFile('sourcelist.txt')
print "The number of sources (/50) detected is: "+str(count(master, test))+"\n"+"The total number of detections is: "+str(len(test))

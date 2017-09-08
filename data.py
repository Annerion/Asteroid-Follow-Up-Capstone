import urllib
import datetime
data= urllib.urlopen('http://www.minorplanetcenter.net/iau/NEO/neocp.txt').read()
date=datetime.date.today()
newFile= open("Desktop/DataCollection/"+"NEOdata."+str(date.year)+"."+str(date.month)+"."+str(date.day)+".txt",'w')
tempData= open("Desktop/DataCollection/"+"TempNEOdata.txt",'r+')
dataFile= open("Desktop/DataCollection/"+"NEOdataMaster.txt",'a')
newFile.write(data)
data= data.splitlines()
oldData= tempData.read().split("\n")
newData= []
for line in data:
	tempLine= line.split()
	checkData= tempLine[0]+" "+tempLine[8]+" "+tempLine[9]+" "+tempLine[10]+" "+tempLine[11]
	if checkData not in oldData:
		newData.append(checkData)
		dataFile.write(line+"\n")
tempData.write("\n".join(newData))
newFile.close
tempData.close
dataFile.close

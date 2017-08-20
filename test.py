import xlsxwriter
import urllib2

list = [1,2,3,4,5,6,7,8,9]

for x in list:
	print x



link = "http://www.ign.com/reviews/games"


f = urllib2.urlopen(link)
myfile = f.read()
print myfile



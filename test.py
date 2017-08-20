import xlsxwriter
import re
from urllib.request import Request, urlopen

list = [1,2,3,4,5,6,7,8,9]

for x in list:
	print(x)



#link = "http://www.metacritic.com/browse/games/release-date/available/ps4/date?page=0"

req = Request('http://www.metacritic.com/browse/games/release-date/available/ps4/date?page=0', headers={'User-Agent': 'Mozilla/5.0'})
#f = urllib.request.urlopen(link)
webpage = urlopen(req).read()
stringP = str(webpage) 
list = stringP.split("basic_stat product_title") #"<a href="

print (type(stringP))

del list[0]

del list[len(list)-1]

c = 0
b = False
for l in list:
	if b:
		c = c+1
	if len(l) >= 5000:
		c = c+1
		b = True 

print (c)

list = list[:len(list)-(c-1)]

#i = list[len(list)-1].index('"<div class="foot_wrap">\\n"')

list[len(list)-1] = list[len(list)-1][:1300]

#print (list[0])

'"<a href="/game/playstation-4/aca-neogeo-metal-slug-2">"'  
regex = r"([<][a][ ][h][r][e][f](.*)[n]([ ]){28}[\w])"
#mo = re.search(regex, list[0])
#print (mo) 
#print()
#print (mo.group())
#print (mo.start())
#print (mo.end())
#cutOff = mo.end()-1
#list[0] = list[0][cutOff:]
#print (list[0])


x = 0
#for l in list: 
#	print ("item")
#	print(x)
#	print(l) 
#	print()
#	x = x+1

print (len(list))


#myfile = f.read()
#print(webpage)
def findTitle(str):
	goal = ""
	for c in str:
		if c != "\\":
			goal=goal+c
		else:
			break
	return goal 

print(findTitle(list[0]))

#goal: make list of titles 


for l in list:
	mo = re.search(regex, l)
	#print (mo)
	cutOff = mo.end()-1
	l = l[cutOff:]
	print(findTitle(l)) #dope you found the titles! Add to tuple with score and date later 


	

	print()
	







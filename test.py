import xlsxwriter
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



x = 0
for l in list: 
	print ("item")
	print(x)
	print(l) 
	print()
	x = x+1

print (len(list))


#myfile = f.read()
#print(webpage)



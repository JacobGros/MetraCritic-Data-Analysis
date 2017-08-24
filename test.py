import xlsxwriter
import re
from urllib.request import Request, urlopen

list = [1,2,3,4,5,6,7,8,9]

for x in list:
	print(x)



req = Request('http://www.metacritic.com/browse/games/release-date/available/ps4/metascore?view=detailed', headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
stringP = str(webpage) 
list = stringP.split("basic_stat product_title") 

#print (type(stringP))

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

#print (c)

list = list[:len(list)-(c-1)]


list[len(list)-1] = list[len(list)-1][:1300]



print (len(list))


def findTitle(str):
	
	regex = r"([p][r][o][d][u][c][t][_][t][i][t][l][e][\"][>][<][a][ ][h][r][e][f](.*)[<][/][a][>][<][/][h])"
	mo  = re.search(regex, str)
	close = mo.group(1)
	close = close[:len(close)-7]
	regex2 = r"([>](?!<))"
	mo2 = re.search(regex2, close)
	
	goal = close[mo2.start()+1:]

	#goal = goal.

		 
	return goal.replace("\\","")



def findScore(str):
	regex = r"([\"][m][e][t][a][s][c][o][r][e](.*)[\"][>][0-9][0-9])"

	#game scored a 100
	regex2 = r"([\"][m][e][t][a][s][c][o][r][e](.*)[\"][>][1][0][0])"
	mo = re.search(regex, str)
	mo2 = re.search(regex2, str)

	if mo2:
		score = str[mo.end()-3:mo.end()]
		return int(score)


	score = str[mo.end()-2:mo.end()]
	return int(score)

def findDate(str):
	regex = r"([A-Z][a-z][a-z][ ][0-9]{1,2}[,][ ][0-9][0-9][0-9][0-9])"
	mo = re.search(regex, str)
	date = str[mo.start():mo.end()]

	return date


for l in list:
	
	print(findTitle(l)) 
	print (findScore(l))
	print (findDate(l))
	print()






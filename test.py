import xlsxwriter
import re
import datetime
import urllib.error
from urllib.request import Request, urlopen 
from decimal import Decimal

list = [1,2,3,4,5,6,7,8,9]

for x in list:
	print(x)

def findTitle(str):
	
	regex = r"([p][r][o][d][u][c][t][_][t][i][t][l][e][\"][>][<][a][ ][h][r][e][f](.*)[<][/][a][>][<][/][h])"
	mo  = re.search(regex, str)

	if mo == None:
		return "NULL"


	close = mo.group(1)
	close = close[:len(close)-7]
	regex2 = r"([>](?!<))"
	mo2 = re.search(regex2, close)
	
	goal = close[mo2.start()+1:]

	#goal = goal.

		 
	return goal.replace("\\","")



def findScore(str):
	#game scored in 10-99
	
	regex = r"([\"][m][e][t][a][s][c][o][r][e](.*)[\"][>][0-9][0-9][<][/][s][p][a][n][>][\\][n][<][/][a][>][<][/][d][i][v][>])"

	#game scored a 100
	regex2 = r"([\"][m][e][t][a][s][c][o][r][e](.*)[\"][>][1][0][0][<])"

	#game scored <10
	regex3 = r"([\"][m][e][t][a][s][c][o][r][e](.*)[n][e][g][a][t][i][v][e][\"][>][0-9][<])"


	mo = re.search(regex, str)
	mo2 = re.search(regex2, str)
	mo3 = mo2 = re.search(regex3, str)

	if mo3:
		score = str[mo.end()-2:mo.end()-1]
		return int(score)

	if mo2:
		score = str[mo.end()-4:mo.end()-1]
		return int(score)

	#score is TBA 

	if mo == None:
		return -1 

	score = str[mo.end()-21:mo.end()-19]
	return int(score)

def findDate(str):
	regex = r"([A-Z][a-z][a-z][ ][0-9]{1,2}[,][ ][0-9][0-9][0-9][0-9])"
	mo = re.search(regex, str)

	if mo == None:
		return ""

	date = str[mo.start():mo.end()]
    

	comma = date.index(",")
	
	day = date[4:comma]
	month = date[0:3]
	year = date[comma+2:]

	if month == "Jan":
		month = 1
	if month == "Feb":
		month = 2
	if month == "Mar":
		month = 3
	if month == "Apr":
		month = 4
	if month == "May":
		month = 5
	if month == "Jun":
		month = 6
	if month == "Jul":
		month = 7
	if month == "Aug":
		month = 8
	if month == "Sep":
		month = 9
	if month == "Oct":
		month = 10
	if month == "Nov":
		month = 11
	if month == "Dec":
		month = 12

	

	
	goal = datetime.datetime(int(year),int(month),int(day),0,0,0)

	

	return goal


def makeURLS(system):
	urls = []
	num =0
	url = 'http://www.metacritic.com/browse/games/score/metascore/all/'+ system + '/filtered?view=detailed&page=' + str(num)

	while num <31:
		#url = 'http://www.metacritic.com/browse/games/release-date/available/'+ system + '/metascore?view=detailed&page=' + str(num)
		url = 'http://www.metacritic.com/browse/games/score/metascore/all/'+ system + '/filtered?view=detailed&page=' + str(num)
		urls.append(url)
		num = num+1
	return urls


def makeList(url): 
	req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	webpage = urlopen(req).read()
	stringP = str(webpage) 
	list = stringP.split("basic_stat product_title") 
	
	del list[0]


	del list[len(list)-1]
	del list[len(list)-1]
	del list[len(list)-1]
	del list[len(list)-1]
	del list[len(list)-1]

	if len(list) != 0:
		del list[len(list)-1]
	 

	i=0
	while i<len(list):
		if len(list[i])>1300:
			list[i] = list[i][:1300]
		i = i+1


	return list


def findAverageScore(list):
	total = 0.0
	length = len(list)

	for l in list:
		total = total + l['Score']
	return round(total/length,0)

def findMaxScore(list):
	return max(list, key=lambda g: g['Score'])

def findMinScore(list):
	return min(list, key=lambda g: g['Score'])

def makeListOfTuples(system):
	urlList = makeURLS(system)



	games = []
	for url in urlList:
		list = makeList(url)
		#print (len(list))
		if len(list) < 10:
			break
		else:
			for l in list:
				game = {'Name' : findTitle(l), 'Score' : findScore(l), 'Date' : findDate(l)}
				if game['Score'] >= 0 and game['Date'] != "":
					games.append(game)

	sortedGames = sorted(games, key=lambda g: g['Date'])
	


	stat = {'System': system, 'Games' : sortedGames, 'Ave' : findAverageScore(sortedGames), 'Max' : findMaxScore(sortedGames), 'Min' : findMinScore(sortedGames) }

	return stat 

def makeSysDic(system):
	while True:
		try:
			stats = makeListOfTuples(system)
			return stats
		except (urllib.error.HTTPError,TimeoutError,urllib.error.URLError) as e:
			if e.code == 429:
				print ("Too many requests. Terminating")
				return -1
			print (" Error... retrying")
		except (urllib.error.URLError) as e2:
			print (" Error... retrying")



def driver():  

	stats = []


	systemList = ['ps4','xboxone', 'switch','ps3','xbox360','wii-u','wii','ps2','xbox','gamecube']

	for system in systemList:
		sysDic = makeSysDic(system)
		if sysDic != -1:
			stats.append(sysDic)
			message = "{} done".format(system)
			print(message)

	for s in stats:
		print(s) 


driver()

#NEXT ADD Write to Xcel method that takes a list of {System, {Game,Score,Date}, Max Min}

#for ps3       http://www.metacritic.com/browse/games/score/metascore/all/ps3/filtered?view=detailed&page=0
#for 360       http://www.metacritic.com/browse/games/score/metascore/all/xbox360/filtered?view=detailed&page=0
#for wii:      http://www.metacritic.com/browse/games/score/metascore/all/wii/filtered?view=detailed&page=0
#for wiiu:     http://www.metacritic.com/browse/games/score/metascore/all/wii-u/filtered?view=detailed&page=0
#for gamecube: http://www.metacritic.com/browse/games/score/metascore/all/gamecube/filtered?view=detailed&page=0 
#for ps2:      http://www.metacritic.com/browse/games/score/metascore/all/ps2/filtered?view=detailed&page=0
#for XBOX:     http://www.metacritic.com/browse/games/score/metascore/all/xbox/filtered?view=detailed&page=0
#for Switch:   http://www.metacritic.com/browse/games/score/metascore/all/switch/filtered?view=detailed&page=0

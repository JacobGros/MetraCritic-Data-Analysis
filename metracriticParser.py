import xlsxwriter
import re
import datetime
import urllib.error
from urllib.request import Request, urlopen 

#Finds title of the game, given a giant string of the game's info
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

		 
	return goal.replace("\\","")


#Finds score of the game, given a giant string of the games's info
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

#Finds release date of the game, given a giant string of the games's info
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

#Produces up to 31 pages to look through, this ensures all games on metracritic get looked at. 
def makeURLS(system):
	urls = []
	num =0
	url = 'http://www.metacritic.com/browse/games/score/metascore/all/'+ system + '/filtered?view=detailed&page=' + str(num)

	while num <31:
		url = 'http://www.metacritic.com/browse/games/score/metascore/all/'+ system + '/filtered?view=detailed&page=' + str(num)
		urls.append(url)
		num = num+1
	return urls

#Takes a webpage and splits it up into a list of giant strings for each game on the page. Possible glitch here, the last game for gamecube,ps2, and xbox 
#get ignored. 
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

#Caclulates the average score for the system 
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

#Makes Dic of stats including the system, the games (w/scores and dates), Max, and Min for the system
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
#This method calls makeListOfTuples, for each system, and provides some exception help 
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
#This method creates the list of Dics, given a system list. Right now its pre determined, but may allow for user input in later update
def driver():  

	stats = []


	systemList = ['ps4','xboxone', 'switch','ps3','xbox360','wii-u','wii','ps2','xbox','gamecube']
	#systemList = ['xboxone']

	for system in systemList:
		sysDic = makeSysDic(system)
		if sysDic != -1:
			stats.append(sysDic)
			message = "{} done".format(system)
			print(message)


	return stats 


#This creates a Dic detailing how many scores fell in range(0-9), (10-19), etc 
def groupScores(sysDic,goal):
	count =0
	for s in sysDic['Games']:
		#st = " {}/{} = {} and {}/10+1 = {}".format((s['Score']),goal,s['Score']/goal, goal, ((goal/10)+1) )
		#print(st)
		if s['Score']/10 >= goal/10 and s['Score']/10 < ((goal/10)+1):
			count = count+1
	return count 


#column can change, row follows same algorithim
#This helps the writeToExcel method for a given SysDic
def writeToExcelHelper(sysDic, ws, c,cf,chart,ws2):


	groupings = {'0-9s':groupScores(sysDic,1), '10-19s':groupScores(sysDic,10),'20-29s':groupScores(sysDic,20),'30-39s':groupScores(sysDic,30),'40-49s':groupScores(sysDic,40),'50-59s':groupScores(sysDic,50),'60-69s':groupScores(sysDic,60),'70-79s':groupScores(sysDic,70),'80-89s':groupScores(sysDic,80),'90-99s':groupScores(sysDic,90),'100s':groupScores(sysDic,100)}

	#print (groupings['0-9s'])
	#print (groupings['10-19s'])
	#print (groupings['20-29s'])
	#print (groupings['30-39s'])
	#print (groupings['40-49s'])
	#print (groupings['50-59s'])
	#print (groupings['60-69s'])
	#print (groupings['70-79s'])
	#print (groupings['80-89s'])
	#print (groupings['90-99s'])
	#print (groupings['100s'])



	ws.write(0, c-1, sysDic['System'].upper(),cf)

	ps = "{} Games in Range".format(sysDic['System'].upper())

	ws2.write(0, c, ps)


	ws.set_column(c-1, c-1, 49)

	ws.set_column(c+1, c+1, 9)

	ws2.set_column(0, 0, 20)

	ws2.set_column(c, c, 35)

	ws.write(2, c-2, 'Max:')
	ws.write(2, c-1, sysDic['Max']['Name'])
	ws.write(2, c, sysDic['Max']['Score'])
	ws.write(2, c+1, str(sysDic['Max'] ['Date'])[:11])


	ws.write(4, c-2, 'Min:')
	ws.write(4, c-1, sysDic['Min']['Name'])
	ws.write(4, c, sysDic['Min']['Score'])
	ws.write(4, c+1, str(sysDic['Min']['Date'])[:11])

	ws.write(6, c-1, "Ave:")
	ws.write(6, c, sysDic['Ave'])

	


	r=8
	for d in sysDic['Games']:
		ws.write(r, c-1, d['Name'])
		ws.write(r, c, d['Score'])
		ws.write(r, c+1, str(d['Date'])[:11])
		r = r+1


	r2 = 2
	for key, value in groupings.items():
		ws2.write(r2,c, value)
		r2 = r2+1

	
	chart.add_series({
    'categories': ['Sheet2', 4,0,r2,0],
    'values':     ['Sheet2', 4, c, r2, c],
    'name' :     sysDic['System'].upper()
    #'data_labels': {'value': False, 'position': 'inside_end'},
    #'line':       {'width': 5.00},

})





#This method writes the results to Excel 
def writeToExcel(list):




	name = input("What would you like to name your Excel file? ")
	workbook = xlsxwriter.Workbook(name+".xlsx")
	ws = workbook.add_worksheet()
	ws2 = workbook.add_worksheet()

	chart = workbook.add_chart({'type': 'column'})
	chart.set_size({'width': 1000, 'height': 1000})
	chart.set_title({'name': 'Systems\' Metracritic Scores'})
	chart.set_x_axis({'name': 'MetraCritic Score Range'})
	chart.set_y_axis({'name': 'Number of Games'})



	chartsheet = workbook.add_chartsheet()

	chartsheet.set_chart(chart)
	
	cell_format = workbook.add_format({'bold': True})

	r =2
	ws2.write(0,0, "MetraCritic Score Range")
	for x in range(0,10):

		s = "{}-{}".format((x*10),(x*10)+9)
		ws2.write(r,0,s)
		r = r+1
	ws2.write(r,0,100)

	
	c =2
	for l in list:
		writeToExcelHelper(l, ws, c, cell_format,chart,ws2)
		c = c+6




	workbook.close()
	m = "Excel sheet is done and saved under {}.xlsx".format(name)
	print (m)
#This call right here does everything 
writeToExcel(driver())



#for ps3       http://www.metacritic.com/browse/games/score/metascore/all/ps3/filtered?view=detailed&page=0
#for 360       http://www.metacritic.com/browse/games/score/metascore/all/xbox360/filtered?view=detailed&page=0
#for wii:      http://www.metacritic.com/browse/games/score/metascore/all/wii/filtered?view=detailed&page=0
#for wiiu:     http://www.metacritic.com/browse/games/score/metascore/all/wii-u/filtered?view=detailed&page=0
#for gamecube: http://www.metacritic.com/browse/games/score/metascore/all/gamecube/filtered?view=detailed&page=0 
#for ps2:      http://www.metacritic.com/browse/games/score/metascore/all/ps2/filtered?view=detailed&page=0
#for XBOX:     http://www.metacritic.com/browse/games/score/metascore/all/xbox/filtered?view=detailed&page=0
#for Switch:   http://www.metacritic.com/browse/games/score/metascore/all/switch/filtered?view=detailed&page=0

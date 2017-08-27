# MetraCritic-Data-Analysis
This code goes through MetaCritic for each system and collects data based off each system's games' scores.
This allows for comparisons like which system has the most games scoring 90+, which has the least? 

First it gets the webpage and converts it into a list. Each element in this list is a hunk of info about a particular game.

Regex are used to find title,score, and date, given one element of the above list. This gets put in a dictionary. This dictionary for a
single game is then added to a list of dictionaries, with each dictionary representing one game. 

Given the game dictionaries for each system, the ave score, max score, and min score are all recorded and added to another Dictionary.
This Dictionary is refered to as sysDic, because it contains all the info needed for write to Excel. 
It contains {'System', 'Games'(list of game dics), 'Max','Min','Ave'}

The results are all written to Excel, and system groupings are calculated. A grouping is a number of games that fall into the range 
of scores. For example '20-29' is a grouping, and it corresponds to the number of games that recieved a score in that range. 
All these groupings are put into a dictionary {'0-9','10-19'.....'90-99','100'}, and these are the result of what is graphed. 

I originally atempted to graph every single game score with its date released, but graphing thousands of points became sloppy
and unreadable. 


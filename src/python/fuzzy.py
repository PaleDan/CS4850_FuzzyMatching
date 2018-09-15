import binarySearchTree
import Levenshtein
import random
from datetime import datetime
#using https://pypi.org/project/python-Levenshtein/0.12.0/
#installed from https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-levenshtein

def search() :
	filename = ''
	searchstring = ''
	
	print('enter the database filename')
	filename = input('>')
	print('\nenter the search filename')
	searchfile = input('>')
	
	file = open(filename)
	searchlist = file.readlines()
	file.close()
	
	file = open(searchfile)
	searchstring = file.read()
	file.close()

	tree = binarySearchTree.Tree()
	
	for i in range(len(searchlist)) :
		distance = Levenshtein.distance(searchstring, searchlist[i])
		tree.insert(distance, i)
		print(searchlist[i] + ' (distance: ' + str(distance) + ')')
	
	topten = tree.get(10)
	print('\ntop ten: (' + str(len(topten)) + ')')
	for i in range(len(topten)) :
		print(str(i+1) + ': ' + searchlist[topten[i].val] + ' (distance: ' + str(topten[i].key) + ')')
#
def timedSearch() :
	for i in range(100) :
		print(datetime.now().time())
#

def treetest() :
	tree = binarySearchTree.Tree()
	max = 1000000
	for i in range(max) :
		randint = random.randint(0,max)
		tree.insert(randint, None)
	topten = tree.get(10)
	print('\ntop ' + str(len(topten)) + ' (of ' + str(max) + ') :')
	for i in range(len(topten)) :
		print(str(i) + ': ' + str(topten[i].key))

#


timedSearch()
import binarySearchTree
import Levenshtein
import random
#using https://pypi.org/project/python-Levenshtein/0.12.0/
#installed from https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-levenshtein

def search() :
	filename = ''
	searchstring = ''
	
	print('enter the filename')
	filename = input('>')
	print('\nenter the search term')
	searchstring = input('>')
	
	file = open(filename)
	searchlist = file.readlines()
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

def test() :
	tree = binarySearchTree.Tree()
	for i in range(15) :
		randint = random.randint(0,200)
		tree.insert(randint, 'x')
		print(randint)
	topten = tree.get(10)
	print('\ntop ten: (' + str(len(topten)) + ')')
	for i in range(len(topten)) :
		print(str(i) + ': ' + str(topten[i].key))

#


search()
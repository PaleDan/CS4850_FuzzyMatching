import binarySearchTree
import Levenshtein
import random
from multiprocessing import Process, Manager
import sys
import time
#using https://pypi.org/project/python-Levenshtein/0.12.0/
#installed from https://www.lfd.uci.edu/~gohlke/pythonlibs/#python-levenshtein

def search() :
	filename = ''
	searchstring = ''
	
	print('enter the database filename')
	filename = input('>')
	print('\nenter the search filename')
	searchfile = input('>')
	
	print('loading...', end='')
	file = open(filename)
	searchlist = file.read().splitlines()
	file.close()
		
	file = open(searchfile)
	searchstring = file.read()
	file.close()
	print('done. (' + str(len(searchlist)) + ')')

	tree = binarySearchTree.Tree()
	
	print("beginning search...")
	begintime = time.process_time()
	
	for i in range(len(searchlist)) :
		ratio = 1 - Levenshtein.ratio(searchstring, searchlist[i])
		tree.insert(ratio, i)
		
	endtime = time.process_time()
	print("finished search. runtime: " + str(endtime - begintime) + " (" + str(endtime) + " - " + str(begintime) + ")")

	
	topten = tree.get(10)
	print('\ntop ten: (' + str(len(topten)) + ')')
	for i in range(len(topten)) :
		print(str(i+1) + ': ' + searchlist[topten[i].val] + ' (ratio: ' + str(1 - topten[i].key) + ')')

def multiSearch(t) :
	print("multiSearch(" + str(t) + ")")
	global nextLock
	global searchlist
	filename = ''
	if t > 0 :
		threadcount = t
	else :
		threadcount = 1
	nextLock = Lock()
	#treeLock = Lock()
	
	print('enter the database filename')
	filename = input('>')
	print('\nenter the search filename')
	searchfile = input('>')
	
	searchlist = []

	print('loading...', end='')
	file = open(filename)
	searchlist = file.read().splitlines()
	file.close()
		
	file = open(searchfile)
	searchstring = file.read()
	file.close()
	print('done. (' + str(len(searchlist)) + ')')

	tree = binarySearchTree.Tree()
	
	threads = []
	
	distances = []
	values = []
	for i in range(threadcount) :
		distances.append(Value('i', 0))
		values.append(searchlist.pop())
	
	print("beginning search...")
	begintime = time.process_time()

	
	for i in range(threadcount) :
		p = Process(target=levenshteinThread, args=(searchstring, values[i], distances[i]))
		threads.append(p)
		p.start()
	
	currentthread = 0
	while len(searchlist) > 0 :
		if not threads[currentthread].is_alive() :
			tree.insert(distances[currentthread].value, values[currentthread])
			values[currentthread] = searchlist.pop()
			#distances[currentthread] = Value('i', 0)
			threads[currentthread] = Process(target=levenshteinThread, args=(searchstring, values[currentthread], distances[currentthread]))
			threads[currentthread].start()
		currentthread = currentthread + 1
		if currentthread >= len(threads) :
			currentthread = 0
		
	for i in range(threadcount) :
		threads[i].join()
		tree.insert(distances[i].value, values[i])
		

	endtime = time.process_time()
	print("finished search. runtime: " + str(endtime - begintime) + " (" + str(endtime) + " - " + str(begintime) + ")")

	topten = tree.get(10)
	print('\ntop ten: (' + str(len(topten)) + ')')
	for i in range(len(topten)) :
		print(str(i+1) + ': ' + topten[i].val + ' (distance: ' + str(topten[i].key) + ')')

def levenshteinThread(searchstring, record, distance) :
	distance.value = Levenshtein.distance(searchstring, record)
	return 

def dbSearch(db1, db2, min, threadcount) :	
	threads = []
	manager = Manager()
	lists = []
	step = int(len(db1) / threadcount)
	initial = 0
	for i in range(threadcount) :
		end = step * (i+1)
		lists.append(manager.list())
		threads.append(Process(target=dbSearchProcess, args=(db1[initial:end], db2, lists[i], min, initial)))
		threads[i].start()
		initial = end
	
	for i in range(len(threads)) :
		threads[i].join()
	
	return lists

def dbSearchProcess(db1, db2, list, min, initial) :
	templist = []
	print(len(db1))
	for j in range(len(db1)) :
		jlist = []
		for i in range(len(db2)) :
			ratio = Levenshtein.ratio(db1[j], db2[i])
			if ratio >= min :
				jlist.append( [ratio, j + initial, i] )

		jlist.sort(key=lambda x: x[0], reverse=True)
		for i in range(len(jlist)) :
			templist.append(jlist[i])
	list.append(templist)

def startSearch(threadcount, min) :
	print('enter the first database filename')
	db1 = input('>')
	
	print('loading...', end='', flush=True)
	file = open(db1)
	db1 = file.read().splitlines()
	file.close()
	print('done. (' + str(len(db1)) + ')')
	
	print('enter the second database filename')
	db2 = input('>')
	
	print('loading...', end='', flush=True)
	file = open(db2)
	db2 = file.read().splitlines()
	file.close()
	print('done. (' + str(len(db2)) + ')')

	begintime = time.time()

	lists = dbSearch(db1, db2, min, threadcount)

	endtime = time.time()

	results = []
	for i in range(len(lists)) :
		for j in range(len(lists[i])) :
			results = results + lists[i][j]

	print("done.")
	for i in range(len(results)) :
		if len(results[i]) > 0 :
			print('[' + str(i) + '](' + str(results[i][0]) + '):', '[' + str(db1[results[i][1]]) + ']', '[' + str(db2[results[i][2]]) + ']' )
		else :
			print('[' + str(i) + '](-1):>NO MATCH')
	print("finished search. runtime: " + str(endtime - begintime) + " (" + str(endtime) + " - " + str(begintime) + ")")

def getNext() :
	global nextLock
	with nextLock :
		global searchlist
		if len(searchlist) > 0 :
			return searchlist.pop()
		else :
			return False

def addToTree(distance, value) :
	global treeLock
	with treeLock :
		tree.insert(distance, value)

def treeTest() :
	tree = binarySearchTree.Tree()
	max = 1000000
	for i in range(max) :
		randint = random.randint(0,max)
		tree.insert(randint, None)
	topten = tree.get(10)
	print('\ntop ' + str(len(topten)) + ' (of ' + str(max) + ') :')
	for i in range(len(topten)) :
		print(str(i) + ': ' + str(topten[i].key))

def timeTest() :
	for i in range(1000) :
		print(time.process_time())



if __name__ == '__main__':
	fuzzy = sys.modules[__name__]
	commands = ['help']
	dashcommands = ['t', 'm']
	threads = 4
	method = 0
	minimum = 0.6
	help = False
	if len(sys.argv) > 1 :
		for i in range(1, len(sys.argv)) :
			if sys.argv[i] in commands :
				if sys.argv[i] == commands[0] :
					help = True
			elif sys.argv[i][0] == '-' and sys.argv[i][1:] in dashcommands and len(sys.argv) > i + 1 :
				if sys.argv[i][1:] == dashcommands[0] :
					threads = int(sys.argv[i+1])
					i = i + 1
				if sys.argv[i][1:] == dashcommands[1] :
					minimum = int(sys.argv[i+1])
					i = i + 1
			elif hasattr(fuzzy, sys.argv[i]) :
				method = getattr(fuzzy, sys.argv[i])
		if help :
			print("-t [number]  - specifies number of threads to use in multisearch\nsearch       - specifies to use the single-threaded search function")
		elif not method == 0 :
			method(threads)
		else :
			startSearch(threads, minimum)
	else :
		startSearch(threads, minimum)

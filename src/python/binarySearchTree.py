class Node:
	def __init__(self, parent, key, val):
		self.key = key
		self.val = val
		self.leftChild = None
		self.rightChild = None
		self.parent = parent
	
	def get(self):
		return self.val
		
	def getKey(self):
		return self.key
	
	def set(self, val):
		self.val = val
		
	def getChildren(self):
		children = []
		if(self.leftChild != None):
			children.append(self.leftChild)
		if(self.rightChild != None):
			children.append(self.rightChild)
		return children
		
	def get(self, count):
		returnlist = []
		if count > 0  and self.leftChild != None :
			left = self.leftChild.get(count)
			returnlist.extend(left)
			count = count - len(left)
		if count > 0 :
			returnlist.append(self)
			count = count - 1
		if count > 0 and self.rightChild != None :
			right = self.rightChild.get(count)
			returnlist.extend(right)
			count = count - len(right)
		return returnlist
		
	
	
	def getLeftmost(self):
		root = self
		while root.leftChild != None :
			root = root.leftChild
		return root

class Tree:
	def __init__(self):
		self.root = None

	def setRoot(self, key, val):
		self.root = Node(None, key, val)

	def insert(self, key, val):
		if(self.root is None):
			self.setRoot(key, val)
		else:
			self.insertNode(self.root, key, val)
			
	def get(self, count):
		return self.root.get(count)
	
	def insertNode(self, currentNode, key, val):
		if(key <= currentNode.key):
			if(currentNode.leftChild):
				self.insertNode(currentNode.leftChild, key, val)
			else:
				currentNode.leftChild = Node(currentNode, key, val)
		elif(key > currentNode.key):
			if(currentNode.rightChild):
				self.insertNode(currentNode.rightChild, key, val)
			else:
				currentNode.rightChild = Node(currentNode, key, val)

	def find(self, val):
		return self.findNode(self.root, val)

	def findNode(self, currentNode, val):
		if(currentNode is None):
			return False
		elif(val == currentNode.val):
			return True
		elif(val < currentNode.val):
			return self.findNode(currentNode.leftChild, val)
		else:
			return self.findNode(currentNode.rightChild, val)
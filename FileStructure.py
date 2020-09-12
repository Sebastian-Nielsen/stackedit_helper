from typing import List, Set


class Node:
	def __init__(self, title: str, type="folder", parent = None, children: Set = set()):
		"""
		:param type: Whether it's a file or a folder
		"""
		self.title = title
		self.type = type
		self.parent = parent
		self.children = children
		assert(children == set())

	def addChildren(self, children: 'List[Node]'):
		self.children = self.children.union(children)

	def __str__(self):
		return self.title

	def __eq__(self, other):
		if isinstance(other, Node):
			return (self.title == other.title) and (self.type == other.type) and \
						 (self.parent.title == other.parent.title)
		return False

	def __hash__(self):
		if self.parent:
			return hash((self.title, self.type, self.parent.title))
		return hash((self.title, self.type, None))

	def __repr__(self):
		# return f"{self.type}({self.title}, parent={self.parent}, chhildren={self.children})"
		return self.title

class FileStructure:
	def __init__(self, root = None):
		self.root = root
		self.deepestChildren = []
		# Dict from node-names to Node objects
		self.__nameToNode = {}

	def addNode(self, node: Node):
		if self.root is None:
			if node.type == "folder":
				self.root = node
			else:
				raise Exception("Root node should be a folder")

		self.__nameToNode[str(node)] = node

	def generatePathToNode(self, node: Node) -> str:
		"""
		Generates the path given a node. E.g. given node 'ai-notes' instance,
		generates: 'Personal website/ai-notes'
		"""
		crnt_node = node
		rtrn_str = str(node)
		while crnt_node.parent:
			rtrn_str = f"{crnt_node.parent}/{rtrn_str}"
			crnt_node = crnt_node.parent
		return rtrn_str

	def addChildrenToNode(self, nodeTitle: str, children: List[Node]):
		"""
		:param node: Node to add children to
		:param children: Children to add to the node
		"""
		pNode = self.getNodeByTitle(nodeTitle)

		for cNode in children:
			# Add the node to the fileStructure dict
			self.addNode(cNode)
			# Set the parent pointer of each child node
			cNode.parent = pNode

		pNode.addChildren(set(children))

	def getNodeByTitle(self, title: str) -> Node:
		return self.__nameToNode[title]

	def increaseDepth(self):
		"""Now adds nodes to the filestructure one more depth down"""
		self.deepestChildren = []

	def getFileStructureFromNodeAndBeyond(self, node: Node) -> str:
		string = str(node)
		for child in node.children:
			string += f"-{self.getFileStructureFromNodeAndBeyond(child)}"


	def __str__(self):
		"""returns a str representation of the filestructure"""
		return self.getFileStructureFromNodeAndBeyond(self.root)


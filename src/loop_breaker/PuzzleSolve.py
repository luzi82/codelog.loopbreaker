import copy

class PuzzleSolve:

	def __init__(self,puzzle):
		self.puzzle = puzzle

		self.yMax = self.puzzle["height"]
		self.xMax = self.puzzle["width"]
		self.yMax2 = self.yMax+2
		self.xMax2 = self.xMax+2

		cell2LL = []
		for y2 in xrange(self.yMax2):
			cell2L = []
			for x2 in xrange(self.xMax2):
				x=x2-1
				y=y2-1
				if(x>=0) and (x<self.xMax) and (y>=0) and (y<self.yMax):
					cell2L.append({
						"x":x,"y":y,"x2":x2,"y2":y2,
						"v":puzzle["cellListList"][y][x],"done":False,"ans":0
					})
				else:
					cell2L.append({
						"x":None,"y":None,"x2":x2,"y2":y2,
						"v":0,"done":True,"ans":0
					})
			cell2LL.append(cell2L)

		dirtyDoneL=[]
		
		for cell2L in cell2LL:
			for cell2 in cell2L:
				if((cell2["v"]==0)or(cell2["v"]==15)):
					cell2["done"]=True
				if cell2["done"]:
					dirtyDoneL.append(cell2)
		
		self.undoneL = [{"cell2LL":cell2LL,"dirtyDoneL":dirtyDoneL}]
		self.doneL = []

	def calc(self):

		while len(self.undoneL)>0:
			undone = self.undoneL[0]
			cell2LL = undone["cell2LL"]
			dirtyDoneL = undone["dirtyDoneL"]

			good = True

			while True:
				#print("vkJqlhcq len(dirtyDoneL) "+str(len(dirtyDoneL)))
				#print("mUXQsVqW dirtyDoneL "+str(dirtyDoneL))
				#print("jGoPBPqc cell2LL "+str(cell2LL))
				if len(dirtyDoneL)==0:
					break
				dirtyDone = dirtyDoneL[0]
				good = good and self.tryFill(undone,dirtyDone["x2"]-1,dirtyDone["y2"])
				good = good and self.tryFill(undone,dirtyDone["x2"]+1,dirtyDone["y2"])
				good = good and self.tryFill(undone,dirtyDone["x2"],dirtyDone["y2"]-1)
				good = good and self.tryFill(undone,dirtyDone["x2"],dirtyDone["y2"]+1)
				if not good:
					break
				dirtyDoneL.pop(0)

			if not good:
				#print("mMjFDAlv diver kill")
				self.undoneL.pop(0)
				continue

			undoneCell = None
			for y2 in xrange(self.yMax2):
				for x2 in xrange(self.xMax2):
					if cell2LL[y2][x2]["done"]:
						continue
					undoneCell = cell2LL[y2][x2]
					break
			if undoneCell == None:
				#print("cHPgseBp diver ok")
				self.doneL.append(undone)
				self.undoneL.pop(0)
				continue

			choiceL = self.getChoiceL(cell2LL,undoneCell)
			
			for choice in choiceL:
				newUndone = copy.deepcopy(undone)
				newCell = newUndone["cell2LL"][undoneCell["y2"]][undoneCell["x2"]]
				newCell["v"]=choice["v"]
				newCell["ans"]=choice["ans"]
				newCell["done"]=True
				newUndone["dirtyDoneL"].append(newCell)
				self.undoneL.append(newUndone)
			
			self.undoneL.pop(0)
			
			#print("GAzwIZpb diver found")

		self.ansLLL = []
		for done in self.doneL:
			ansLL = [[0 for x in xrange(self.xMax)] for x in xrange(self.yMax)]
			cell2LL = done["cell2LL"]
			for cell2L in cell2LL:
				for cell2 in cell2L:
					if (cell2["y"]!=None) and (cell2["x"]!=None):
						ansLL[cell2["y"]][cell2["x"]]=cell2["ans"]
			self.ansLLL.append(ansLL)

	def tryFill(self,undone,x2,y2):
	
		if x2<0:
			return True
		if y2<0:
			return True
		if x2>=self.xMax2:
			return True
		if y2>=self.yMax2:
			return True
			
		#print("WtGLobPm tryFill "+str(x2)+" "+str(y2))

		cell2LL = undone["cell2LL"]
		if cell2LL[y2][x2]["done"]:
			return True

		cell = cell2LL[y2][x2]
		choiceL = self.getChoiceL(cell2LL,cell)
		if len(choiceL) == 0:
			return False
		if len(choiceL) > 1:
			return True

		#print("vRgmZcwf fill")
		cell["v"] = choiceL[0]["v"]
		cell["ans"] = choiceL[0]["ans"]
		cell["done"]=True
		
		undone["dirtyDoneL"].append(cell)
		
		return True

	def getChoiceL(self,cell2LL,cell):

		cellNotDone=0
		cellSet=0
		x2 = cell["x2"]
		y2 = cell["y2"]

		c = cell2LL[y2-1][x2]
		if c["done"]:
			cellSet|=((c["v"]>>2)&1)<<0
		else:
			cellNotDone|=1<<0

		c = cell2LL[y2][x2+1]
		if c["done"]:
			cellSet|=((c["v"]>>3)&1)<<1
		else:
			cellNotDone|=1<<1

		c = cell2LL[y2+1][x2]
		if c["done"]:
			cellSet|=((c["v"]>>0)&1)<<2
		else:
			cellNotDone|=1<<2

		c = cell2LL[y2][x2-1]
		if c["done"]:
			cellSet|=((c["v"]>>1)&1)<<3
		else:
			cellNotDone|=1<<3

		if cellNotDone == 15:
			return True
					
		vv = cell["v"]
		ans = 0
		okList = []

		while True:
			vvv = ( ( ~ ( vv ^ cellSet ) ) | cellNotDone )
			vvv &= 15
			if vvv == 15:
				okList.append({"ans":ans,"v":vv})
			vv <<= 1
			vv |= (vv>>4)
			vv &= 15
			ans = ans+1
			if vv == cell["v"]:
				break

		return okList

import cv2
from itertools import product
import copy

class LoopBreakerContext:

	def __init__(self):
		pass

	def setPuzzleImageOriginal(self,filename):
		self.image_ori = self.processImage(cv2.imread(filename))

	def getBorderTestClickList(self):
		ret = []
		
		imgHeight, imgWidth = self.image_ori.shape[:2]
		offset=5

		for y,x in product(xrange(imgHeight),xrange(imgWidth)):
			if(self.image_ori[y,x]>=0x7f):
				ret.append({"x":x+offset,"y":y+offset})
				break

		for x,y in product(reversed(xrange(imgWidth)),xrange(imgHeight)):
			if(self.image_ori[y,x]>=0x7f):
				ret.append({"x":x-offset,"y":y+offset})
				break

		for y,x in product(reversed(xrange(imgHeight)),xrange(imgWidth)):
			if(self.image_ori[y,x]>=0x7f):
				ret.append({"x":x+offset,"y":y-offset})
				break

		for x,y in product(xrange(imgWidth),xrange(imgHeight)):
			if(self.image_ori[y,x]>=0x7f):
				ret.append({"x":x+offset,"y":y+offset})
				break

		return ret

	def setBorderTestClickImage(self, imageListList):

		borderList=[]
		
		for imageList in imageListList:
			tmp0 = None
			for image in imageList:
				tmp1 = self.processImage(cv2.imread(image))
				tmp1 = cv2.bitwise_xor(self.image_ori,tmp1)
				if tmp0 == None:
					tmp0 = tmp1
				else:
					tmp0 = cv2.bitwise_or(tmp0,tmp1)
			border = self.detectBorder(tmp0)
			borderList.append(border)

		self.x0=borderList[3]["x0"]
		self.y0=borderList[0]["y0"]
		self.x1=borderList[1]["x1"]
		self.y1=borderList[2]["y1"]
		self.cellW=borderList[0]["x1"]-borderList[0]["x0"]
		self.cellH=borderList[0]["y1"]-borderList[0]["y0"]
		
		self.puzzleWidth=(self.x1-self.x0+(self.cellW/2))/self.cellW
		self.puzzleHeight=(self.y1-self.y0+(self.cellH/2))/self.cellH

		self.cellXList=[]
		self.cellXmList=[]
		for xx in xrange(self.puzzleWidth):
			tmp = (self.x0*(self.puzzleWidth-xx)+self.x1*xx)/self.puzzleWidth
			self.cellXList.append(tmp)
			self.cellXmList.append(tmp+self.cellW/2)
		self.cellYList=[]
		self.cellYmList=[]
		for yy in xrange(self.puzzleHeight):
			tmp = (self.y0*(self.puzzleHeight-yy)+self.y1*yy)/self.puzzleHeight
			self.cellYList.append(tmp)
			self.cellYmList.append(tmp+self.cellH/2)
		
		self.puzzle={}
		self.puzzle["width"]=self.puzzleWidth
		self.puzzle["height"]=self.puzzleHeight
		self.puzzle["cellListList"]=[]
		for yy in xrange(self.puzzleHeight):
			cellList=[]
			for xx in xrange(self.puzzleWidth):
				cellDetectPointList = self.getCellDetectPointList(xx,yy)
				v=0
				u=1
				for cellDetectPoint in cellDetectPointList:
					if self.image_ori[cellDetectPoint["y"],cellDetectPoint["x"]] >= 0x7f:
						v |= u
					u <<= 1
				cellList.append(v)
			self.puzzle["cellListList"].append(cellList)
		
		self.puzzle["solutionList"] = self.solvePuzzle(self.puzzle)
	
	def getPuzzle(self):
		return self.puzzle

	def getCellDetectPointList(self,xx,yy):
		x0 = self.cellXList[xx]
		y0 = self.cellYList[yy]
		x1 = x0 + self.cellW
		y1 = y0 + self.cellH
		
		xm = x0 + self.cellW/2
		ym = y0 + self.cellH/2
		xd = self.cellW/16
		yd = self.cellH/16
		
		return[
			{"x":xm,"y":y0+yd},
			{"x":x1-xd,"y":ym},
			{"x":xm,"y":y1-yd},
			{"x":x0+xd,"y":ym}
		]

	def getSolutionClickStepList(self):
		ret = []
		for iLL in self.puzzle["solutionList"]:
			oLL = []
			for yy in xrange(self.puzzleHeight):
				for xx in xrange(self.puzzleWidth):
					if iLL[yy][xx] == 0:
						continue
					oLL.append({
						"x":self.cellXmList[xx],
						"y":self.cellYmList[yy],
						"count":iLL[yy][xx]
					})
			ret.append(oLL)
		return ret

	@staticmethod
	def processImage(image):
		ret = image
		ret = cv2.cvtColor(ret, cv2.COLOR_BGR2GRAY)
		_,ret = cv2.threshold(ret, 164, 255, cv2.THRESH_BINARY_INV)
		
		return ret

	@staticmethod
	def showImage(image):
		cv2.imshow('image',image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		print(ret)

	@staticmethod
	def detectBorder(image):
		ret={}

		imgHeight, imgWidth = image.shape[:2]
	
		for y,x in product(xrange(imgHeight),xrange(imgWidth)):
			if(image[y,x]>=0x7f):
				ret["y0"]=y
				break

		for x,y in product(xrange(imgWidth),xrange(imgHeight)):
			if(image[y,x]>=0x7f):
				ret["x0"]=x
				break

		for x,y in product(reversed(xrange(imgWidth)),xrange(imgHeight)):
			if(image[y,x]>=0x7f):
				ret["x1"]=x
				break

		for y,x in product(reversed(xrange(imgHeight)),xrange(imgWidth)):
			if(image[y,x]>=0x7f):
				ret["y1"]=y
				break

		return ret

	@staticmethod
	def solvePuzzle(puzzle):
	
		hh = puzzle["height"]+2
		ww = puzzle["width"]+2
		
		pLL = []
		for yy in xrange(hh):
			pL = []
			for xx in xrange(ww):
				xxx=xx-1
				yyy=yy-1
				if(xxx>=0) and (xxx<puzzle["width"]) and (yyy>=0) and (yyy<puzzle["height"]):
					pL.append({
						"x":xxx,"y":yyy,
						"v":puzzle["cellListList"][yyy][xxx],"done":False,"ans":0
					})
				else:
					pL.append({
						"x":None,"y":None,
						"v":0,"done":True,"ans":0
					})
			pLL.append(pL)
		
		for pL in pLL:
			for p in pL:
				if((p["v"]==0)or(p["v"]==15)):
					p["done"]=True
		
		undoneLLL = [pLL]
		doneLLL = []
		while len(undoneLLL)>0:
			pLL = undoneLLL[0]
			allDone = True
			for pL in pLL:
				for p in pL:
					allDone &= p["done"]
			if allDone:
				doneLLL.append(pLL)
				undoneLLL.pop(0)
				continue

			action = False
			bad = False
			diverX=None
			diverY=None
			diverOkList=None
			for yy in xrange(hh):
				for xx in xrange(ww):
					if pLL[yy][xx]["done"]:
						continue
					cellNotDone=0
					cellSet=0
					
					pp = pLL[yy-1][xx]
					if pp["done"]:
						cellSet|=((pp["v"]>>2)&1)<<0
					else:
						cellNotDone|=1<<0

					pp = pLL[yy][xx+1]
					if pp["done"]:
						cellSet|=((pp["v"]>>3)&1)<<1
					else:
						cellNotDone|=1<<1

					pp = pLL[yy+1][xx]
					if pp["done"]:
						cellSet|=((pp["v"]>>0)&1)<<2
					else:
						cellNotDone|=1<<2

					pp = pLL[yy][xx-1]
					if pp["done"]:
						cellSet|=((pp["v"]>>1)&1)<<3
					else:
						cellNotDone|=1<<3
					
					if cellNotDone == 15:
						continue
					
					pp = pLL[yy][xx]
					vv = pp["v"]
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
						if vv == pp["v"]:
							break
					if len(okList) == 1:
						pp["v"]=okList[0]["v"]
						pp["ans"]=okList[0]["ans"]
						pp["done"]=True
						action = True
					elif len(okList) == 0:
						bad = True
						break
					elif (not action) and (diverOkList==None):
						diverX = xx
						diverY = yy
						diverOkList = okList
				if bad:
					break
			
			if bad:
				undoneLLL.pop(0)
				continue
				
			if action:
				continue

			for diverOk in diverOkList:
				newPLL = copy.deepcopy(pLL)
				newP = newPLL[diverY][diverX]
				newP["v"]=diverOk["v"]
				newP["ans"]=diverOk["ans"]
				newP["done"]=True
				undoneLLL.append(newPLL)
			
			undoneLLL.pop(0)

		ret = []
		for doneLL in doneLLL:
			pLL = [[0 for x in xrange(puzzle["width"])] for x in xrange(puzzle["height"])]
			for doneL in doneLL:
				for done in doneL:
					if (done["y"]!=None) and (done["x"]!=None):
						pLL[done["y"]][done["x"]]=done["ans"]
			ret.append(pLL)

		return ret

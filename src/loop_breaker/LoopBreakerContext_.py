import cv2
from itertools import product
import PuzzleSolve

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
		borderImg=[]
		
		for imageList in imageListList:
			tmp0 = None
			for image in imageList:
				tmp1 = self.processImage(cv2.imread(image))
				tmp1 = cv2.bitwise_xor(self.image_ori,tmp1)
				if tmp0 == None:
					tmp0 = tmp1
				else:
					tmp0 = cv2.bitwise_or(tmp0,tmp1)
			borderImg.append(tmp0)

		borderList.append(self.detectBorder(borderImg[0],["y0","y1"]))
		borderList.append(self.detectBorder(borderImg[1],["x0","x1"]))
		borderList.append(self.detectBorder(borderImg[2],["y1"]))
		borderList.append(self.detectBorder(borderImg[3],["x0"]))

		self.x0=borderList[3]["x0"]
		self.y0=borderList[0]["y0"]
		self.x1=borderList[1]["x1"]
		self.y1=borderList[2]["y1"]
		self.cellW=borderList[1]["x1"]-borderList[1]["x0"]
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
	
	def solve(self):
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
	def detectBorder(image,interestL):
		ret={}

		imgHeight, imgWidth = image.shape[:2]
	
		if "y0" in interestL:
			for y in xrange(imgHeight):
				if cv2.countNonZero(image[y:y+1,:])>0:
					ret["y0"]=y
					break

		if "x0" in interestL:
			for x in xrange(imgWidth):
				if cv2.countNonZero(image[:,x:x+1])>0:
					ret["x0"]=x
					break

		if "x1" in interestL:
			for x in reversed(xrange(imgWidth)):
				if cv2.countNonZero(image[:,x:x+1])>0:
					ret["x1"]=x
					break

		if "y1" in interestL:
			for y in reversed(xrange(imgHeight)):
				if cv2.countNonZero(image[y:y+1,:])>0:
					ret["y1"]=y
					break

		return ret

	@staticmethod
	def solvePuzzle(puzzle):

		p = PuzzleSolve.PuzzleSolve(puzzle)
		p.calc()
		return p.ansLLL

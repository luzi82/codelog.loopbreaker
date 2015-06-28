from os.path import dirname
import sys
import time
import os
import loop_breaker

adb_exe="3rdparty/android-sdk-linux/platform-tools/adb"
device_tmp="/storage/sdcard1/tmp"

def getScreenshot(filename):
	os.system("rm -f "+filename)
	os.system(adb_exe+" shell screencap -p "+device_tmp+"/screen.png")
	os.system(adb_exe+" pull "+device_tmp+"/screen.png "+filename)
	os.system(adb_exe+" shell rm "+device_tmp+"/screen.png")

def click(x,y):
	os.system(adb_exe+" shell input tap "+str(x)+" "+str(y))

if __name__ == '__main__':
	os.system("mkdir -p /tmp/LoopBreaker")
	while True:
		lbl = loop_breaker.LoopBreakerContext()
		
		getScreenshot("/tmp/LoopBreaker/ori.png")
		lbl.setPuzzleImageOriginal("/tmp/LoopBreaker/ori.png")

		borderTestClickList = lbl.getBorderTestClickList()
		borderTestClickImageLL = []
		for i in xrange(len(borderTestClickList)):
			borderTestClick=borderTestClickList[i]
			borderTestClickImageL=[]
			for j in xrange(3):
				click(borderTestClick["x"],borderTestClick["y"])
				filename = "/tmp/LoopBreaker/border"+str(i)+"-"+str(j)+".png"
				getScreenshot(filename)
				borderTestClickImageL.append(filename)
			click(borderTestClick["x"],borderTestClick["y"])
			borderTestClickImageLL.append(borderTestClickImageL)

		lbl.setBorderTestClickImage(borderTestClickImageLL)

		print(lbl.getPuzzle())
		
		clickStepList = lbl.getSolutionClickStepList()
		
		if len(clickStepList) == 0:
			break
		
		for step in clickStepList[0]:
			for c in xrange(step["count"]):
				click(step["x"],step["y"])
		
		time.sleep(3)
		click(100,100)
		time.sleep(5)

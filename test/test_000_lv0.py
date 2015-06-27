from os.path import dirname
import sys
sys.path.append(dirname(dirname(__file__))+"/src")

TEST_PATH=dirname(__file__)

import unittest
import loop_breaker

class Test000(unittest.TestCase):

	def test_analyze(self):
		
		lbl = loop_breaker.LoopBreakerContext()
		
		lbl.setPuzzleImageOriginal(TEST_PATH+"/res/lv00000000-ori.png")
		
		tmp = lbl.getBorderTestClickList()
		self.assertEqual(len(tmp),4)
		self.assertTrue(tmp[0]["y"]>=544)
		self.assertTrue(tmp[0]["y"]<=570)
		self.assertTrue(tmp[1]["x"]>=420)
		self.assertTrue(tmp[1]["x"]<=461)
		self.assertTrue(tmp[2]["y"]>=700)
		self.assertTrue(tmp[2]["y"]<=735)
		self.assertTrue(tmp[3]["x"]>=258)
		self.assertTrue(tmp[3]["x"]<=300)
		
		lbl.setBorderTestClickImage([
			[
				TEST_PATH+"/res/lv00000000-0-1.png",
				TEST_PATH+"/res/lv00000000-0-2.png",
				TEST_PATH+"/res/lv00000000-0-3.png"
			],
			[
				TEST_PATH+"/res/lv00000000-1-1.png",
				TEST_PATH+"/res/lv00000000-1-2.png",
				TEST_PATH+"/res/lv00000000-1-3.png"
			],
			[
				TEST_PATH+"/res/lv00000000-2-1.png",
				TEST_PATH+"/res/lv00000000-2-2.png",
				TEST_PATH+"/res/lv00000000-2-3.png"
			],
			[
				TEST_PATH+"/res/lv00000000-3-1.png",
				TEST_PATH+"/res/lv00000000-3-2.png",
				TEST_PATH+"/res/lv00000000-3-3.png"
			]
		]);

		tmp = lbl.getPuzzle()
		self.assertEqual(tmp["width"],3)
		self.assertEqual(tmp["height"],2)
		self.assertEqual(tmp["cellListList"],[
			[3,14,12],
			[3,11,12]
		])
		self.assertEqual(tmp["solutionList"],[[
			[1,0,0],
			[0,0,1]
		]])
		
		tmp = lbl.getSolutionClickStepList()
		self.assertEqual(len(tmp),1)
		self.assertTrue(tmp[0][0]["x"]>=216)
		self.assertTrue(tmp[0][0]["x"]<=311)
		self.assertTrue(tmp[0][0]["y"]>=544)
		self.assertTrue(tmp[0][0]["y"]<=639)
		self.assertEqual(tmp[0][0]["count"],1)
		self.assertTrue(tmp[0][1]["x"]>=407)
		self.assertTrue(tmp[0][1]["x"]<=503)
		self.assertTrue(tmp[0][1]["y"]>=640)
		self.assertTrue(tmp[0][1]["y"]<=735)
		self.assertEqual(tmp[0][1]["count"],1)

if __name__ == '__main__':
	unittest.main()

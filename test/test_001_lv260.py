from os.path import dirname
import sys
sys.path.append(dirname(dirname(__file__))+"/src")

TEST_PATH=dirname(__file__)

import unittest
import loop_breaker

class Test001(unittest.TestCase):

	def test_analyze(self):
		
		lbl = loop_breaker.LoopBreakerContext()
		
		lbl.setPuzzleImageOriginal(TEST_PATH+"/res/lv00000260-ori.png")
		
		lbl.setBorderTestClickImage([
			[
				TEST_PATH+"/res/lv00000260-0-1.png",
				TEST_PATH+"/res/lv00000260-0-2.png",
				TEST_PATH+"/res/lv00000260-0-3.png"
			],
			[
				TEST_PATH+"/res/lv00000260-1-1.png",
				TEST_PATH+"/res/lv00000260-1-2.png",
				TEST_PATH+"/res/lv00000260-1-3.png"
			],
			[
				TEST_PATH+"/res/lv00000260-2-1.png",
				TEST_PATH+"/res/lv00000260-2-2.png",
				TEST_PATH+"/res/lv00000260-2-3.png"
			],
			[
				TEST_PATH+"/res/lv00000260-0-1.png",
				TEST_PATH+"/res/lv00000260-0-2.png",
				TEST_PATH+"/res/lv00000260-0-3.png"
			]
		]);

		lbl.solve()
		tmp = lbl.getPuzzle()
		self.assertEqual(len(tmp["solutionList"]),2)
		
		tmp = lbl.getSolutionClickStepList()
		self.assertEqual(len(tmp),2)

if __name__ == '__main__':
	unittest.main()

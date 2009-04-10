# -*- coding: utf-8 -*-
#
#  test_comb.py
#  simplestats
# 
#  Created by Lars Yencken on 10-04-2009.
#  Copyright 2009 Lars Yencken. All rights reserved.
#

import sys, unittest
import doctest

import comb

def suite():
    testSuite = unittest.TestSuite((
            unittest.makeSuite(CombinationTest),
            doctest.DocTestSuite(comb),
        ))
    return testSuite

#----------------------------------------------------------------------------#

class CombinationTest(unittest.TestCase):
    def setUp(self):
        self.dataA = [1,2,3]

    def testCombinations(self):
        self.assertEqual(comb.combinations(self.dataA, self.dataA),
                [(1,1),(2,1),(3,1),(1,2),(2,2),(3,2),(1,3),(2,3),(3,3)])
        return

    def testICombinations(self):
        self.assertEqual(list(comb.icombinations(self.dataA, self.dataA)),
                [(1,1),(2,1),(3,1),(1,2),(2,2),(3,2),(1,3),(2,3),(3,3)])

        return

    def testUniqueTuples(self):
        self.assertEqual(comb.unique_tuples([1,2]), [(1,2)])
        self.assertEqual(comb.unique_tuples([1,2,3]), [(1,2), (1,3), (2,3)])

        return

    def testInclusionCombination(self):
        self.assertEqual(
                set(map(tuple, comb.inclusion_combinations([1,2]))),
                set(map(tuple, [[], [1], [2], [1,2]])),
            )
        self.assertEqual(comb.inclusion_combinations([]), [[]])
        return

    def testIUniqueTuples(self):
        self.assertEqual(list(comb.iunique_tuples([1,2])), [(1,2)])
        self.assertEqual(list(comb.iunique_tuples([1,2,3])), [(1,2), (1,3),
                (2,3)])

        return

    def testSegmentCombinations(self):
        result = set([('d', 'o', 'g'), ('do', 'g'), ('d', 'og'), ('dog',)])
        self.assertEqual(
                set(comb.segment_combinations(['d', 'o', 'g'])),
                result
            )
        self.assertEqual(
                set(comb.isegment_combinations(['d', 'o', 'g'])),
                result
            )

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())


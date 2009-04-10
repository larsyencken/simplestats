# -*- coding: utf-8 -*-
#
#  test_aggregate.py
#  simplestats
# 
#  Created by Lars Yencken on 10-04-2009.
#  Copyright 2009 Lars Yencken. All rights reserved.
#

import sys, unittest
import doctest

import aggregate

#----------------------------------------------------------------------------#

def suite():
    testSuite = unittest.TestSuite((
            unittest.makeSuite(AggregateTestCase),
        ))
    return testSuite

#----------------------------------------------------------------------------#

class AggregateTestCase(unittest.TestCase):
    def setUp(self):
        return

    def testBinsByData(self):
        """
        Tests splitting data into bins.
        """
        data = [3,2,5,1,7,3,0]

        expectedLabels = [(0,3), (3,5), (5,7)]
        expectedBins = [[0,1,2], [3,3], [5,7]]

        self.assertEqual(
                list(aggregate.bins_by_data(data, 3)),
                zip(expectedLabels, expectedBins)
            )

        return

    def testBinsByRange(self):
        """
        Tests splitting data into bins.
        """
        data = [3,2,5,1,9,3,0]

        expectedLabels = [(0.0,3.0), (3.0,6.0), (6.0,9.0)]
        expectedBins = [[0,1,2], [3,3,5], [9]]

        self.assertEqual(
                list(aggregate.bins_by_range(data, 3, lambda x: x)),
                zip(expectedLabels, expectedBins)
            )

        return

    def testBinsByInc(self):
        """
        Tests splitting data into bins.
        """
        data = [3,2,5,1,8,3,0]

        expectedLabels = [(0.0,3.0), (3.0,6.0), (6.0,9.0)]
        expectedBins = [[0,1,2], [3,3,5], [8]]

        self.assertEqual(
                list(aggregate.bins_by_increment(data, 3.0, lambda x: x)),
                zip(expectedLabels, expectedBins)
            )

        data = [3,2,5,1,9,3,0]

        expectedLabels = [(0.0,3.0), (3.0,6.0), (6.0,9.0), (9.0, 12.0)]
        expectedBins = [[0,1,2], [3,3,5], [], [9]]

        self.assertEqual(
                list(aggregate.bins_by_increment(data, 3.0, lambda x: x)),
                zip(expectedLabels, expectedBins)
            )

        return


    def tearDown(self):
        pass

#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())


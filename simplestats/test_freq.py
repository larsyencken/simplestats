# -*- coding: utf-8 -*-
#
#  test_freq.py
#  simplestats
#

import unittest
import doctest

import freq


def suite():
    testSuite = unittest.TestSuite((
        unittest.makeSuite(FreqDistTestCase),
        unittest.makeSuite(CondFreqDistTestCase),
        doctest.DocTestSuite(freq),
    ))
    return testSuite


class FreqDistTestCase(unittest.TestCase):
    def testBasic(self):
        x = freq.FreqDist()
        x.inc('dog')
        self.assertEqual(x.candidates(), [('dog', 0.0)])
        self.assertEqual(x.prob('dog'), 1.0)
        x.inc('cat')
        self.assertEqual(x.prob('dog'), 0.5)
        self.assertEqual(x.prob('cat'), 0.5)


class CondFreqDistTestCase(unittest.TestCase):
    def setUp(self):
        model = freq.ConditionalFreqDist()
        model.inc('Breakfast', 'Cereal')
        model.inc('Breakfast', 'Toast')
        model.inc('Lunch', 'Sandwich')
        model.inc('Dinner', 'Spaghetti', 2)
        model.inc('Dinner', 'Stir-fry')
        self.model = model

    def test_dist(self):
        model = self.model
        self.assertEqual(
            set(model.candidates('Breakfast')),
            set([('Cereal', -0.69314718055994529),
                 ('Toast', -0.69314718055994529)])
        )
        self.assertEqual(
            set(model.candidates('Dinner')),
            set([('Spaghetti', -0.40546510810816444),
                 ('Stir-fry', -1.0986122886681098)])
        )
        self.assertEqual(
            set(model.candidates('Lunch')),
            set([('Sandwich', 0.0)]),
        )

    def testDerivativeDists(self):
        "Tests to_condition_dist() and to_sample_dist() methods."
        condition_dist = self.model.to_condition_dist()
        self.assertEqual(condition_dist._total, 6)
        self.assertEqual(condition_dist.prob('Dinner'), (3.0/6.0))
        self.assertEqual(condition_dist.prob('Lunch'), (1.0/6.0))
        self.assertEqual(condition_dist.prob('Breakfast'), (2.0/6.0))

        sample_dist = self.model.to_sample_dist()
        self.assertEqual(sample_dist._total, 6)
        self.assertEqual(sample_dist.prob('Spaghetti'), (2.0/6.0))
        self.assertEqual(sample_dist.prob('Stir-fry'), (1.0/6.0))
        self.assertEqual(sample_dist.prob('Sandwich'), (1.0/6.0))
        self.assertEqual(sample_dist.prob('Cereal'), (1.0/6.0))
        self.assertEqual(sample_dist.prob('Toast'), (1.0/6.0))


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())

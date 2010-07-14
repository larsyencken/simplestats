# -*- coding: utf-8 -*-
#
#  comb.py
#  simplestats
# 
#  Created by Lars Yencken on 10-04-2009.
#  Copyright 2009 Lars Yencken. All rights reserved.
#

"""
Combinations and permuatations of items.
"""

from itertools import ifilter
import warnings
import sys

class deprecated(object):
    def __init__(self, py_version, module_and_method):
        self.py_version = py_version
        self.module_and_method = module_and_method

    def __call__(self, f):
        def g(*args, **kwargs):
            if sys.version_info >= self.py_version:
                warnings.warn(
                    "method %s() can be replaced by %s() in Python "
                    "%d.%d and above" % (f.__name__, self.module_and_method,
                    self.py_version[0], self.py_version[1])
                )
            return f(*args, **kwargs)
        g.__name__ = f.__name__
        g.__doc__ = f.__doc__

        return g

@deprecated((2, 6), 'itertools.product')
def combinations(*combination_list):
    """
    Generates a list of all possible combinations of one element from the
    first item in combination_list, one from the second, etc. For example::

        >>> combinations([1, 2], ['dog'], ['a', 'b'])
        [(1, 'dog', 'a'), (2, 'dog', 'a'), (1, 'dog', 'b'), (2, 'dog', 'b')]
    """
    combination_list = list(combination_list[:])
    combination_list.reverse()

    first_list = combination_list.pop()
    combos = map(lambda x: (x,), first_list)

    while combination_list:
        next_level_combos = []
        for item_to_add in combination_list.pop():
            # add this item to the end of every existing combo 
            for existing_combo in combos:
                next_level_combos.append(existing_combo + (item_to_add,))

        combos = next_level_combos

    return combos

#----------------------------------------------------------------------------#

def iunique_pairs(input_list):
    return UniquePairsIterator(input_list)

class UniquePairsIterator(object):
    """
    An interator over pairings which also has a length method.

    >>> x = UniquePairsIterator([1, 2, 3])
    >>> len(x)
    3
    >>> list(x)
    [(1, 2), (1, 3), (2, 3)]
    """
    def __init__(self, input_list):
        self.i = 0
        self.j = 1
        self.input_list = sorted(input_list)
        self.list_len = len(input_list)

        if self.list_len < 2:
            raise ValueError, "input must be of length at least 2"

    def next(self):
        if self.i == self.list_len - 1 and self.j >= self.list_len:
            raise StopIteration

        item = self.input_list[self.i], self.input_list[self.j]
        self.j += 1
        if self.j >= self.list_len:
            self.i += 1
            self.j = self.i + 1

        return item

    def __len__(self):
        return self.list_len * (self.list_len - 1) / 2

    def __iter__(self):
        return self

    def __repr__(self):
        return '<UniquePairsIterator: %d items>' % len(self)

#----------------------------------------------------------------------------#

@deprecated((2, 6), 'itertools.combinations')
def unique_tuples(input_list, n=2):
    "Similar to combinations, but selects from the same list."
    def filter_fn(x):
        for i in xrange(n-1):
            if x[i] >= x[i+1]:
                return False
        else:
            return True

    return filter(filter_fn, combinations(*(n*[input_list])))

#----------------------------------------------------------------------------#

@deprecated((2, 6), 'itertools.combinations')
def iunique_tuples(input_list, n=2):
    "An iterator version of unique_tuples."
    def filter_fn(x):
        for i in xrange(n-1):
            if x[i] >= x[i+1]:
                return False
        else:
            return True

    return ifilter(filter_fn, icombinations(*(n*[input_list])))

#----------------------------------------------------------------------------#

@deprecated((2, 6), 'itertools.product')
def icombinations(*combination_lists):
    """
    As for combinations(), but returns an iterator.
    """
    combination_lists = map(list, combination_lists)
    lengths = map(len, combination_lists)
    combined = zip(combination_lists, lengths)
    n_combs = reduce(lambda x, y: x*y, lengths)

    for i in xrange(n_combs):
        item = ()
        for item_list, list_length in combined:
            i, offset = divmod(i, list_length)
            item += (item_list[offset],)
        yield item

#----------------------------------------------------------------------------#

def combination_seqs(*combination_list):
    """
    As with combinations() above, except that each potential item is
    assumed to already be in sequence form. For example::

        >>> combination_seqs([(1, 2), (3, 4)], [('dog',), ('cat',)])
        [(1, 2, 'dog'), (3, 4, 'dog'), (1, 2, 'cat'), (3, 4, 'cat')]
    """
    return list(icombination_seqs(*combination_list))

#----------------------------------------------------------------------------#

def icombination_seqs(*combination_lists):
    """
    As for combinations(), but returns an iterator.

        >>> list(icombination_seqs([(1, 2), (3, 4)], [('dog',), ('cat',)]))
        [(1, 2, 'dog'), (3, 4, 'dog'), (1, 2, 'cat'), (3, 4, 'cat')]
    """
    for seq_combs in icombinations(*combination_lists):
        result = []
        for seq in seq_combs:
            result.extend(seq)
        yield tuple(result)

#----------------------------------------------------------------------------#

def segment_combinations(g_string):    
    """
    Determines the possible segment combinations based on the grapheme
    string alone, in particular due to kanji placement. For example::

        >>> segment_combinations('ab')
        [('a', 'b'), ('ab',)]
    
    """
    # start out with just the first character
    segmentations = [[g_string[0]]]

    # add remaining characters one by one
    for char in g_string[1:]: 
        next_segmentation_round = []
        for segment in segmentations:
            # the new char in its own segment
            next_segmentation_round.append(segment + [char])

            # the new char as part of the previous segment
            segment[-1] += char
            next_segmentation_round.append(segment)

        segmentations = next_segmentation_round
    
    segmentations = map(tuple, segmentations)

    return segmentations

#----------------------------------------------------------------------------#

def isegment_combinations(g_string):
    """
    As for segment_combinations(), but returns an iterator.

        >>> list(sorted(isegment_combinations('ab')))
        [('a', 'b'), ('ab',)]

    Note that the order may be different.
    """
    if not g_string:
        return

    g_string_size = len(g_string)
    n_combs = 2**(g_string_size-1)

    for i in xrange(n_combs):
        current_comb = [g_string[0]]
        for j in xrange(1,g_string_size):
            i, has_boundary = divmod(i, 2)
            if has_boundary:
                current_comb.append(g_string[j])
            else:
                current_comb[-1] += g_string[j]
        yield tuple(current_comb)

    return

#----------------------------------------------------------------------------#

def inclusion_combinations(sequence):
    """
    Returns a list of all combinations of inclusion/exclusion of the
    elements of the given sequence.

    >>> inclusion_combinations([])
    [[]]
    >>> inclusion_combinations([1, 2])
    [[], [1], [2], [1, 2]]
    """
    current_combs = [[]]
    for element in sequence:
        next_set = []
        for comb in current_combs:
            next_set.append(comb + [element])

        current_combs += next_set

    return current_combs

# vim: ts=4 sw=4 sts=4 et tw=78:

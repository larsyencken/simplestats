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

import itertools

def combinations(*combination_list):
    """
    Generates a list of all possible combinations of one element from the
    first item in combination_list, one from the second, etc. For example::

        >>> combinations([1, 2], ['dog'], ['a', 'b'])
        [(1, 'dog', 'a'), (1, 'dog', 'b'), (2, 'dog', 'a'), (2, 'dog', 'b')]
    """
    return list(itertools.product(*combination_list))

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
        self.input_list = input_list
        list_len = len(input_list)
        if list_len == 0:
            self.size = 0
        elif list_len == 1:
            self.size = 1
        else:
            self.size = list_len * (list_len - 1) / 2

    def __iter__(self):
        for v in itertools.combinations(self.input_list, 2):
            yield v

    def __len__(self):
        return self.size

    def __repr__(self):
        return '<UniquePairsIterator: %d items>' % len(self)

#----------------------------------------------------------------------------#

def unique_tuples(input_list, n=2):
    "Similar to combinations, but selects from the same list."
    return list(itertools.combinations(input_list, n))

#----------------------------------------------------------------------------#

def iunique_tuples(input_list, n=2):
    "An iterator version of unique_tuples."
    return itertools.combinations(input_list, n)

#----------------------------------------------------------------------------#

def icombinations(*combination_lists):
    """
    As for combinations(), but returns an iterator.
    """
    return itertools.product(*combination_lists)

#----------------------------------------------------------------------------#

def combination_seqs(*combination_list):
    """
    As with combinations() above, except that each potential item is
    assumed to already be in sequence form. For example::

        >>> combination_seqs([(1, 2), (3, 4)], [('dog',), ('cat',)])
        [(1, 2, 'dog'), (1, 2, 'cat'), (3, 4, 'dog'), (3, 4, 'cat')]
    """
    return list(icombination_seqs(*combination_list))

#----------------------------------------------------------------------------#

def icombination_seqs(*combination_lists):
    """
    As for combinations(), but returns an iterator.

        >>> list(icombination_seqs([(1, 2), (3, 4)], [('dog',), ('cat',)]))
        [(1, 2, 'dog'), (1, 2, 'cat'), (3, 4, 'dog'), (3, 4, 'cat')]
    """
    for seq_combs in icombinations(*combination_lists):
        result = []
        for seq in seq_combs:
            result.extend(seq)
        yield tuple(result)
    return

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

# -*- coding: utf-8 -*-
#
#  freq.py
#  simplestats
# 
#  Created by Lars Yencken on 10-04-2009.
#  Copyright 2009 Lars Yencken. All rights reserved.
#

"A simple frequency distribution, modelled after that in NLTK."

#----------------------------------------------------------------------------#

import sys
import bz2
import gzip
import codecs

from math import log

#----------------------------------------------------------------------------#

class FreqDist(dict):
    """
    A simple frequency distribution, and some methods to access MLE
    probability estimations based on this distribution.

        >>> x = FreqDist()
        >>> x.prob('unknown')
        0.0
        >>> x.inc('a', 3)
        >>> x.inc('b')
        >>> x.prob('a')
        0.75
        >>> x.prob('b')
        0.25
        >>> x.prob('unknown')
        0.0
    """
    #------------------------------------------------------------------------#
    # PUBLIC METHODS
    #------------------------------------------------------------------------#

    def __init__(self, pairSeq=None):
        """
        Constructor. Can optionally be given a sequence of (sample, count)
        pairs to load counts from.
        """
        self._total = 0

        if pairSeq is not None:
            for sample, count in pairSeq:
                self[sample] = count
                self._total += count
        return

    #------------------------------------------------------------------------#

    def total():
        doc = "The total count."
        def fget(self):
            return self._total
        return locals()
    total = property(**total())

    #------------------------------------------------------------------------#

    def inc(self, sample, n=1):
        """Add one to the count for this sample."""
        self.__setitem__(sample, self.get(sample, 0) + n)
        self._total += n
        return

    #------------------------------------------------------------------------#

    def decrement(self, sample, n=1):
        """Remove one to the count for this sample."""
        count = self[sample]
        
        if count < n:
            raise ValueError, "Can't reduce a count below zero"
        elif count == n:
            # If we reduce a count to zero, delete it.
            self._total -= n
            del self[sample]
        else:
            # Reduce it by the given amount only.
            self._total -= n
            self[sample] -= n

        return

    #------------------------------------------------------------------------#

    def remove_sample(self, sample):
        """
        Removes the sample and its count from the distribution. Returns
        the count of the sample.
        """
        count = self[sample]
        del self[sample]
        self._total -= count

        return count

    #------------------------------------------------------------------------#

    def count(self, sample):
        """Return the frequency count of the sample."""
        return self.get(sample, 0)

    #------------------------------------------------------------------------#

    def prob(self, sample):
        """Returns the MLE probability of this sample."""
        c = self.get(sample, 0)
        if c > 0:
            return c / float(self._total)
        else:
            return 0.0

    #------------------------------------------------------------------------#

    def log_prob(self, sample):
        """Returns the log MLE probability of this sample."""
        return log(self.get(sample, 0) / float(self._total))

    #------------------------------------------------------------------------#

    def candidates(self):
        """
        Returns a list of (sample, log_prob) pairs, using the log MLE
        probability of each sample.
        """
        return [
                (k, log(v/float(self._total))) \
                for (k, v) \
                in self.iteritems()
            ]

    #------------------------------------------------------------------------#

    def dump(self, filename):
        """
        Dump the current counts to the given filename. Note that symbols
        are coerced to strings, so arbitrary objects may not be
        reconstructed identically.
        """
        o_stream = sopen(filename, 'w')
        for key, count in sorted(self.iteritems(), key=lambda x: x[1],  
                reverse=True):
            key = _escape_spaces(unicode(key))
            print >> o_stream, "%s %d" % (key, count)
        o_stream.close()
        return

    #------------------------------------------------------------------------#

    def load(self, filename):
        """
        Loads counts from the given filename. Can be done for more than
        one file.
        """
        i_stream = sopen(filename, 'r')
        for line in i_stream:
            key, count = line.rstrip().split(_symbol_sep)
            key = _unescape_spaces(key)
            count = int(count)
            self.inc(key, count)
        i_stream.close()

        return

    #------------------------------------------------------------------------#

    @staticmethod
    def from_file(filename):
        """
        An alternative constructor which builds the distribution from a file.
        """
        dist = FreqDist()
        dist.load(filename)
        return dist

    #------------------------------------------------------------------------#

    def merge(self, rhs_dist):
        for sample, count in rhs_dist.iteritems():
            self.inc(sample, count)
        return

    #------------------------------------------------------------------------#
    # PRIVATE METHODS
    #------------------------------------------------------------------------#

    #------------------------------------------------------------------------#

#----------------------------------------------------------------------------#

class DefaultFreqDist(FreqDist):
    """
    A wrapper for a frequency distribution which defaults to the minimum
    count in the distribution for unknown values.
    """
    def __init__(self, dist):
        self.update(dist)
        self._total = dist._total
        
        # Prune empty counts
        for key in self.keys():
            if FreqDist.__getitem__(self, key) == 0:
                del self[key]
        
        self._min = min(self.itervalues())
        self._min_prob = self._min / float(self._total)
        self._min_log_prob = log(self._min_prob)
        
    def __getitem__(self, key):
        if key in self:
            return FreqDist.__getitem__(self, key)
        
        return self._min
    
    def prob(self, key):
        if key in self:
            return FreqDist.prob(self, key)
        
        return self._min_prob
    
    def log_prob(self, key):
        if key in self:
            return FreqDist.log_prob(self, key)
        
        return self._min_log_prob
        
    
#----------------------------------------------------------------------------#

class ConditionalFreqDist(dict):
    """
    A model for P(Sample|Condition) for a number of conditions.
    """
    #------------------------------------------------------------------------#
    # PUBLIC METHODS
    #------------------------------------------------------------------------#

    def inc(self, condition, sample, n=1):
        """Increments a count of (sample|condition)."""
        condition_dist = self.get(condition)
        if condition_dist is None:
            condition_dist = self.setdefault(condition, FreqDist())

        condition_dist.inc(sample, n)
        return

    #------------------------------------------------------------------------#

    def prob(self, condition, sample):
        """
        Returns P(sample | condition). An exception is raised for unseen
        conditions.
        """
        condition_dist = self.get(condition)
        if condition_dist is None:
            raise UnknownSymbolError, condition
        else:
            return condition_dist.prob(sample)

    #------------------------------------------------------------------------#

    def log_prob(self, condition, sample):
        """
        Returns log(P(sample | condition)). An exception is raised for
        unseen conditions.
        """
        condition_dist = self.get(condition)
        if condition_dist is None:
            raise UnknownSymbolError, condition
        else:
            return condition_dist.log_prob(sample)

    #------------------------------------------------------------------------#
    
    def candidates(self, condition):
        "Return candidates for the given condition."
        conditionModel = self.get(condition)

        if conditionModel is None:
            # Miss, no such condition recorded.
            return []
        else:
            # Hit, return candidates.
            return conditionModel.candidates()

    #------------------------------------------------------------------------#

    def itercounts(self):
        """
        Returns an interator over all the counts in this model, presented
        as a sequence of (condition, sample, count) tuples.
        """
        for condition, sample_dist in self.iteritems():
            for sample, count in sample_dist.iteritems():
                yield condition, sample, count
        return

    #------------------------------------------------------------------------#

    def invert(self):
        """
        Returns a P(condition|sample) model based off the same counts as
        here.
        """
        newModel = ConditionalFreqDist()
        for condition, sample, count in self.itercounts():
            newModel.inc(sample, condition, count)

        return newModel

    #------------------------------------------------------------------------#

    def dump(self, filename):
        """
        Dump this model to a filename.
        """
        o_stream = sopen(filename, 'w')
        for condition, sample, count in sorted(self.itercounts(),
                key=lambda x: (x[0], -x[2], x[1])):
            condition = _escape_spaces(unicode(condition))
            sample = _escape_spaces(unicode(sample))
            print >> o_stream, u"%s %s %d" % (
                    condition, sample, count
                )
        o_stream.close()
        return

    #------------------------------------------------------------------------#

    def load(self, filename):
        """
        Load counts for this model from a filename.
        """
        i_stream = sopen(filename, 'r')
        for line in i_stream:
            condition, sample, count = line.rstrip().split(_symbol_sep)
            condition = _unescape_spaces(condition)
            sample = _unescape_spaces(sample)
            count = int(count)
            self.inc(condition, sample, count)
        i_stream.close()
        return

    #------------------------------------------------------------------------#

    @staticmethod
    def from_file(filename):
        """
        Alternative constructor. Builds a conditional frequency distribution
        from a file in one line.
        """
        obj = ConditionalFreqDist()
        obj.load(filename)
        return obj

    #------------------------------------------------------------------------#

    def to_condition_dist(self):
        """Generates a frequency distribution of conditions."""
        dist = FreqDist()
        for condition, condition_dist in self.iteritems():
            dist.inc(condition, sum(condition_dist.itervalues()))

        return dist

    #------------------------------------------------------------------------#

    def to_sample_dist(self):
        """Generates a freqency distribution of samples."""
        dist = FreqDist()
        for condition, condition_dist in self.iteritems():
            dist.merge(condition_dist)

        return dist

#----------------------------------------------------------------------------#

def smooth_by_adding_one(freq_dist):
    # XXX this type of smoothing has a particular name (Bell smoothing?) 
    for sample in freq_dist.iterkeys():
        freq_dist[sample] += 1
    return

#----------------------------------------------------------------------------#

class UnknownSymbolError(Exception):
    """
    An error which gets thrown when encountering an unknown character.
    """
    pass

#----------------------------------------------------------------------------#

_symbol_sep = ' '           # The separator we use in our file format
_space_replacement = '_^_'  # The replacement string for dumps

def _escape_spaces(value):
    """
    Esacapes any spaces in the given string with a special value.
    
    >>> _escape_spaces('dog eats cat')
    'dog_^_eats_^_cat'

    >>> _escape_spaces('cow')
    'cow'
    """
    return value.replace(_symbol_sep, _space_replacement)

def _unescape_spaces(value):
    """
    Unescapes any escaped spaces in the string.
    
    >>> _unescape_spaces('dog_^_eats_^_cat')
    'dog eats cat'
    
    >>> _unescape_spaces('cow')
    'cow'
    """
    return value.replace(_space_replacement, _symbol_sep)

def _contains_escape(value):
    """
    Checks the string for the special replacement sequence.
    
    >>> _contains_escape('cow')
    False
    
    >>> _contains_escape('dog_^_eats_^_cat')
    True
    """
    return _space_replacement in value

def sopen(filename, mode='rb', encoding='utf8'):
    """
    Transparently uses compression on the given file based on file
    extension.

    @param filename: The filename to use for the file handle.
    @param mode: The mode to open the file in, e.g. 'r' for read, 'w' for
        write, 'a' for append.
    @param encoding: The encoding to use. Can be set to None to avoid
        using unicode at all.
    """
    read_mode = 'r' in mode
    if read_mode and 'w' in mode:
        raise Exception, "Must be either read mode or write, but not both"

    if filename.endswith('.bz2'):
        stream = bz2.BZ2File(filename, mode)
    elif filename.endswith('.gz'):
        stream = gzip.GzipFile(filename, mode)
    elif filename == '-':
        if read_mode:
            stream = sys.stdin
        else:
            stream = sys.stdout
    else:
        stream = open(filename, mode)

    if encoding not in (None, 'byte'):
        if read_mode:
            return codecs.getreader(encoding)(stream)
        else:
            return codecs.getwriter(encoding)(stream)

    return stream

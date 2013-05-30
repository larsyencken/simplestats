# -*- coding: utf-8 -*-
#
#  aggregate.py
#  simplestats
#

"Aggregating data into bins or other approximations."

_eps = 1e-8


def bins_by_data(data, n):
    """
    Puts the data into n sorted bins. Where n does not divide the length
    of the data directly, distributes the remainder as evenly as possible.
    Returns an iterator over the bins.

    @param data: A sequence of data.
    """
    data.sort()

    assert n <= len(data), "Can't split a group more ways than its length"

    items_per_group, remainder = divmod(len(data), n)

    start_at = 0
    for i in xrange(n):
        end_at = start_at + items_per_group

        if remainder > 0:
            end_at += 1
            remainder -= 1

        yield (start_at, end_at), data[start_at:end_at]

        start_at = end_at


def bins_by_increment(data, inc, key=lambda x: x[0]):
    """
    Calculates bins by range increment. Assumes data is a sequence of
    tuples, where the first tuple is the one whose range is divided up.
    """
    data = list(data)
    data.sort()

    # add _eps to the end of the range to ensure we capture that object
    start_range = key(data[0])
    end_range = key(data[-1]) + _eps

    for bin_start in frange(start_range, end_range, inc):
        bin_end = bin_start + inc

        bin_data = [x for x in data if key(x) >= bin_start
                    and key(x) < bin_end]

        yield (bin_start, bin_end), bin_data

    return


def bins_by_range(data, n, key=lambda x: x[0]):
    """
    Calculates bins by range. Assumes data is a sequence of tuples, where
    the first tuple is the one whose range is divided up.
    """
    data = list(data)
    data.sort()

    start_range = key(data[0])
    end_range = key(data[-1])
    bin_size = (end_range - start_range)/float(n)

    for i in xrange(n):
        bin_start = start_range + i*bin_size
        bin_end = start_range + (i+1)*bin_size

        # add eps to the size of the last bin to ensure we capture that
        # object
        if i == (n-1):
            use_bin_end = bin_end + _eps
        else:
            use_bin_end = bin_end

        bin_data = [x for x in data if key(x) >= bin_start
                    and key(x) < use_bin_end]

        yield (bin_start, bin_end), bin_data


def frange(start, end=None, inc=None):
    """
    A range function, that does accept float increments...
    http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66472

        >>> frange(1.0, 3.0, 0.5)
        [1.0, 1.5, 2.0, 2.5]
    """

    if end is None:
        end = start + 0.0
        start = 0.0

    if inc is None:
        inc = 1.0

    L = []
    while 1:
        next = start + len(L) * inc
        if inc > 0 and next >= end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)

    return L

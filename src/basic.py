# -*- coding: utf-8 -*-
#
#  stats.py
#  simplestats
#

"""
General combinatoric methods, in particular determining possible combinations
of input.
"""

from math import sqrt, isnan

from errors import InsufficientData


def mean(values):
    """
    Returns the mean of a sequence of values. If the sequence is empty, raises
    an InsufficientData error.

    >>> mean([1, 2, 3])
    2.0
    """
    values_iter = iter(values)
    n = 1

    # Need at least one value.
    try:
        total = values_iter.next()
    except StopIteration:
        raise InsufficientData

    for value in values_iter:
        total += value
        n += 1

    return total / float(n)


def stddev(values):
    """
    Returns the standard deviation of a sequence of values. If less than three
    values are provided, raises an InsufficientData error.

    >>> stddev([1, 2, 3])
    1.0
    """
    values_iter = iter(values)
    try:
        value = values_iter.next()
    except StopIteration:
        raise InsufficientData

    total = value
    totalSquared = value * value
    n = 1

    for value in values_iter:
        total += value
        totalSquared += value * value
        n += 1

    # Need at least two values.
    if n < 2:
        raise InsufficientData

    n = float(n)
    return sqrt((totalSquared - total * total / n) / (n - 1))


def basic_stats(values):
    """
    Returns the mean and standard deviation of the sample as a tuple.

    >>> basic_stats([1, 2, 3])
    (2.0, 1.0)
    """
    total = 0.0
    total_sq = 0.0
    i = -1
    for i, v in enumerate(values):
        total += v
        total_sq += v * v

    n = i + 1

    if n == 0:
        raise InsufficientData

    n = float(n)
    if n > 2:
        stddev_val = sqrt((total_sq - total * total / n) / (n - 1))
    else:
        stddev_val = None

    mean_val = total / n

    return (mean_val, stddev_val)


# XXX deprecate this method
is_nan = isnan

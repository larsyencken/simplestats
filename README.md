# simplestats

[![Build Status](https://travis-ci.org/larsyencken/simplestats.png)](https://travis-ci.org/larsyencken/simplestats)

### Installing

`simplestats` is [available on PyPI](http://pypi.python.org/pypi/simplestats/), so you can install it with pip:

```
pip install simplestats
```

### Descriptive statistics

`simplestats` provides many of the same basic statistics functions that you'd get from using `numpy` or another array provider, but on normal python types.

```pycon
>>> import simplestats
>>> simplestats.mean([1, 2, 3])
2.0
>>> simplestats.stddev([1, 2, 3])
1.0
>>> simplestats.basic_stats([1, 2, 3])
(2.0, 1.0)
```

### Frequency distributions

It also provides frequency distributions and conditional frequency distributions modeled after those available in the [Natural Language Toolkit](http://www.nltk.org/).

```pycon
>>> from simplestats.freq import FreqDist
>>> d = FreqDist()
>>> d.inc('cat')
>>> d.inc('dog', 3)
>>> d['cat']
1
>>> d.prob('cat')
0.25
```

A handy feature of frequency distributions is that they can be dumped to and loaded from files very easily, provided your conditions and symbols are strings (simple or unicode).

```pycon
>>> from simplestats.freq import ConditionalFreqDist
>>> cd = ConditionalFreqDist.from_file('pet_names.csv')
>>> cd.prob('dog', 'Fido')
0.05
>>> cd.dump('new_file.csv') # save to a file
>>> os.path.exists('new_file.csv')
True
>>> cd.to_condition_dist().prob('dog') # look at just the condition distribution
0.75
```

This makes it very convenient for generating simple probability models and combining them as you see fit.

### Combinatorics

The methods in this module are largely superseded by more efficient built-in versions found in Python 2.6 or later, in the `itertools` module. If you're running an older version of Python, you may still find them useful.

```pycon
>>> from simplestats.comb import combinations
>>> combinations(['Mon', 'Tue'], ['work', 'party'])
[('Mon', 'work'), ('Mon', 'party'), ('Tue', 'work'), ('Tue', 'party')]
```

The `comb` module also contains various similar methods which generate permutations or combinations. For example, `segment_combinations`, which provides permutations of segment boundaries.

```pycon
>>> from simplestats.comb import segment_combinations
>>> segment_combinations(['re', 'tri', 'ed'])
[('re', 'tri', 'ed'), ('re', 'tried'), ('retri', 'ed'), ('retried',)]
```

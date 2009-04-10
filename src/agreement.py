# -*- coding: utf-8 -*-
#
#  agreement.py
#  simplestats
# 
#  Created by Lars Yencken on 10-04-2009.
#  Copyright 2009 Lars Yencken. All rights reserved.
#

"""
Measuring agreement between raters.
"""

from itertools import izip

from freq import FreqDist
from errors import InsufficientData

def kappa(responses_a, responses_b, potential_responses=None):
    """
    Assuming matched list of response values for each rater, determine
    their kappa value using Cohen's method.
    """
    if not responses_a or not responses_b:
        raise InsufficientData, "Need at least one response to calculate kappa"

    if len(responses_a) != len(responses_b):
        raise ValueError, "Response vectors are different lengths"
    
    # Build rater bias distributions.
    bias_a = FreqDist()
    for sample in responses_a:
        bias_a.inc(sample)

    bias_b = FreqDist()
    for sample in responses_b:
        bias_b.inc(sample)

    if potential_responses is None:
        # Detect the sample range.
        potential_responses = set(bias_a.keys()).union(bias_b.keys())
    
    # calculate p_agreement: the actual frequency of agreement
    n_agreements = 0
    n_questions = 0
    for responseA, responseB in izip(responses_a, responses_b):
        if responseA == responseB:
            # they agreed 
            n_agreements += 1

        n_questions += 1

    assert n_questions > 0
    p_agreement = n_agreements / float(n_questions)

    assert 0 <= p_agreement <= 1, "P(Agreement) should be a defined probability"

    # calculate p_expected: the agreement expected by chance
    p_expected = 0.0
    for response in potential_responses:
        p_expected += bias_a.prob(response) * bias_b.prob(response)
    
    assert 0 <= p_expected <= 1, \
        "P(Expected) should be bewteeen 0 and 1, not %.2f" % p_expected

    # calculate kappa
    kappa = (p_agreement - p_expected)/(1 - p_expected)

    return kappa

# vim: ts=4 sw=4 sts=4 et tw=78:

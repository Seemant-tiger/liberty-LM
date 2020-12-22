import itertools
from collections import namedtuple

import fuzzywuzzy.fuzz
import jellyfish

from scraping.utils import cleaners

NameMatches = namedtuple('NameMatches', 'tough partial overall')


def name_match(a, b):
    a = a.encode('ascii', errors='ignore').decode()
    b = b.encode('ascii', errors='ignore').decode()
    scores_tough = []
    scores_partial = []
    
    actual_a = cleaners.as_unicode(a)
    actual_b = cleaners.as_unicode(b)
    scores_tough.extend([
        fuzzywuzzy.fuzz.ratio(actual_a, actual_b),
        fuzzywuzzy.fuzz.token_sort_ratio(actual_a, actual_b),
    ])
    scores_partial.extend([
        _word_by_word_match(actual_a, actual_b),
        round(jellyfish.jaro_winkler(actual_a, actual_b) * 100, 2),
    ])
    
    a = cleaners.as_unicode(cleaners.cleaned_string(a))
    b = cleaners.as_unicode(cleaners.cleaned_string(b))
    scores_tough.extend([
        fuzzywuzzy.fuzz.ratio(a, b),
        fuzzywuzzy.fuzz.token_sort_ratio(a, b),
    ])
    scores_partial.extend([
        _word_by_word_match(a, b),
        round(jellyfish.jaro_winkler(a, b) * 100, 2),
    ])
    
    return NameMatches(
        (max(scores_tough)),
        (max(scores_partial)),
        max((max(scores_tough), max(scores_partial))),
    )


def _word_by_word_match(a, b):
    a = a.split()
    b = b.split()
    if not (a or b) or len(a) < 2 or len(b) < 2:
        return 0
    
    ratio_1 = 0
    for i, j in itertools.product(a, b):
        if fuzzywuzzy.fuzz.ratio(i, j) > 90:
            ratio_1 = 100 / len(a)
            break
    
    ratio_2 = 0
    for i, j in itertools.product(a, b):
        if fuzzywuzzy.fuzz.ratio(i, j) > 90:
            ratio_2 = 100 / len(a)
            break
    
    return int(max(ratio_1, ratio_2))

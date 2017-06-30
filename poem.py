#!/usr/bin/env python3

import random

markov_matrix = [
    [0.1, 0.7, 0.2], # Noun
    [0.3, 0.1, 0.6], # Verb
    [0.4, 0.1, 0.5], # Adjective
]

words = [
    [ # Nouns
        'chair',
        'trash can',
        'alarm clock',
        'butterfly',
        'cloud',
        'sandwich',
        'particle',

    ], [ # Verbs
        'deconstruct',
        'smell',
        'ruin',
        'clean',
        'regard',
        'forget',
        'eat',
        'remember',
        'glitter',

    ], [ # Adjectives
        'pink',
        'easy',
        'difficult',
        'boring',
        'annoying',
        'malleable',
        'bright',
        'lost',
    ]
]

MIN_LEN = 15
MAX_LEN = 35
poem_len = int((MAX_LEN - MIN_LEN) * random.random()) + MIN_LEN

word_type = 0
for i in range(poem_len):
    word_i = int(random.random() * len(words[word_type]))
    print('{} '.format(words[word_type][word_i]), end='')

    next_word_type_prob = random.random()
    prob_sum = 0.0
    for mi, prob in enumerate(markov_matrix[word_type]):
        prob_sum += prob
        if next_word_type_prob <= prob_sum:
            word_type = mi
            break
print()

# A good one:
#
# cloud ruin cloud trash can ruin glitter annoying lost difficult
# malleable trash can regard annoying bright sandwich particle forget malleable
# boring bright alarm clock malleable annoying
#
# Formatted well:
# Clouds ruin cloud trash cans, ruins glitter.
# Annoying, lost, difficult malleable trash cans regard annoying bright sandwich
# particles.
# Forget malleable boring bright alarm clocks.
#
# Malleable.
# Annoying.

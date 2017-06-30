#!/usr/bin/env python3

import random
import pronouncing
import inflect
import small_dict

BUCKET_LEN = 5

markov_matrix = [
    [0.05, 0.6, 0.05, 0.3], # Noun
    [0.15, 0.05, 0.3, 0.5], # Verb
    [0.4, 0.1, 0.5, 0], # Adjective
    [0.05, 0.6, 0.05, 0.3], # Adverb
]

def gen_buckets():
    return [
        random.sample(small_dict.nouns, BUCKET_LEN) + ['he', 'her', 'it'],
        random.sample(small_dict.verbs, BUCKET_LEN) + ['is', 'was'],
        random.sample(small_dict.adjs, BUCKET_LEN),
        random.sample(small_dict.advs, BUCKET_LEN),
    ]

def stanza(buckets):
    line0 = line(buckets)
    rhymes = [[], [], [], []]
    for r in pronouncing.rhymes(line0[-1]):
        if r in wordnet_advs:
            rhymes[3].append(r)
        elif r in wordnet_adjs:
            rhymes[2].append(r)
        elif r in wordnet_verbs:
            rhymes[1].append(r)
        else:
            rhymes[0].append(r)

    line1 = line(buckets, rhymes=rhymes)
    line2 = line(buckets)
    line3 = line(buckets, rhymes=rhymes)

    print(format_line(line0, capitalize=True, end=','))
    print(format_line(line1, capitalize=False, end='.'))
    print(format_line(line2, capitalize=True, end=''))
    print(format_line(line3, capitalize=False, end='.'))
    print()

def format_line(line, capitalize, end):
    fmt = ' '.join(line)
    fmt = fmt.capitalize()
    fmt += end
    return fmt

def line(buckets, rhymes=None):
    word_type = random.randint(0, len(markov_matrix) - 1)
    max_len = random.randint(4, 8)

    words = []
    for i in range(max_len):
        if rhymes is not None:
            rhyme_prob = ((i + 1) / max_len)
            if random.random() <= rhyme_prob:
                if len(rhymes[word_type]) > 0:
                    words.append(random.choice(rhymes[word_type]))
                    return words

        words.append(random.choice(buckets[word_type]))
        next_word_type_prob = random.random()
        prob_sum = 0.0
        for mi, prob in enumerate(markov_matrix[word_type]):
            prob_sum += prob
            if next_word_type_prob <= prob_sum:
                word_type = mi
                break

    return words

def print_poem():
    buckets0 = gen_buckets()
    buckets1 = gen_buckets()

    stanza(buckets0)
    stanza(buckets1)
    stanza([b0 + b1 for b0, b1 in zip(buckets0, buckets1)])

if __name__ == '__main__':
    print_poem()

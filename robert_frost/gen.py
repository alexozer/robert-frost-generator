#!/usr/bin/env python3

from collections import namedtuple
import random
import numpy as np
import pronouncing

from original_poems import ROBERT_FROST
from english import PREPOSITIONS, PRONOUNS

"""
Properties of words:
- type
- beginning-line frequency
- rhyming words
"""

WORD_TYPES = [
    PRONOUNS,
    PREPOSITIONS,
    WORDNET_VERBS,
    WORDNET_NOUNS,
    WORDNET_ADJS,
    WORDNET_ADVS,
]

def tokenize(poems):
    """ Converts a string of poems into a list of lines of words """

    split_chars = '!@#$%^&*()_+-=[]{}\\|;:\",<.>/?`~ —'
    lines = []
    current_line = []
    current_word = ''
    for char in poems:
        if char in split_chars:
            if len(current_word) > 2 or current_word in ['i', 'a']:
                current_line.append(current_word)
                current_word = ''

        elif char == '\n':
            if current_line:
                lines.append(current_line)
                current_line = []
                current_word = ''

        else:
            current_word += char.lower()

    return lines

def flatten_lines(lines):
    return [word for line in lines for word in line]

def get_matrix(lines):
    matrix = [[0 for j in enumerate(WORD_TYPES)] for i in enumerate(WORD_TYPES)]
    words = flatten_lines(lines)

    for word_i, word in enumerate(words[:-1]):
        next_word = words[word_i + 1]

        word_type = get_word_type(word)
        next_word_type = get_word_type(next_word)
        if word_type is None or next_word_type is None:
            continue

        matrix[word_type][next_word_type] += 1

    row_sums = [sum(row) for row in matrix]
    norm = [[col / row_sum for col in row] for row, row_sum in zip(matrix, row_sums)]

    return norm

def get_word_type(word):
    for i, word_list in enumerate(WORD_TYPES):
        if word in word_list:
            return i

    return None

def classify_lines(lines):
    words = set(w for w in flatten_lines(lines) if get_word_type(w) is not None)
    database = {word: {} for word in words}

    for word, info in database.items():
        info['type'] = get_word_type(word)
        info['rhyming_words'] = set(pronouncing.rhymes(word)).intersection(words)

        info['begin_line_count'] = 0
        info['begin_line_prob'] = 0

    for l in lines:
        if not l:
            continue
        first_word = l[0]
        if not first_word in database:
            continue

        info = database[first_word]
        info['begin_line_count'] += 1

    for word, info in database.items():
        info['begin_line_prob'] = info['begin_line_count'] / len(words)

    return database

def get_buckets(database):
    buckets = [[] for _ in WORD_TYPES]
    for word, info in database.items():
        buckets[info['type']].append(word)

    return buckets

def gen_line(database, buckets, matrix, start_words, rhyme_word):
    max_len = random.randint(8, 10)

    words = [random.choice(start_words)]
    for i in range(max_len - 1):
        prev_word_type = database[words[i]]['type']
        word_type_prob = random.random()
        word_type = None
        prob_sum = 0.0
        for mi, prob in enumerate(matrix[prev_word_type]):
            prob_sum += prob
            if word_type_prob <= prob_sum:
                word_type = mi
                break

        rhyme_prob = ((i + 1) / max_len) ** 3
        if random.random() <= rhyme_prob:
            rhyming_words = database[rhyme_word]['rhyming_words']
            correct_rhymes = [r for r in rhyming_words if database[r]['type'] == word_type]
            if correct_rhymes:
                words.append(random.choice(correct_rhymes))
                return words

        words.append(random.choice(buckets[word_type]))

    return words

def gen_rhyme_scheme():
    length = random.randint(3, 5)
    a_rhymes = random.sample(range(length), length // 2 + 1)
    scheme = [0 for _ in range(length)]
    for i in a_rhymes:
        scheme[i] = 1

    return scheme

def get_rhyme_sets(database):
    many_rhymes = sorted(list(database.keys()), key=lambda x: -len(database[x]['rhyming_words']))
    unique_rhymes = []
    while many_rhymes:
        r = many_rhymes[0]
        unique_rhymes.append(r)
        r_rhymes = database[r]['rhyming_words']
        many_rhymes = list(filter(
            lambda x: len(database[x]['rhyming_words'].intersection(r_rhymes)) < len(r_rhymes) // 2,
            many_rhymes,
        ))

    return unique_rhymes

def gen_poem(originals):
    lines = tokenize(originals)
    matrix = get_matrix(lines)
    database = classify_lines(lines)
    database_list = list(database)
    buckets = get_buckets(database)
    rhyme_sets = get_rhyme_sets(database)
    rhyme_scheme = gen_rhyme_scheme()

    num_stanzas = random.randint(3, 5)

    def pick_rhyme():
        if not rhyme_sets:
            return random.choice(database_list)
        else:
            return rhyme_sets[int((random.random() ** 4) * len(rhyme_sets))]

    stanzas = []

    for _ in range(num_stanzas):
        rhyme_a, rhyme_b = pick_rhyme(), pick_rhyme()
        lines = []

        common_word = random.choice(database_list)
        for r in rhyme_scheme:
            selected_rhyme = [rhyme_a, rhyme_b][r]
            selected_word = common_word if random.random() < 0.5 else random.choice(database_list)
            lines.append(gen_line(database, buckets, matrix, [selected_word], selected_rhyme))

        stanzas.append(lines)

    for stanza in stanzas:
        for line in stanza:
            print(' '.join(line).capitalize())

        print()

if __name__ == '__main__':
    all_poems = ''
    for p in ROBERT_FROST.values():
        all_poems += p
    gen_poem(all_poems)

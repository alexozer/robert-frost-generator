from nltk.corpus import wordnet
def big_word_list(t):
    return {x.name().split('.', 1)[0].replace('_', ' ') for x in wordnet.all_synsets(t)}

WORDNET_NOUNS = big_word_list(wordnet.NOUN)
WORDNET_VERBS = big_word_list(wordnet.VERB)
WORDNET_ADJS = big_word_list(wordnet.ADJ)
WORDNET_ADVS = big_word_list(wordnet.ADV)

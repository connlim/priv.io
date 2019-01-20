import json
import re

import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet


lem = WordNetLemmatizer()

filename = 'test.txt'


def remove_noise(text):
    return [(word, tag) for (word, tag) in text if word not in stopwords.words('english')]


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''


def get_sentence(pos, text):
    before = text[pos::-1]
    try:
        start = len(before) - before.index('.')
    except ValueError:
        start = 0
    try:
        end = text[pos:].index('.') + pos + 1
    except ValueError:
        end = len(text)
    return text[start:end]


def main():
    with open('keywords.json') as fp:
        json_data = json.loads(fp.read())
    with open(filename) as fp:
        m = fp.read()
        tokenized = nltk.word_tokenize(m)
        tagged = nltk.pos_tag(tokenized)
        # denoised = remove_noise(tagged)
        lemmatized = [lem.lemmatize(word, 'v') for (word, tag) in tagged]

        print(' '.join(lemmatized), end='\n\n')

        results = {}
        for key in json_data:
            instances = [(x, i) for i, x in enumerate(lemmatized) for word in json_data[key] if x == word]
            if len(instances) > 0:
                results[key] = instances
        print(results, end='\n\n')

        # Get sentence
        sentences = {}
        for key in results:
            sentences[key] = {}
            for word in results[key]:
                s = ' '.join(get_sentence(word[1], tokenized))
                s = re.sub(r' ([.,!?\)])', r'\1', s)
                s = re.sub(r'(\() ', r'\1', s)
                sentences[key][word] = s
        print(sentences)


if __name__ == '__main__':
    main()

import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet

import json

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


def main():
    with open('keywords.json') as fp:
        json_data = json.loads(fp.read())
    with open(filename) as fp:
        m = fp.read()
        tokenized = nltk.word_tokenize(m)
        tagged = nltk.pos_tag(tokenized)
        # denoised = remove_noise(tagged)
        lemmatized = [lem.lemmatize(word, 'v') for (word, tag) in tagged]

        results = {}
        for key in json_data:
            instances = [(x, i) for i, x in enumerate(lemmatized) for word in json_data[key] if x == word]
            if len(instances) > 0:
                results[key] = instances 

        print(results)

        print(' '.join(lemmatized))


if __name__ == '__main__':
    main()    

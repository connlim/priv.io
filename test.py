import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet

nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('wordnet', quiet=True)

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
    with open(filename) as fp:
        m = fp.read()
        tokenized = nltk.word_tokenize(m)
        tagged = nltk.pos_tag(tokenized)
        denoised = remove_noise(tagged)
        lemmatized = [lem.lemmatize(word, 'v') for (word, tag) in denoised]

        print(' '.join(lemmatized))


if __name__ == '__main__':
    main()

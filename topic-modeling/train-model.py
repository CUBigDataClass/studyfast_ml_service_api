from utils import *
from gensim import corpora, models

def train_model(data):
    # Load our data into a dataframe and preprocess the text
    df = data_to_pd(data)
    corpus = df['text'].map(preprocess)
    # Creates a dictionary of words from the corpus
    dictionary = gensim.corpora.Dictionary(corpus)
    dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)
    bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
    # Train our model
    lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=3, id2word=dictionary, passes=2, workers=2)
    return lda_model, bow_corpus

def partition(data, search):
    lda_model, bow_corpus = train_model(data)
    scores = {}
    for i in range(0, len(bow_corpus)):
        for index, score in sorted(lda_model[bow_corpus[i]], key=lambda tup: -1*tup[1]):
            scores[index] = scores.get(index, list()) + [score]
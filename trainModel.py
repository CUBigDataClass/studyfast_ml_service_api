from utils import *
from gensim import corpora, models
import numpy as np

def train_model(data):
    # Stabilizes the model so the results are deterministic
    np.random.seed(42)
    # Load our data into a dataframe and preprocess the text
    df = data_to_pd(data)
    corpus = df['text'].map(preprocess)
    # Creates a dictionary of words from the corpus
    dictionary = gensim.corpora.Dictionary(corpus)
    bow_corpus = [dictionary.doc2bow(doc) for doc in corpus]
    # Train our model
    lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=3, id2word=dictionary, passes=2, workers=2)
    return lda_model, bow_corpus, dictionary

def classify_search(search, dictionary, lda_model):
    bow_vector = dictionary.doc2bow(preprocess(search))
    ranked = sorted(lda_model[bow_vector], key=lambda tup: -1*tup[1])
    print(ranked)
    return ranked[0][0]

def partition(data, search):
    lda_model, bow_corpus, dictionary = train_model(data)
    target_topic = classify_search(search, dictionary, lda_model)
    scores = []
    for i in range(0, len(bow_corpus)):
        ranked = sorted(lda_model[bow_corpus[i]], key=lambda tup: -1*tup[1])
        if ranked[0][0] == target_topic:
            scores.append(True)
        else:
            scores.append(False)
    return scores

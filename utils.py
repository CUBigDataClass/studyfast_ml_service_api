import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import math
import pandas as pd
from pandas.io.json import json_normalize

stemmer = SnowballStemmer("english")

def bucket_times(data, seconds=30):
    buckets = {}
    for timeframe in data:
        bucket = math.floor(timeframe['start']/seconds)
        buckets[bucket] = buckets.get(bucket, "") + timeframe['text'] + " "
    formatted = []
    for k, v in buckets.items():
        formatted.append({'bucket': k, 'text': v})
    return formatted

def data_to_pd(data):
    data = bucket_times(data)
    df = pd.DataFrame.from_dict(json_normalize(data), orient='columns')
    return df

def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result
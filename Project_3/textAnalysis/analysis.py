from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation

with open("title.txt", 'r') as f:
    lines = f.readlines()
    cv = CountVectorizer(stop_words = 'english')
    dtm = cv.fit_transform(lines)
    lda = LatentDirichletAllocation(n_components=10,random_state=0)
    extraction = lda.fit(dtm)
    feature_names = cv.get_feature_names()
    n_top_words = 5
    for topic_idx, topic in enumerate(lda.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)

with open("abstract.txt", 'r') as f:
    lines = f.readlines()
    cv = CountVectorizer(stop_words = 'english')
    dtm = cv.fit_transform(lines)
    lda = LatentDirichletAllocation(n_components=10,random_state=0)
    extraction = lda.fit(dtm)
    feature_names = cv.get_feature_names()
    n_top_words = 5
    for topic_idx, topic in enumerate(lda.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)


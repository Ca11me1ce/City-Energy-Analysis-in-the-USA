###################
# Author: Dandan Wang
# NetID: dw862
# Function: topic modeling analysis.
# #################
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation

def LDA():
    with open("text.txt", 'r') as f:
        lines = f.readlines()
        cv = CountVectorizer(stop_words = 'english')
        dtm = cv.fit_transform(lines)
        lda = LatentDirichletAllocation(n_components=10,random_state=0)
        extraction = lda.fit(dtm)
        feature_names = cv.get_feature_names()
        n_top_words = 10
        for topic_idx, topic in enumerate(lda.components_):
            message = "Topic #%d: " % topic_idx
            message += " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
            print(message)

if __name__ == "__main__":
    LDA()


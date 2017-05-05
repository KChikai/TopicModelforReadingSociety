# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import distance
from wordcloud import WordCloud
from gensim import corpora, models

# the definition of paths
DOCUMENTS = '../data/ap.dat'
VOCABULARY = '../data/vocab.txt'


def closest_to(doc_id, topics):
    dense = np.zeros((len(topics), 100), float)
    for ti, t in enumerate(topics):
        for tj, v in t:
            dense[ti, tj] = v
    pairwise = distance.squareform(distance.pdist(dense))
    largest = pairwise.max()
    for ti in range(len(topics)):
        pairwise[ti, ti] = largest + 1
    return int(pairwise[doc_id].argmin())


def create_wordcloud(text, filename):
    # choose the font suitable for your environment
    fpath = "/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc"

    wordcloud = WordCloud(background_color="black", font_path=fpath,
                          width=900, height=500).generate_from_frequencies(text)
    plt.imshow(wordcloud)
    plt.savefig(filename)


def main():
    corpus = corpora.BleiCorpus(DOCUMENTS, VOCABULARY)

    # create LDA model
    #lda = models.LdaModel(corpus, num_topics=100, id2word=corpus.id2word)
    #lda.save('ap.lda')

    # load LDA model
    lda = models.LdaModel.load('ap.lda')
    topics = [lda[c] for c in corpus]

    # create Wordcloud from two sentences
    doc_id = 50
    sentence0 = sentence1 = []
    closest_id = closest_to(doc_id, topics)
    print(closest_id)
    for index, c in enumerate(corpus):
        if index == doc_id:
            sentence0 = [(lda.id2word[tup[0]], tup[1]) for tup in c]
        if index == closest_id:
            sentence1 = [(lda.id2word[tup[0]], tup[1]) for tup in c]

    create_wordcloud(sentence0, 'sim_docs/' + str(0) + ".png")
    create_wordcloud(sentence1, 'sim_docs/' + str(1) + ".png")

    '''
    # create Wordcloud from a document
    doc_num = 2
    lists = [lda.get_topic_terms(topic_index[0], topn=10) for topic_index in topics[doc_num]]
    word_list = [(lda.id2word[tup[0]], tup[1]) for l in lists for tup in l]
    create_wordcloud(word_list, "document" + str(doc_num) + ".png")

    # create Wordcloud from a topic
    for topic_num in range(100):
        word_list = lda.show_topic(topicid=topic_num, topn=40)
        create_wordcloud(word_list, "lda_topics/topic" + str(topic_num) + ".png")
    '''


if __name__ == '__main__':
    main()
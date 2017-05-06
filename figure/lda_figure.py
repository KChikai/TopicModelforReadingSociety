# -*- coding: utf-8 -*-

import math
import json
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
from scipy.spatial import distance
from gensim import corpora, models

# the definition of data paths
DOCUMENTS = '../data/ap/ap.dat'
VOCABULARY = '../data/ap/vocab.txt'


def make_mm_corpus():
    corpus = corpora.BleiCorpus(DOCUMENTS, VOCABULARY)
    corpora.MmCorpus.serialize('ap_corpus.mm', corpus=corpus, id2word=corpus.id2word)
    with open('ap_dic.txt', 'w', encoding='utf-8') as f:
        json.dump(corpus.id2word, f)


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


def split_corpus(c, rate_or_size):
    if isinstance(rate_or_size, float):
        size = math.floor(len(c) * rate_or_size)
    else:
        size = rate_or_size

    # simple split, not take sample randomly
    left = c[:-size]
    right = c[-size:]

    return left, right


def calc_perplexity(m, c):
    return np.exp(-m.log_perplexity(c))


def search_model(corpus, dictionary, rate_or_size):
    most = [1.0e8, None]
    training, test = split_corpus(corpus, rate_or_size)
    print("data set: training/test = {0}/{1}".format(len(training), len(test)))

    for t in [100, 150, 200]:
        m = models.LdaMulticore(corpus=training, id2word=dictionary, num_topics=t, workers=2)
        p1 = calc_perplexity(m, training)
        p2 = calc_perplexity(m, test)
        print("topic_number = {0}: perplexity is {1}/{2}".format(t, p1, p2))

        if p2 < most[0]:
            most[0] = p2
            most[1] = m

    return most[0], most[1]


def bar_chart(topics, topic_dim):
    x = [i for i in range(topic_dim)]
    y1 = y2 = np.zeros(topic_dim)

    # show bar chart; topic index/topic number
    for topic_dis in topics:
        for tup in topic_dis:
            y1[tup[0]] += 1
    plt.bar(x, y1, align="center")
    #plt.xticks(x, ['{0}'.format(i) for i in range(topic_dim)])
    #plt.show()

    # show bar chart; number of topics/number of text
    for topic_dis in topics:
        y2[len(topic_dis)] += 1
    plt.bar(x, y2, align="center")
    plt.show()


def two_bar_chart(topics1, topics2, label1, label2):
    w = 0.5
    x = np.arange(60)
    y1 = np.zeros(60)
    y2 = np.zeros(60)

    for topic_dis in topics1:
        y1[len(topic_dis)] += 1
    for topic_dis in topics2:
        y2[len(topic_dis)] += 1

    plt.bar(x, y1, color='b', width=w, label=label1, align="center")
    plt.bar(x + w, y2, color='g', width=w, label=label2, align="center")
    plt.legend(loc="best")
    plt.show()


def create_wordcloud(text, filename):
    # choose the font suitable for your environment
    fpath = "/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc"

    wordcloud = WordCloud(background_color="black", font_path=fpath,
                          width=900, height=500).generate_from_frequencies(text)
    plt.imshow(wordcloud)
    plt.savefig(filename)


def main():
    # make corpus
    #make_mm_corpus()

    # load corpus
    corpus = corpora.MmCorpus('ap_corpus.mm')
    with open('ap_dic.txt', 'r', encoding='utf-8') as f:
        dictionary = json.load(f)
    dictionary = {int(i): dictionary[i] for i in dictionary}

    # load LDA and HDP model
    '''
    lda = models.LdaModel.load('../word_cloud/ap.lda')
    lda_topics = [lda[c] for c in corpus]
    hdp = models.HdpModel.load('../word_cloud/ap.hdp')
    hdp_topics = [hdp[c] for c in corpus]
    '''

    '''
    # show similar sentences
    doc_id = 100
    closest_id = closest_to(doc_id=doc_id, topics=lda_topics)
    print('Document_{0} is closest to Document_{1} in AP corpus.'.format(closest_id, doc_id))
    sentence0 = [(lda.id2word[tup[0]], tup[1]) for tup in corpus[doc_id]]
    sentence1 = [(lda.id2word[tup[0]], tup[1]) for tup in corpus[closest_id]]
    create_wordcloud(sentence0, 'sim_docs/' + str(0) + ".png")
    create_wordcloud(sentence1, 'sim_docs/' + str(1) + ".png")
    '''

    # show a bar graph
    #bar_chart(topics=topics, topic_dim=100)
    #two_bar_chart(topics1=lda_topics, topics2=hdp_topics, label1='lda', label2='hdp')
    corpus = corpora.BleiCorpus(DOCUMENTS, VOCABULARY)
    lda = models.LdaMulticore(corpus=corpus, id2word=corpus.id2word, num_topics=100, alpha=0.00001)
    d_topics = [lda[c] for c in corpus]
    lda = models.LdaModel(corpus=corpus, id2word=corpus.id2word, num_topics=100, alpha=0.00001)
    n_topics = [lda[c] for c in corpus]
    two_bar_chart(topics1=d_topics, topics2=n_topics, label1='LdaMulticore', label2='LdaModel')

    # show perplexities LDA model (topic_num = 50, 100, 150)
    #a, b = search_model(corpus, dictionary, rate_or_size=0.2)


if __name__ == '__main__':
    main()
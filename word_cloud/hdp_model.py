# -*- coding: utf-8 -*-

import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from gensim import corpora, models

# the definition of data paths
DOCUMENTS = '../data/ap/ap.dat'
VOCABULARY = '../data/ap/vocab.txt'


def create_wordcloud(text, filename):
    """
    This function creates a wordcloud image from an list of tuple data.
    :param text: list of tuple (word, frequency)
    :param filename: filename to save as an image file
    :return:
    """
    # choose the font suitable for your environment
    fpath = "/Library/Fonts/ヒラギノ丸ゴ ProN W4.ttc"

    wordcloud = WordCloud(background_color="black", font_path=fpath,
                          width=900, height=500).generate_from_frequencies(text)
    plt.imshow(wordcloud)
    plt.savefig(filename)


def main():

    # create corpus from AP data
    corpus = corpora.BleiCorpus(DOCUMENTS, VOCABULARY)

    # define HDP model
    if os.path.exists('ap.hdp'):
        # load HDP model
        hdp = models.HdpModel.load('ap.hdp')
    else:
        # create HDP model
        hdp = models.HdpModel(corpus, id2word=corpus.id2word)
        hdp.save('ap.hdp')

    # create Wordcloud from a topic
    word_list = hdp.show_topics(topics=-1, topn=40, formatted=False)        # collect all data of topics
    for topic_num in range(len(word_list)):
        tuple_list = word_list[topic_num][1]
        create_wordcloud(tuple_list, "hdp_topics/topic" + str(topic_num) + ".png")


if __name__ == '__main__':
    main()
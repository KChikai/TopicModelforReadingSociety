# Topic Model for the lecture in Onizuka Lab. NLP Team  

このレポジトリに輪講で紹介したトピックモデルについてのサンプルプログラムを置いておきます．


## Requirements

### Data Set

今回使用するデータセットとして，Associated Press (AP) データセット
（トピックモデル研究の初期から使われている、ニュースレポートのデータセット）
を使用する．データのダウンロードは`./data`ディレクトリ内で以下のコマンドを実行．

    $ ./download_ap.sh
    
解凍されたディレクトリ内に`ap.dat`, `ap.txt`, `vocab.txt`の三つのファイルができる．


### Packages

スクリプト群は全てPythonの3系で動作する．
必要なパッケージは以下の通り．

- [gensim][gensim]
- [wordcloud][wordcloud]
- numpy
- scipy
- matplotlib

[gensim]: https://radimrehurek.com/gensim/ "gensim" 
[wordcloud]: https://github.com/amueller/word_cloud "wordcloud"



## Features 

- `word_cloud/lda_model.py`
  - LDAモデルの構築，モデルが生成するトピックのワードクラウド結果を可視化．

- `word_cloud/hdp_model.py`
  - HDPモデルの構築，モデルが生成するトピックのワードクラウド結果を可視化．

- `figure/lda_figure.py`
  - 生成したモデルの類似文書を計算
  - 類似トピックのワードクラウド化
  - トピック分布の出力



## Create LDA or HDP Model

ダウンロードしたデータからLDA，HDPモデルの作成を行う．
追記予定．


## Result 

実際のサンプル結果を示す．


***One of the topic in LDA model:***

![lda alpha](https://github.com/OnizukaLab/TopicModelReadingSociety/blob/master/data/example_results/sample_lda_topic.png?raw=true)

上図は実際に生成されたLDAモデルのトピックの一つを[wordcloud][wordcloud]に出力した例である．
データセットが昔のニュース記事であるので，[1988年アメリカ合衆国大統領選挙][election]の候補者であった
マイケル・デュカキスとジョージ・H・W・ブッシュの名前が同一topic内に含まれていることがわかる．

[election]: https://ja.wikipedia.org/wiki/1988%E5%B9%B4%E3%82%A2%E3%83%A1%E3%83%AA%E3%82%AB%E5%90%88%E8%A1%86%E5%9B%BD%E5%A4%A7%E7%B5%B1%E9%A0%98%E9%81%B8%E6%8C%99 "election"


***Alpha Parameter of LDA model:***

![lda alpha](https://github.com/OnizukaLab/TopicModelReadingSociety/blob/master/data/example_results/lda_alpha.png?raw=true)

AlphaはLDAモデル内のディリクレ分布のパラメータであり，数値を大きくすることでトピック数を増やすことができる．
上図グラフでは，Alphaの数値を大きくすることでトピック数の偏りが平滑化されている．


***Number of topics between LDA model and HDP model:***

![lda alpha](https://github.com/OnizukaLab/TopicModelReadingSociety/blob/master/data/example_results/lda_alpha.png?raw=true)

同一コーパスでモデルを生成した時のLDAとHDPのトピック分布の違いを示す．
LDAは手動で100トピックと設定，HDPはトピック数は自動決定であり150トピックとなった．



## Reference

- [実践 機械学習システム][book1] Willi Richert (著), Luis Pedro Coelho (著), 斎藤 康毅 (翻訳)
- [自然言語処理概論][book2] 黒橋 禎夫 (著), 柴田 知秀 (著)

[book1]: https://www.amazon.co.jp/%E5%AE%9F%E8%B7%B5-%E6%A9%9F%E6%A2%B0%E5%AD%A6%E7%BF%92%E3%82%B7%E3%82%B9%E3%83%86%E3%83%A0-Willi-Richert/dp/4873116988 "book1"
[book2]: https://www.amazon.co.jp/%E8%87%AA%E7%84%B6%E8%A8%80%E8%AA%9E%E5%87%A6%E7%90%86%E6%A6%82%E8%AB%96-%E3%83%A9%E3%82%A4%E3%83%96%E3%83%A9%E3%83%AA%E6%83%85%E5%A0%B1%E5%AD%A6%E3%82%B3%E3%82%A2-%E3%83%86%E3%82%AD%E3%82%B9%E3%83%88-%E9%BB%92%E6%A9%8B-%E7%A6%8E%E5%A4%AB/dp/4781913881/ref=sr_1_2?s=books&ie=UTF8&qid=1494058369&sr=1-2&keywords=%E8%87%AA%E7%84%B6%E8%A8%80%E8%AA%9E%E5%87%A6%E7%90%86%E3%80%80%E9%BB%92%E6%A9%8B "book2"

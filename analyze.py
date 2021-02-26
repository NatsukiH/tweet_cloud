import MeCab
import matplotlib.pyplot as plt
import csv
from wordcloud import WordCloud
from tqdm import tqdm


def mecab_tweet(tweets_data):

    # # 読込むファイル名を設定
    # fname = r"'" + dfile + "'"
    # fname = fname.replace("'", "")

    # Mecabを使用して、形態素解析
    mecab = MeCab.Tagger("-Ochasen")

    # "名詞", "動詞", "形容詞", "副詞"を格納するリスト
    words = []

    # ファイルを読込み
    # with open(fname, 'r', encoding="utf-8") as f:
    for reader in tqdm(tweets_data):
        # reader = f.readline()

        # Mecabで形態素解析を実施
        node = mecab.parseToNode(reader)

        while node:
            word_type = node.feature.split(",")[0]

            # 取得する単語は、"名詞", "動詞", "形容詞", "副詞"
            if word_type in ["名詞", "動詞", "形容詞", "副詞"]:
                words.append(node.surface)

            node = node.next
            # reader = f.readline()

    # wordcloudで出力するフォントを指定
    # font_path = r"C:\WINDOWS\Fonts\HGRGE.TTC"

    stop_words = ['https', '://', '=&', 'する', 'ください', '@', '/',
                  ';', '。', 'Japan', 'RT', u'説明', u'データ', u'する', u'オラクル', u'日本', u'提供', u'開催', u'お客様']
    changed_words = [w for w in words if w not in stop_words]

    txt = " ".join(changed_words)

    return txt

    # print(txt)

    # ストップワードの設定　※これは検索キーワードによって除外したほうがいい単語を設定
    # stop_words = ['https', 'OracleInnovation', 'Innovation', 'Oracle', 'co', 'the', 'of',
    #               'Summit', 'Tokyo', 'Japan', 'RT', u'説明', u'データ', u'する', u'オラクル', u'日本', u'提供', u'開催', u'お客様']

    # # 解析した単語、ストップワードを設定、背景の色は黒にしてます
    # wordcloud = WordCloud(background_color="black", font_path=font_path, stopwords=set(stop_words),
    #                       width=800, height=600).generate(txt)
    # wordcloud = WordCloud(background_color="black", stopwords=set(stop_words),
    #                       width=800, height=600).generate(txt)

    # plt.imshow(wordcloud)
    # plt.axis("off")
    # plt.show()

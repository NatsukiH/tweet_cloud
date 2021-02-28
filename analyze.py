import MeCab
import matplotlib.pyplot as plt
import csv
from wordcloud import WordCloud
from tqdm import tqdm


def mecab_tweet(tweets_data):

    # Mecabを使用して、形態素解析
    mecab = MeCab.Tagger("-Ochasen")

    # "名詞", "動詞", "形容詞", "副詞"を格納するリスト
    words = []

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

    # stop_words = ['https', '://', '=&', 'する', 'ください', '@', '/',
    #               ';', '。', 'Japan', 'RT', u'説明', u'データ', u'する', u'オラクル', u'日本', u'提供', u'開催', u'お客様']
    stop_words = ['https', '://', '=&', '@', '/', ';', '。', 'RT', 'は', '、', 'の', '（', '）', 'に', 'で', 'を', 'た',
                  'し', 'が', 'と', 'て', 'ある', 'れ', 'さ', 'する', 'いる', 'から', 'も', '・', 'として', '「', '」',
                  'い', 'こと', '–', 'な', 'なっ', 'や', 'れる', 'など', 'ため', 'この', 'まで', 'また', 'あっ', 'ない',
                  'あり', 'なる', 'その', 'られ', '後', '『', '』', 'へ', 'という', 'よう', '(', 'もの', 'より', 'だ',
                  'おり', '的', '中', 'により', ')', '2', 'による', '第', 'なり', 'によって', '1', 'これ', 'その後',
                  'ず', ',', 'か', '時', 'なく', 'られる', 'だっ', 'において', '者', 'なかっ', '行わ', '多く', 'しかし',
                  '3', 'せ', '他', '名', 'それ', 'について', '間', '上', 'ば', '受け', '.', '呼ば',
                  'なお', 'できる', '目', '行っ', '内', 'う', '数', 'のみ', '前', '以下', 'き', '：', '元', '化',
                  '4', '等', 'および', 'でき', '同年', '主', '場合', '際', '一', '約', 'における', 'さらに', '人',
                  'ら', '5', '中心', 'いう', '知ら', '初', 'だけ', '時代', '以上',
                  '生まれ', '2010年', 'にて', '見', '務め', '持つ', 'とともに', '大', '頃', '2007年', '2009年',
                  '2008年', 'うち', '行う', 'ほか', '特に', '全', 'ながら', '当初', '発売', 'せる', '2011年',
                  'かつて', '下', '一つ', '2006年', '6', 'でも', '年', '2012年', '形', '用い', 'に対して',
                  '/', '本', '考え', 'なら', '以外', '一方', 'それぞれ', '各', '同様', '4月', '経', '2013年',
                  'と共に', '2005年', 'そして', '3月', 'これら', '及び', '用', '2014年', '事', 'ものの',
                  'にかけて', '部', '通り', 'とも', '彼', '2015年', 'または', 'たり', '側', 'とき', 'ほど', 'ので', 'ただし',
                  '二', '2004年', '郡', '初めて', 'たち', '部分', '2016年', '最も', '7', '旧', '地', '10月', '8',
                  '系', '大きな', '続け', '以前', '全て', '与え', '9月', '含む', 'といった', 'ほとんど', '7月',
                  'ところ', '2017年', '2003年', '向け', '持っ', '2000年', '加え', '使わ', '型', '6月', 'に関する',
                  '12月', '名称', 'に対する', '1月', '万', '5月', '-1', '名前', '〜', '＝', '※', '”', '“', '→', '…', '×', '！',
                  '／', '？', '○', 'ノ', '〈', '〉', '々', '，', '＆', '☆', '―', '＋', 'α', '〒', '《', '》', '‐', '…。',
                  '【', '】', '★', 'ください', 'そう', 'そう', '#', 'さん', 'ちゃん', 'the', 'a']
    changed_words = [w for w in words if w not in stop_words]

    txt = " ".join(changed_words)

    return txt

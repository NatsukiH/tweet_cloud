import tweepy           # To consume Twitter's API
import pandas as pd     # To handle data
import numpy as np      # For number computing
from flask import Flask, render_template, request
import datetime
from tqdm import tqdm

import os
from os.path import join, dirname
from dotenv import load_dotenv

import analyze

app = Flask(__name__)
# We import our access keys:
# API's setup:


def twitter_setup():

    # python で Twitter APIを使用するためのConsumerキー、アクセストークン設定
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    Consumer_key = os.environ['CONSUMER_KEY']
    Consumer_secret = os.environ['CONSUMER_SECRET']
    Access_token = os.environ['ACCESS_TOKEN']
    Access_secret = os.environ['ACCESS_SECRET']

    # 認証
    auth = tweepy.OAuthHandler(Consumer_key, Consumer_secret)
    auth.set_access_token(Access_token, Access_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    return api


def get_tweetdata(api, keyword):
    # 検索キーワード設定
    q = keyword
    # つぶやきを格納するリスト
    tweets_data = []
    # カーソルを使用してデータ取得
    for tweet in tqdm(tweepy.Cursor(api.search, q=q, tweet_mode='extended', lang='ja', result_type="recent").items(20)):

        # つぶやき時間がUTCのため、JSTに変換  ※デバック用のコード
        # jsttime = tweet.created_at + datetime.timedelta(hours=9)
        # print(jsttime)

        # つぶやきテキスト(FULL)を取得
        tweets_data.append(tweet.full_text + '\n')
    print("Getting Tweet data...")

    return tweets_data


api = twitter_setup()


@app.route('/', methods=['GET'])
def get():
    return render_template("index.html")


@app.route('/', methods=['POST'])
def post():
    query = request.form.get('query')

    if query == "":
        return render_template("index.html")
    else:
        tweets_data = get_tweetdata(api, query)
        tweets_txt = analyze.mecab_tweet(tweets_data)
        if tweets_txt == "":
            return render_template('notfound.html', title=query)
        else:
            return render_template('result.html', title=query, tweets=tweets_data, tweets_txt=tweets_txt)


@app.route('/giikusai')
def giikusai():
    tweets_data = get_tweetdata(api, "#技育祭 -RT")
    tweets_txt = analyze.mecab_tweet(tweets_data)
    return render_template("result.html", title="#技育祭", tweets=tweets_data, tweets_txt=tweets_txt)


@app.route('/halla')
def rooma():
    tweets_data = get_tweetdata(api, "#ホールA -RT")
    tweets_txt = analyze.mecab_tweet(tweets_data)
    if tweets_txt == "":
        return render_template('notfound.html', title="#ホールA")
    else:
        return render_template("result.html", title="#ホールA", tweets=tweets_data, tweets_txt=tweets_txt)
    # return render_template("result.html", title="#ホールA", tweets=tweets_data, tweets_txt=tweets_txt)


@app.route('/hallb')
def roomb():
    tweets_data = get_tweetdata(api, "#ホールB -RT")
    tweets_txt = analyze.mecab_tweet(tweets_data)
    if tweets_txt == "":
        return render_template('notfound.html', title="#ホールB")
    else:
        return render_template("result.html", title="#ホールB", tweets=tweets_data, tweets_txt=tweets_txt)
    # return render_template("result.html", title="#ホールB", tweets=tweets_data, tweets_txt=tweets_txt)


@app.route('/hallc')
def roomc():
    tweets_data = get_tweetdata(api, "#ホールC -RT")
    tweets_txt = analyze.mecab_tweet(tweets_data)
    if tweets_txt == "":
        return render_template('notfound.html', title="#ホールC")
    else:
        return render_template("result.html", title="#ホールC", tweets=tweets_data, tweets_txt=tweets_txt)
    # return render_template("result.html", title="#ホールC", tweets=tweets_data, tweets_txt=tweets_txt)


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

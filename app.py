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
    for tweet in tqdm(tweepy.Cursor(api.search, q=q, count=100, tweet_mode='extended', lang='ja').items(20)):

        # つぶやき時間がUTCのため、JSTに変換  ※デバック用のコード
        #jsttime = tweet.created_at + datetime.timedelta(hours=9)
        # print(jsttime)

        # つぶやきテキスト(FULL)を取得
        tweets_data.append(tweet.full_text + '\n')
    print("Getting Tweet data...")

    return tweets_data


api = twitter_setup()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/page0')
def page0():
    tweets_data = get_tweetdata(api, "#技育祭 -RT ")
    tweets_txt = analyze.mecab_tweet(tweets_data)
    return render_template("page0.html", tweets=tweets_data, tweets_txt=tweets_txt)


@app.route('/page1')
def page1():
    tweets_data = get_tweetdata(api, "#ウインターハッカソン -RT ")
    tweets_txt = analyze.mecab_tweet(tweets_data)
    return render_template("page1.html", tweets=tweets_data, tweets_txt=tweets_txt)


@app.route('/page2')
def page2():
    tweets_data = get_tweetdata(api, "#駆け出しエンジニアと繋がりたい -RT ")
    tweets_txt = analyze.mecab_tweet(tweets_data)
    return render_template("page2.html", tweets=tweets_data, tweets_txt=tweets_txt)


@app.route('/page3')
def page3():
    tweets_data = get_tweetdata(api, "#プログラミング -RT ")
    tweets_txt = analyze.mecab_tweet(tweets_data)
    return render_template("page3.html", tweets=tweets_data, tweets_txt=tweets_txt)


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# from credentials import *    # This will allow us to use the keys as variables
import tweepy           # To consume Twitter's API
import pandas as pd     # To handle data
import numpy as np      # For number computing
from flask import Flask, render_template, request
import datetime
from tqdm import tqdm


app = Flask(__name__)
# We import our access keys:
# API's setup:


def twitter_setup():

    # python で Twitter APIを使用するためのConsumerキー、アクセストークン設定
    Consumer_key = 'rLR7hXgxncgqoZO8zRC9EmZVw'
    Consumer_secret = 'I4aGqPNiVvnpbLssdFRLEUhCFKVr9KQZ3jDj8jbLO96TjXDMaZ'
    Access_token = '976845735969935360-dNTPhOII0Lb2O1qlDYCFAUSPjCE4EXd'
    Access_secret = 'AME1JZHsBoATojFFKPGYdP1Rks0qqdspCKO5ywiqAAReU'

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
    tweets_data = get_tweetdata(api, "技育祭 -RT ")
    return render_template("index.html", tweets=tweets_data)


@app.route('/page1')
def page1():
    tweets_data = get_tweetdata(api, "キンプリ -RT ")
    return render_template("page1.html", tweets=tweets_data)


@app.route('/page2')
def page2():
    tweets_data = get_tweetdata(api, "King&Prince -RT ")
    return render_template("page2.html", tweets=tweets_data)


if __name__ == '__main__':
    app.run(debug=True)

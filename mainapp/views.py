from django.shortcuts import render
from textblob import TextBlob
import tweepy
# Create your views here.

consumer_key = "VgDQeZQRev9pwq94QLacQ5pT4"
consumer_secret = "8r5DaSNabr1i2HGHry15GhNgcdDX9WPiiUIGTHNZSW7bKPpOh9"

access_token = "739533477784100864-kTuX5EaRxmneG9Ps4arND3hsik1IlVn"
access_token_secret = "05P3FY5wQWYZiHPjMaUmOP3vIGJQ8Sl6jCKVoqiEBIqpH"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def textformatting(tweet):
    text = tweet.text
    print(text)
    try:
        if 'RT ' in text:
            text = text.split(':', 1)
            text = text[1]
    except:
        pass
    return text


def profile_pic_quality(tweet):
    profile_pic = tweet.user.profile_image_url
    profile_pic = profile_pic.replace("_normal", "")
    return profile_pic


def tweet_template(public_tweets):
    tweets = []
    for tweet in public_tweets:
        # Tweet Text
        text = textformatting(tweet)

        # User Info
        screen_name = tweet.user.screen_name
        profile_pic = profile_pic_quality(tweet)
        followers_count = tweet.user.followers_count

        # Sentiment Analaysis
        sentiment = sentiment_analysis(tweet)

        # Context Dictionary
        tweet_template = {'screen_name': screen_name, 'text': text, 'sentiment': sentiment,
                          'profile_pic': profile_pic, 'followers_count': followers_count}

        tweets.append(tweet_template)
    return tweets


def sentiment_analysis(tweet):
    analysis = TextBlob(tweet.text)
    sentiment = analysis.sentiment.polarity
    print(sentiment)
    return sentiment


def get_context_dict(search_query):
    if search_query:
        # Public Tweet List
        public_tweets = api.search(search_query, lang='en')
        tweets = tweet_template(public_tweets)
        context_dict = {'tweets': tweets}
    else:
        context_dict = {}
        print("Passed")
        pass
    return context_dict


def index(request):
    if request.method == 'GET':

        search_query = request.GET.get('search_box')
        context_dict = get_context_dict(search_query)

    return render(request, 'mainapp/index.html', context=context_dict)

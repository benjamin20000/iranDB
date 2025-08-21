from fetcher import  Fetcher
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from tqdm.auto import tqdm
import pandas as pd
def _count_words(tweet):
    words = tweet.split()
    count = {}
    for word in words:
        if word in count:
            count[word] += 1
        else:
            count[word] = 1
    return count
def _find_rarest_world(tweet):
    my_dict = _count_words(tweet)
    return min(my_dict, key=my_dict.get)

def assign_rarest_world(df):
    text_col = df["Text"]
    tqdm.pandas()
    df['rarest_world'] =  text_col.progress_apply(_find_rarest_world)


def _classified_emotion(tweet):
    score = SentimentIntensityAnalyzer().polarity_scores(tweet)
    return score["compound"]

def assign_emotion(df):
    text_col = df["Text"]
    tqdm.pandas()
    scores = text_col.progress_apply(_classified_emotion) # pandas apply
    bins = [-1, -0.5, 0.5, 1]
    labels = ["negative", "neutral", "positive"]
    df['sentiment'] = pd.cut(scores, bins=bins, labels=labels, right=True)





df = Fetcher.get_df()
assign_rarest_world(df)
assign_emotion(df)
print(df)

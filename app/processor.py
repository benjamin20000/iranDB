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

def assign_rarest_world(df):
    df['rarest_world'] = None
    for index in df.index:
        my_dict = _count_words(df.loc[index]["Text"])
        df.loc[index,'rarest_world'] = min(my_dict, key=my_dict.get)

def _classified_emotion(tweet):
    score = SentimentIntensityAnalyzer().polarity_scores(tweet)
    return score["compound"]

def assign_emotion(df):
    text_col = df["Text"]
    tqdm.pandas()
    scores = text_col.progress_apply(_classified_emotion) # pandas apply
    print(scores)
    bins = [-1, -0.5, 0.5, 1]
    labels = ["negative", "neutral", "positive"]
    df['sentiment'] = pd.cut(scores, bins=bins, labels=labels, right=True)
    print(df)





df = Fetcher.get_df()
# assign_rarest_world(df)
assign_emotion(df)
# print(df)

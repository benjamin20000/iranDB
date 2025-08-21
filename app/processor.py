from fetcher import  Fetcher
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from tqdm.auto import tqdm
import pandas as pd
from config import blacklist_path


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


def _load_blacklist():
    black_list = []
    with open(blacklist_path, "r") as file:
        for line in file:
            black_list.append(line.rstrip())
    return black_list


def _detected_weapons(tweet,black_list):
    words = tweet.split()
    for word in words:
        if word in black_list:
            return word
    return ""

def assign_weapons_detected(df):
    black_list = _load_blacklist()
    text_col = df["Text"]
    tqdm.pandas()
    df['weapons_detected'] = text_col.progress_apply(_detected_weapons, args=(black_list,))
    print(df['weapons_detected'])

# df = Fetcher.get_df()
# assign_weapons_detected(df)
# assign_rarest_world(df)
# assign_emotion(df)
# print(df)

import os

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from tqdm.auto import tqdm
import pandas as pd
from app.config import blacklist_path

class Processor:
    def _count_words(self, tweet):
        words = tweet.split()
        count = {}
        for word in words:
            if word in count:
                count[word] += 1
            else:
                count[word] = 1
        return count

    def _find_rarest_world(self, tweet):
        my_dict = self._count_words(tweet)
        return min(my_dict, key=my_dict.get)

    def assign_rarest_world(self,df):
        text_col = df["Text"]
        tqdm.pandas()
        df['rarest_world'] =  text_col.progress_apply(self._find_rarest_world)

    def _classified_emotion(self, tweet):
        score = SentimentIntensityAnalyzer().polarity_scores(tweet)
        return score["compound"]

    def assign_emotion(self, df):
        tqdm.pandas() #init tqdm lib
        nltk_dir = "/tmp/nltk"
        os.makedirs(nltk_dir,exist_ok=True)
        nltk.data.path.append(nltk_dir)
        nltk.download('vader_lexicon',download_dir=nltk_dir,quiet=True) # download vader_lexicon for nltk lib
        text_col = df["Text"]
        scores = text_col.progress_apply(self._classified_emotion) # pandas apply
        bins = [-1, -0.5, 0.5, 1]
        labels = ["negative", "neutral", "positive"]
        df['sentiment'] = pd.cut(scores, bins=bins, labels=labels, right=True)


    def _load_blacklist(self):
        black_list = []
        with open(blacklist_path, "r") as file:
            for line in file:
                black_list.append(line.rstrip())
        return black_list

    # ----- iterating over the black list
    # ----- to check if tween contains this line - one word or more
    def _detected_weapons(self, tweet,black_list):
        for weapon in black_list:
            if weapon in tweet:
                return weapon
        return ""

    def assign_weapons_detected(self, df):
        black_list = self._load_blacklist()
        text_col = df["Text"]
        tqdm.pandas()
        df['weapons_detected'] = text_col.progress_apply(self._detected_weapons, args=(black_list,))





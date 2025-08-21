from pymongo import MongoClient
import os
from dotenv import load_dotenv
import pandas as pd


class Fetcher:
    @staticmethod
    def _get_uri():
        load_dotenv(dotenv_path=".env")
        username = os.getenv("username")
        password = os.getenv("password")
        db = os.getenv("db_name")
        uri = f"mongodb+srv://{username}:{password}@{db}.gurutam.mongodb.net/"
        return uri

    @staticmethod
    def _get_tweets():
        uri = Fetcher._get_uri()
        client = MongoClient(uri)
        mydb = client["IranMalDB"]
        collection  = mydb["tweets"]
        tweets_collection = collection.find({},{"_id":0})
        tweets_arr = []
        for tweet in tweets_collection:
            tweets_arr.append(tweet)
        client.close()
        return tweets_arr

    @staticmethod
    def get_df():
        data = Fetcher._get_tweets()
        df = pd.DataFrame(data)
        return df



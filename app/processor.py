from fetcher import  Fetcher



def _count_words(tweet):
    words = tweet.split()
    count = {}
    for word in words:
        if word in count:
            count[word] += 1
        else:
            count[word] = 1
    return count

def find_rarest_world():
    df = Fetcher.get_df()
    _count_words(df.loc[2]["Text"])


find_rarest_world()
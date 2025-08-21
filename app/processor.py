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

def assign_rarest_world():
    df = Fetcher.get_df()
    df['rarest_world'] = None
    for index in df.index:
        my_dict = _count_words(df.loc[index]["Text"])
        df.loc[index,'rarest_world'] = min(my_dict, key=my_dict.get)
    print(df)

assign_rarest_world()
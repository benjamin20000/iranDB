from app.fetcher import  Fetcher
from app.processor import Processor


class Manager:
    def __init__(self, flag=True):
        self.df = Fetcher.get_df()
        if len(self.df) == 0:
            flag = False
        self.processor = Processor()



    def process(self):
        self.processor.assign_rarest_world(self.df)
        self.processor.assign_emotion(self.df)
        self.processor.assign_weapons_detected(self.df)

    def get_data(self):
        return self.df.to_dict(orient="records")



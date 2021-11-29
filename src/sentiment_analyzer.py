import re
import os
import logging
import en_core_web_sm
import emoji
import numpy
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import spacy
from config import REDDIT_WORD_SENTIMENT
from collections import defaultdict
from datetime import date
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.sentiment import vader
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import RegexpTokenizer
from plotly.subplots import make_subplots


logging.basicConfig(level = logging.INFO)


class SentimentAnalyzer:
    def __init__(self, reddit_word_sentiment):
        self.dates = [date(2021,10,day).strftime("%Y-%m-%d") for day in range(1, 32)]
        self.filenames = [f"{os.getcwd()}/data/bitcoin_subreddit_{date}.txt" for date in self.dates]
        self.reddit_word_sentiment = reddit_word_sentiment
        self.data = defaultdict(list)
        self.cleaned_data = defaultdict(list)
        self.sentiment_scores = defaultdict(list)


    def populate_data(self):
        for i, filename in enumerate(self.filenames):
            with open(filename, "r") as handler:
                for line in handler:
                    line = line.strip()
                    first_space = line.find(" ")
                    second_space = line.find(" ", first_space+1)
                    # check if the second word for the line is "submission" or "comment"
                    # remove the first (id) and second word (submission / comment) if the above is true
                    if first_space != -1 and second_space != -1 and line[first_space+1:second_space] == "submission" or line[first_space+1:second_space] == "comment":
                        # the data key is data such as 2021-10-01 
                        # the data value is a list. the list contains all the comments and submissions for the date
                        self.data[self.dates[i]].append(line[second_space+1:])


    def clean_data(self):
        tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|http\S+')
        nlp = en_core_web_sm.load()
        all_stopwords = nlp.Defaults.stop_words
        lemmatizer = WordNetLemmatizer()
        stemmer = PorterStemmer()
        for date, lines in self.data.items():
            # cast each word as str in submission and comment lst
            str_lines = [str(i) for i in lines]
            # convert lst to str
            unclean_str = ' , '.join(str_lines)
            # remove emoji from str
            no_emoji_str = emoji.get_emoji_regexp().sub(u'',unclean_str)
            # tokenize 
            tokens = tokenizer.tokenize(no_emoji_str)    
            # convert word in tokens to lowercase
            tokens = [word.lower() for word in tokens]
            # remove stopwords
            tokens = [word for word in tokens if word not in all_stopwords]
            # normalize with lemmatizing
            tokens = ([lemmatizer.lemmatize(word) for word in tokens])
            # normalize words with stemming
            tokens = [stemmer.stem(word) for word in tokens]
            self.cleaned_data[date] = tokens


    def generate_sentiment_scores(self):
        sia = vader.SentimentIntensityAnalyzer()
        sia.lexicon.update(self.reddit_word_sentiment)
        for date, tokens in self.cleaned_data.items():
            for token in tokens:
                pol_score = sia.polarity_scores(token)
                pol_score["words"] = token
                self.sentiment_scores[date].append(pol_score["compound"])
        self.sentiment_scores = {date: numpy.mean(scores) for date, scores in self.sentiment_scores.items()}


    def visualize_sentiment(self):
        btc_ss = pd.DataFrame(self.sentiment_scores.items(), columns=["Date", "Score"])
        btc_prices = pd.read_csv(f"{os.getcwd()}/data/bitcoin_oct_prices.csv")
        # convert to datetime
        btc_ss['Date'] = pd.to_datetime(btc_ss['Date'])
        btc_prices['Date'] = pd.to_datetime(btc_prices['Date'])
        #convert to numeric
        btc_prices['Price'] = btc_prices['Price'].str.replace(',', '').astype(float) 
        # create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        # add traces
        fig.add_trace(
            go.Scatter(x=btc_ss['Date'], y=btc_ss['Score'], name="sentiment"),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=btc_prices['Date'], y=btc_prices['Price'], name="price"),
            secondary_y=True,
        )
        # add figure title
        fig.update_layout(
            title_text="Bitcoin Sentiment vs Price"
        )
        # set x-axis title
        fig.update_xaxes(title_text="Date")
        # set y-axes titles
        fig.update_yaxes(title_text="<b>primary</b> Bitcoin Sentiment", secondary_y=False)
        fig.update_yaxes(title_text="<b>secondary</b> Bitcoin Price", secondary_y=True)
        # plot graph
        fig.show()


    def run(self):
        self.populate_data()
        self.clean_data()
        self.generate_sentiment_scores()
        for date, mean_score in self.sentiment_scores.items():
            logging.info(f"The mean sentiment score for {date} is {mean_score}")
        self.visualize_sentiment()
        

if __name__ == "__main__":
    sa = SentimentAnalyzer(REDDIT_WORD_SENTIMENT)
    sa.run()
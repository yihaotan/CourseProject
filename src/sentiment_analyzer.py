import re
import os
import logging
import en_core_web_sm
import emoji
import spacy
from collections import defaultdict
from datetime import date
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk import FreqDist


logging.basicConfig(level = logging.INFO)


class SentimentAnalyzer:
    def __init__(self):
        self.dates = [date(2021,10,day).strftime("%Y-%m-%d") for day in range(1, 32)]
        self.filenames = [f"{os.getcwd()}/bitcoin_subreddit_{date}.txt" for date in self.dates]
        self.data = defaultdict(list)
        self.cleaned_data = defaultdict(str)


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
                        # the data value is a list. the list contains all the commnets and submissions for the date
                        self.data[self.dates[i]].append(line[second_space+1:])


    def clean_data(self):
        self.populate_data()
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


if __name__ == "__main__":
    sa = SentimentAnalyzer()
    sa.clean_data()
    for date, tokens in sa.cleaned_data.items():
        logging.info(f"The date is: {date}")
        logging.info(f"The tokens is: {tokens}")
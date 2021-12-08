# CourseProject

Please fork this repository and paste the github link of your fork on Microsoft CMT. Detailed instructions are on Coursera under Week 1: Course Project Overview/Week 9 Activities.

# Crypto Sentiment Analysis 

## Goal 

The goal of this project is to:
- scrape submissions / comments from the most popular Bitcoin [subreddit](https://www.reddit.com/r/Bitcoin/) between 2021-10-01 and 2021-10-31.
- clean and preprocess the data.
- perform Bitcoin sentiment analysis using [Vader](https://github.com/cjhutto/vaderSentiment) and [Pushshift] (https://github.com/pushshift/api)
- implement a Bitcoin sentiment vs price visualization.
- evalute sentiment result with external sources with [Crypto Fear & Greed Index](https://alternative.me/crypto/fear-and-greed-index/).

## Documentation 

### Overview of functions 

1. scrapper.py 


```
scrape_data(self, comment_cnt):
```
scrape data using VADER and Pushshift. The number of top comments per submission is less than or equal to the comment_cnt.

```
write_data(self):
```
write the scrapped data line by line to data/bitcoin_subreddit_{date}.txt. Example of data is 2021-10-01.


2. sentiment_analyzer.py 

```
clean_data(self):
```
clean the data by converting the str data per day to word tokens.
stopwords and emojis are removed from the each token.
the tokens are also stemmed and lemmatized.
the cleaned_data is of this format: {'2021-10-01': ['clean_data_1', 'clean_data_2'], '2021-10-02': ['clean_data_1', 'clean_data_2'].

```
generate_sentiment_scores(self):
```
generate sentiment score by using Vader.
compute the mean overall compound score per day.

```
visualize_sentiment(self):
```
plot a bitcoin sentiment vs price per day for the month of Oct-2021 using plotly.
the x-axis is date and the y-axis is a dual axis of sentiment score and bitcoin price.



### Implementation documentation 

There are 2 main python files scrapper.py and sentiment_analyzer.py in the codebase.

1. scrapper.py

* The main responsibility of scapper class is to scrape submissions / comments from Bitcoin subreddit and write the data to text files in src/data directory.
* Each file contains data for a given day i.e. bitcoin_subreddit_2021_10_01.txt. In total, there are 31 files from 2021-10-01 to 2021-10-31.
* There are 3 columns per file. The first column is the ID, the second column is the data type (submission / comment) and the third column is the text data.
* To reduce the size of the dataset, only the top 10 comments are chosen for each submission.
* Pushshift and Vader are required to scrape the Bitcoin subreddit data, as Vader cannot scrape data by date. 
* For a given day, Pushshift scrapes all the submission ids while Vader scrape all the submission texts the comment ids and comments associated with submission id. This process contiunes from 2021-10-01 to 2021-10-31.

2. sentiment_analyzer.py

* The main responsibility of sentiment_analyzer class is to clean and preprocess data, perform Bitcoin sentiment analysis and implement a Bitcoin sentiment vs price visualization.
* The cleaning and preprocessing portion involves the following steps:
  1. Get the submission and comment text from each file i.e. bitcoin_subreddit_2021_10_01.txt.
  2. Remove emojis from the submission and comment texts.
  3. Tokenize the submission and comment texts into token (word).
  4. Lowercase each token.
  5. Remove stopwords.
  6. Lemmatize each token.
  7. Stem each token.
* The sentiment analysis involves the following steps:
  1. Update the Vader lexicon with custom Bitcoin sentiment keywords. The keywords are found in src/config.py. Examples of keywords include 'mooning': 1.0, 'tendie': 0.5 and 'paper': -0.5.
  1. Compute the polarity compound score for each token per day using Vader.
  2. Compute the overall mean polarity compound score per day using numpy.
* Use plotly to plot the Bitcoin sentiment vs price visualization. The x-axis is date while the left y-axis is Bitcoin sentiment (overall mean daily polarity compound score) and the right y-axis is the daily Bitcoin price.

![bitcoin_sentiment_vs_price](https://user-images.githubusercontent.com/9248134/145162940-bb65a9d2-814a-497a-bab4-0edb761dcb32.png)

### Usage documentation

Git clone the repo.

```
git clone https://github.com/yihaotan/CourseProject.git
```

Set up a virtual python environment (Optional).

```
python -m venv /path/to/directory
```

Activate virtual python environment (Optional).

```
source /path/to/venv/bin/activate
```


Go to the cloned repo and install all the necessary python packages in requirements.txt.

```
pip install -r requirements.txt
```

Add the new keywords and score in src/config.py if you like (Optional).

```
{ ...,
  'red': -1.0
}
```


Run the sentiment_analyzer.py. This will open a plotly graph of Bitcoin sentiment vs price in your localhost. 

```
cd src
python sentiment_analyzer.py
```

Run scrapper.py. This will write 31 text files in this format such as bitcoin_subreddit_2021_10_01 to the src/data directory (Optional). 

```
cd src
python scrapper.py
```

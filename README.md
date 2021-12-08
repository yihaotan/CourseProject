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




### Implementation documentation 

There are 2 main python files scrapper.py and sentiment_analyzer.py in the codebase

1. scrapper.py

* The main responsibility of scapper class is to scrape submissions / comments from Bitcoin subreddit and write the data to text files in src/data directory.
* Each file contains data for a given day i.e. bitcoin_subreddit_2021_10_01.txt. In total, there are 31 files from 2021-10-01 to 2021-10-31.
* There are 3 columns per file. The first column is the ID, the second column is the data type (submission / comment) and the third column is the text data.
* To reduce the size of the dataset, only the top 10 comments are chosen for each submission.
* Pushshift and Vader are required to scrape the Bitcoin subreddit data, as Vader cannot scrape data by date. 
* For a given day, pushshift scrapes all the submission ids while Vader scrape all the submssison texts the comment ids and comments associated with submission id. This process repeats for each day in the month of Oct, 2021.

2. sentiment_analyzer.py




### Usage documentation

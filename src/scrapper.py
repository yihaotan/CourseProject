import praw
import requests
import json
import time
import logging
from collections import defaultdict, namedtuple
from datetime import date, timedelta

logging.basicConfig(level = logging.INFO)
RedditData = namedtuple("RedditData", "id data_type text")


class RedditScapper():
    def __init__(self, subreddit, data_type, start_date, end_date):
        self.reddit_client = praw.Reddit(
            client_id="0dZ8lx8njCLOBwPW2GhgKg", 
            client_secret="8snDPMZnkRlMvNUSDUypH81F22pszA", 
            user_agent="ua"
        )
        self.subreddit = subreddit
        self.data_type = data_type 
        self.start_date = start_date 
        self.end_date = end_date
        self.comment_cnt = 0
        self.submission_cnt = 0
        self.output = defaultdict(list)
    

    def _get_pushshift_data(self, data_type, subreddit, start_date, end_date):
        base_url = "https://api.pushshift.io"
        url = f"{base_url}/reddit/{data_type}/search?&size=1000&after={start_date}&before={end_date}&subreddit={subreddit}"
        logging.info(f"The pushshift url is {url}")
        response = requests.get(url)
        data = json.loads(response.text)
        return data["data"]
    

    def _get_date_submission(self, data_type, subreddit, start_date, end_date):
        dates = {
            (start_date + timedelta(days=i)).strftime("%Y-%m-%d"): (start_date + timedelta(days=i+1)).strftime("%Y-%m-%d") \
            for i in range((end_date-start_date).days+1)
        }
        date_submission = defaultdict(list)
        for sd, ed in dates.items():
            data = self._get_pushshift_data(data_type, subreddit, sd, ed)
            time.sleep(1)
            submissions = [d["id"] for d in data]
            date_submission[sd].extend(submissions)
        return date_submission


    def scrape_data(self, comment_cnt=10):
        all_submission_ids = []
        submission_info = defaultdict(list)
        date_submission = self._get_date_submission(self.data_type, self.subreddit, self.start_date, self.end_date)
        
        for date in date_submission:
            all_submission_ids.extend(date_submission[date])
        
        for submission_id in all_submission_ids:
            submission = self.reddit_client.submission(submission_id)
            self.submission_cnt += 1
            logging.info(f"Scrapping submission #{self.submission_cnt} {submission_id}")
            submission_info[submission_id].append(RedditData(submission.id, "submission", submission.title))
            submission.comments.replace_more(limit=0)
            submission.comment_sort = "top"
            submission.comments.list()
            cur_cnt = 0
            for comment in submission.comments.list():
                if cur_cnt == comment_cnt: 
                    break 
                submission_info[submission_id].append(RedditData(comment.id, "comment", comment.body))
                logging.info(f"Scrapping comment {comment.id}")
                self.comment_cnt += 1
                cur_cnt += 1
        
        for date, submission_ids in date_submission.items():
            for submission_id in submission_ids:
                self.output[date].extend(submission_info[submission_id])
        
            
    def write_data(self):
        for date, data in self.output.items():
            with open(f"bitcoin_subreddit_{date}.txt", "w") as handler:
                for d in data: 
                    handler.write(f"{d.id} {d.data_type} {d.text} \n")


if __name__ == "__main__":
    reddit_scrapper = RedditScapper("bitcoin", "submission", date(2021,10,1), date(2021,10,31))
    reddit_scrapper.scrape_data()
    reddit_scrapper.write_data()
    for date, data in reddit_scrapper.output.items():
        logging.info(f"The total number of submissions and comments for {date} is {len(data)}")
    logging.info(f"The total number of submissions are: {reddit_scrapper.submission_cnt}")
    logging.info(f"The total number of comments are: {reddit_scrapper.comment_cnt}")
    logging.info("Scrapping completed!")
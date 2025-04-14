import os
import snscrape.modules.twitter as sntwitter
import pandas as pd
import json
import csv
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TwitterScraper:
    def __init__(self):
        """
        Initialize the TwitterScraper with default values
        """
        self.tweets_list = []
        self.df = None
    
    def search_by_keyword(self, keyword, limit=100, start_date=None, end_date=None, lang=None):
        """
        Search tweets by keyword
        
        Args:
            keyword (str): Keyword to search for
            limit (int): Maximum number of tweets to return
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            lang (str): Language filter (e.g., 'en' for English)
            
        Returns:
            pandas.DataFrame: DataFrame containing tweets
        """
        query = f"{keyword}"
        
        if start_date and end_date:
            query += f" since:{start_date} until:{end_date}"
        
        if lang:
            query += f" lang:{lang}"
            
        logging.info(f"Searching for tweets with query: {query}")
        
        try:
            self.tweets_list = []
            
            # Using Twitter Search to get tweets
            for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
                if i >= limit:
                    break
                
                self.tweets_list.append({
                    'date': tweet.date,
                    'id': tweet.id,
                    'url': tweet.url,
                    'content': tweet.rawContent,
                    'user': tweet.user.username,
                    'reply_count': tweet.replyCount,
                    'retweet_count': tweet.retweetCount,
                    'like_count': tweet.likeCount,
                    'quote_count': tweet.quoteCount
                })
            
            # Creating a dataframe
            self.df = pd.DataFrame(self.tweets_list)
            logging.info(f"Successfully retrieved {len(self.tweets_list)} tweets")
            return self.df
            
        except Exception as e:
            logging.error(f"Error searching for tweets: {str(e)}")
            raise
    
    def search_by_hashtag(self, hashtag, limit=100, start_date=None, end_date=None, lang=None):
        """
        Search tweets by hashtag
        
        Args:
            hashtag (str): Hashtag to search for (with or without the # symbol)
            limit (int): Maximum number of tweets to return
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            lang (str): Language filter (e.g., 'en' for English)
            
        Returns:
            pandas.DataFrame: DataFrame containing tweets
        """
        # Add the # symbol if it's not already there
        if not hashtag.startswith('#'):
            hashtag = f"#{hashtag}"
            
        return self.search_by_keyword(hashtag, limit, start_date, end_date, lang)
    
    def search_by_user(self, username, limit=100, start_date=None, end_date=None):
        """
        Search tweets by Twitter user
        
        Args:
            username (str): Twitter username (with or without the @ symbol)
            limit (int): Maximum number of tweets to return
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            
        Returns:
            pandas.DataFrame: DataFrame containing tweets
        """
        # Remove the @ symbol if it's present
        if username.startswith('@'):
            username = username[1:]
            
        query = f"from:{username}"
        
        if start_date and end_date:
            query += f" since:{start_date} until:{end_date}"
            
        logging.info(f"Searching for tweets with query: {query}")
        
        try:
            self.tweets_list = []
            
            # Using Twitter Search to get tweets
            for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
                if i >= limit:
                    break
                
                self.tweets_list.append({
                    'date': tweet.date,
                    'id': tweet.id,
                    'url': tweet.url,
                    'content': tweet.rawContent,
                    'user': tweet.user.username,
                    'reply_count': tweet.replyCount,
                    'retweet_count': tweet.retweetCount,
                    'like_count': tweet.likeCount,
                    'quote_count': tweet.quoteCount
                })
            
            # Creating a dataframe
            self.df = pd.DataFrame(self.tweets_list)
            logging.info(f"Successfully retrieved {len(self.tweets_list)} tweets")
            return self.df
            
        except Exception as e:
            logging.error(f"Error searching for tweets: {str(e)}")
            raise
    
    def save_to_csv(self, filename=None):
        """
        Save the scraped tweets to a CSV file
        
        Args:
            filename (str, optional): Filename to save the CSV. If none provided, 
                                      a default name with timestamp will be used.
                                      
        Returns:
            str: Path to the saved file
        """
        if self.df is None or self.df.empty:
            logging.error("No tweets to save. Run a search method first.")
            return None
            
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"twitter_data_{timestamp}.csv"
        
        try:
            self.df.to_csv(filename, index=False, quoting=csv.QUOTE_ALL)
            logging.info(f"Data saved to {filename}")
            return filename
        except Exception as e:
            logging.error(f"Error saving to CSV: {str(e)}")
            return None
    
    def save_to_json(self, filename=None):
        """
        Save the scraped tweets to a JSON file
        
        Args:
            filename (str, optional): Filename to save the JSON. If none provided, 
                                      a default name with timestamp will be used.
                                      
        Returns:
            str: Path to the saved file
        """
        if self.df is None or self.df.empty:
            logging.error("No tweets to save. Run a search method first.")
            return None
            
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"twitter_data_{timestamp}.json"
        
        try:
            # Convert datetime objects to strings for JSON serialization
            json_df = self.df.copy()
            if 'date' in json_df.columns:
                json_df['date'] = json_df['date'].astype(str)
                
            json_df.to_json(filename, orient='records', indent=4)
            logging.info(f"Data saved to {filename}")
            return filename
        except Exception as e:
            logging.error(f"Error saving to JSON: {str(e)}")
            return None
    
    def get_statistics(self):
        """
        Calculate statistics about the scraped tweets
        
        Returns:
            dict: Dictionary containing statistics
        """
        if self.df is None or self.df.empty:
            logging.error("No tweets to analyze. Run a search method first.")
            return {}
            
        stats = {
            'total_tweets': len(self.df),
            'avg_replies': self.df['reply_count'].mean() if 'reply_count' in self.df.columns else 0,
            'avg_retweets': self.df['retweet_count'].mean() if 'retweet_count' in self.df.columns else 0,
            'avg_likes': self.df['like_count'].mean() if 'like_count' in self.df.columns else 0,
            'avg_quotes': self.df['quote_count'].mean() if 'quote_count' in self.df.columns else 0
        }
        
        return stats 
from database import db
from datetime import datetime

class Tweet(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    reply_count = db.Column(db.Integer, default=0)
    retweet_count = db.Column(db.Integer, default=0)
    like_count = db.Column(db.Integer, default=0)
    quote_count = db.Column(db.Integer, default=0)
    
    # For search history tracking
    search_id = db.Column(db.Integer, db.ForeignKey('search.id'), nullable=True)
    
    def __repr__(self):
        return f"<Tweet {self.id}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat(),
            'content': self.content,
            'user': self.user,
            'url': self.url,
            'reply_count': self.reply_count,
            'retweet_count': self.retweet_count,
            'like_count': self.like_count,
            'quote_count': self.quote_count
        }


class Search(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    search_type = db.Column(db.String(50), nullable=False)
    query = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    limit = db.Column(db.Integer, default=100)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    lang = db.Column(db.String(10), nullable=True)
    
    # Relationship with tweets
    tweets = db.relationship('Tweet', backref='search', lazy=True)
    
    def __repr__(self):
        return f"<Search {self.id}: {self.search_type} - {self.query}>"
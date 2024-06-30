import praw
import firebase_admin
from firebase_admin import credentials, firestore


reddit = praw.Reddit(
    client_id='your_client_id',
    client_secret='your_client_server',
    user_agent='your_user_agent'
)


if not firebase_admin._apps:
    cred = credentials.Certificate("./serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()


def fetch_and_store_indian_politics_data(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    for submission in subreddit.search('flair:Politics OR flair:"Indian Politics" OR flair:"Political Discussion"', sort='new', limit=100):
        
        data = {
            'title': submission.title,
            'score': submission.score,
            'id': submission.id,
            'url': submission.url,
            'created': submission.created,
            'num_comments': submission.num_comments,
            'body': submission.selftext,
            'author': submission.author.name if submission.author else None,
            'location': submission.author_flair_text if submission.author_flair_text else None
        }
    
        db.collection('politics100').document(submission.id).set(data)


fetch_and_store_indian_politics_data('IndiaSpeaks')

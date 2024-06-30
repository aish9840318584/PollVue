import praw
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Reddit API
reddit = praw.Reddit(
    client_id='XVOwcl8EnAsyLP8yG2rSpA',
    client_secret='bnODrAwL3ZfzQTzvCDmzBoJFP59xew',
    user_agent='PollVue'
)

# Initialize Firebase (only once)
if not firebase_admin._apps:
    cred = credentials.Certificate("./serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Function to fetch data about Indian politics from Reddit and store it in Firebase
def fetch_and_store_indian_politics_data(subreddit_name):
    subreddit = reddit.subreddit(subreddit_name)
    for submission in subreddit.search('flair:Politics OR flair:"Indian Politics" OR flair:"Political Discussion"', sort='new', limit=100):
        # Extract relevant data
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
        # Store data in Firestore
        db.collection('politics100').document(submission.id).set(data)

# Example usage: Fetch data from r/IndiaSpeaks or another relevant subreddit
fetch_and_store_indian_politics_data('IndiaSpeaks')

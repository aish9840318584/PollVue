import streamlit as st
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob
from firebase_admin import firestore, credentials
import firebase_admin
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


nltk.download('stopwords')


if not firebase_admin._apps:
    cred = credentials.Certificate("./serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def fetch_data():
    docs = db.collection('politics100').stream()
    data = []
    for doc in docs:
        data.append(doc.to_dict())
    return data

def analyze_sentiment(text):
    if text:
        text_without_stopwords = ' '.join([word for word in text.split() if word.lower() not in stopwords.words('english')])
        blob = TextBlob(text_without_stopwords)
        polarity = blob.sentiment.polarity
        if polarity >= 0.5:
            support_level = "Strongly Supportive"
        elif polarity > 0:
            support_level = "Supportive"
        elif polarity == 0:
            support_level = "Neutral"
        elif polarity >= -0.5:
            support_level = "Opposed"
        else:
            support_level = "Strongly Opposed"
        return polarity, support_level
    return 0, "Neutral"

def main():
    st.markdown("<h1 style='text-align: center;'>Political Statistics</h1>", unsafe_allow_html=True)
    data = fetch_data()

    location_sentiments = {}

    for entry in data:
        location = entry.get('location', 'Unknown')
        polarity, _ = analyze_sentiment(entry.get('title', ''))
        if location not in location_sentiments:
            location_sentiments[location] = []
        location_sentiments[location].append(polarity)

    avg_sentiments = {loc: sum(sents) / len(sents) for loc, sents in location_sentiments.items()}
    sorted_sentiments = sorted(avg_sentiments.items(), key=lambda x: x[1], reverse=True)

    st.header("Top 5 Supportive States")
    for loc, sentiment in sorted_sentiments[:5]:
        st.subheader(f"{loc}: {sentiment:.2f}")
        st.progress((sentiment + 1) / 2)

    st.header("Top 5 Opposed States")
    for loc, sentiment in sorted_sentiments[-5:]:
        st.subheader(f"{loc}: {sentiment:.2f}")
        st.progress((sentiment + 1) / 2)


    st.header("Sentiment Polarity by State")
    df = pd.DataFrame(list(avg_sentiments.items()), columns=['State', 'Polarity'])
    df = df.sort_values(by='Polarity', ascending=False)

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(x='Polarity', y='State', data=df, palette='viridis', ax=ax)
    ax.set_xlabel('Polarity')
    ax.set_ylabel('State')
    ax.set_title('Sentiment Polarity by State')
    st.pyplot(fig)

if __name__ == "__main__":
    main()

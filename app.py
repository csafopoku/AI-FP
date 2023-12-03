from flask import Flask, render_template, request, url_for, redirect
import tweepy 
from tensorflow.keras.models import load_model
import joblib

app = Flask(__name__)

# Load your LSTM model
model_path="best_lstm_model.joblib"
# model = load_model('model.keras')
best_lstm_model=joblib.load(model_path)

# Twitter API credentials
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAOrEpwEAAAAAqkND%2BUblN2UrMpPBSt5c%2FV%2Fn%2Bfc%3DtGUr8XKJXQwIFtYiAC8SP4d9wSkuCVKrqiDaQpa8dfoABIIkY8'

# Set up Tweepy client
client = tweepy.Client(bearer_token=bearer_token)

def get_tweet_text(tweet_id):
    try:
        tweet = client.get_tweet(tweet_id, tweet_fields=['context_annotations', 'created_at'])
        return tweet.data.text
    except tweepy.TweepError as e:
        print("Tweepy Error: {}".format(e))
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    tweet_url = request.form['tweet_url']
    
    # Extract tweet ID from the URL
    tweet_id = tweet_url.split('/')[-1]
    
    # Get the tweet text
    tweet_text = get_tweet_text(tweet_id)
    
    if tweet_text is None:
        return render_template('error.html', message="Unable to fetch tweet.")

    # Classify the tweet
    result, flagged_words = model.classify(tweet_text)  # Adjust according to your model's method

    # Display the result
    return render_template('result.html', result=result, flagged_words=flagged_words, tweet_text=tweet_text)

if __name__ == '__main__':
    app.run(debug=True)
# -*- coding: utf-8 -*-
"""sentimental_Analysis_Twitter.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-HGYJwb5mBXLCkgQWndNEW0DGJZ-ntmn
"""

pip install tweepy

import tweepy
import pandas as pd

consumer_key = "fqOdqBRuqEKnJiNCkn9yLV87N"
consumer_secret = "hnHzBskX5tOjjOeG3Z0mu1mHEtBmojwZs2t7s1g50jmU7ZWwcZ"
access_token = "1786638188259209216-eWp6ImDanmoKoyj7ZY5kXgsneHRTQm"
access_token_secret = "MPFWoXv7jTS8COJXB6RbpmaFQBKy2ej2A3DubDgJIef8U"

# Authenticate with Twitter API
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Define search query (e.g., hashtags)
query = "#Women OR #Metoo"

# Collect tweets
tweets = []
for tweet in tweepy.Cursor(api.search_tweets, q=query, tweet_mode='extended', lang='en').items(1000):
    tweets.append(tweet._json)

# Convert tweets to DataFrame
df = pd.DataFrame(tweets)

# Save DataFrame to CSV
df.to_csv('tweets_dataset.csv', index=False)

import pandas as pd
from google.colab import drive
from textblob import TextBlob
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

drive.mount('/content/drive')
file_path = '/Twitter_Data.csv'

# Load the dataset
tweets_data = pd.read_csv(file_path)

# Clean the dataset (assuming 'text' column contains the tweet text)
cleaned_tweets = [TextBlob(tweet).clean for tweet in tweets_data['text']]

# Perform sentiment analysis and classify tweets
sentiments = [TextBlob(tweet).sentiment.polarity for tweet in cleaned_tweets]
classified_sentiments = ['positive' if sentiment > 0 else 'negative' if sentiment < 0 else 'neutral' for sentiment in sentiments]

# Add classified sentiments to the dataset
tweets_data['sentiment'] = classified_sentiments

# Split dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(tweets_data['text'], tweets_data['sentiment'], test_size=0.2, random_state=42)

# Train your machine learning model (e.g., using sklearn)
# (Note: You need to vectorize your text data before training)
# (Here, I'm using a placeholder for demonstration)
# model.fit(X_train_vectorized, y_train)

# Predict sentiment on test set
# y_pred = model.predict(X_test_vectorized)

# Evaluate the model
# print(classification_report(y_test, y_pred))

# You can further analyze the results, compare performance of different algorithms, etc.

# Check the first few rows of the dataset
print(tweets_data.head())

# Drop rows with missing values in the 'clean_text' column
tweets_data = tweets_data.dropna(subset=['clean_text'])

# Convert 'clean_text' column to string to handle any non-string values
tweets_data['clean_text'] = tweets_data['clean_text'].astype(str)

# Drop rows with missing values in the 'category' column
tweets_data = tweets_data.dropna(subset=['category'])

# Convert 'category' column to integers to handle any non-integer values
tweets_data['category'] = tweets_data['category'].astype(int)

# Convert 'category' column to strings
tweets_data['category'] = tweets_data['category'].astype(str)

# Evaluate the model
print(classification_report(tweets_data['category'], tweets_data['predicted_category']))

print(classification_report(tweets_data['category'], tweets_data['predicted_category'], zero_division=1))

# Assuming your DataFrame is named tweets_data
# Convert the 'clean_text' column to lowercase to ensure case-insensitive search
tweets_data['clean_text_lower'] = tweets_data['clean_text'].str.lower()

# Count occurrences of the word "women"
women_count = tweets_data['clean_text_lower'].str.count('women').sum()

print("Occurrences of the word 'women' in the dataset:", women_count)

import matplotlib.pyplot as plt

# Filter the dataset to include only the rows containing the word "women"
women_tweets = tweets_data[tweets_data['clean_text_lower'].str.contains('women')]

# Group by sentiment category and count occurrences
sentiment_counts = women_tweets.groupby('predicted_category').size()

# Plot the distribution
sentiment_counts.plot(kind='bar', color=['green', 'red', 'blue'])
plt.title('Sentiment Distribution of Tweets containing "women"')
plt.xlabel('Sentiment Category')
plt.ylabel('Number of Tweets')
plt.xticks([0,1,2], labels=['Positive', 'Negative', 'Neutral'])
plt.show()

# Count total tweets
total_tweets = len(tweets_data)

print("Total number of tweets:", total_tweets)

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pandas as pd
from google.colab import drive

drive.mount('/content/drive')
file_path = '/content/Twitter_Data.csv'

# Load the dataset

tweets_data = pd.read_csv(file_path)
women_tweets = tweets_data[tweets_data['clean_text'].str.contains('women')]
# Assuming 'clean_text_lower' is the column containing preprocessed text data
X = women_tweets['clean_text_lower']
y = women_tweets['predicted_category']  # Assuming 'predicted_category' is the column containing sentiment labels

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorize the text data
vectorizer = TfidfVectorizer(max_features=1000)  # Adjust max_features as needed
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Initialize classifiers
nb_classifier = MultinomialNB()
svm_classifier = SVC()
rf_classifier = RandomForestClassifier()
lr_classifier = LogisticRegression()

# Train classifiers
nb_classifier.fit(X_train_vectorized, y_train)
svm_classifier.fit(X_train_vectorized, y_train)
rf_classifier.fit(X_train_vectorized, y_train)
lr_classifier.fit(X_train_vectorized, y_train)

# Evaluate classifiers
print("Naive Bayes:")
print(classification_report(y_test, nb_classifier.predict(X_test_vectorized)))

print("SVM:")
print(classification_report(y_test, svm_classifier.predict(X_test_vectorized)))

print("Random Forest:")
print(classification_report(y_test, rf_classifier.predict(X_test_vectorized)))

print("Logistic Regression:")
print(classification_report(y_test, lr_classifier.predict(X_test_vectorized)))

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pandas as pd
from google.colab import drive
import matplotlib.pyplot as plt
import re


drive.mount('/content/drive')
file_path = '/content/Twitter_Data.csv'

# Load the dataset

tweets_data = pd.read_csv(file_path)

tweets_data = tweets_data.dropna(subset=['clean_text'])
# Filter the dataset to include only the rows containing the word "women"
women_data = tweets_data[tweets_data['clean_text'].str.contains('women')]

# Prepare text data and labels
X = women_data['clean_text']
y = women_data['category']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorize the text data
vectorizer = TfidfVectorizer(max_features=1000)  # You can adjust max_features as needed
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Initialize classifiers
nb_classifier = MultinomialNB()
svm_classifier = SVC()
rf_classifier = RandomForestClassifier()
lr_classifier = LogisticRegression()

# Train classifiers
nb_classifier.fit(X_train_vectorized, y_train)
svm_classifier.fit(X_train_vectorized, y_train)
rf_classifier.fit(X_train_vectorized, y_train)
lr_classifier.fit(X_train_vectorized, y_train)

# Evaluate classifiers
print("Naive Bayes:")
print(classification_report(y_test, nb_classifier.predict(X_test_vectorized)))

print("SVM:")
print(classification_report(y_test, svm_classifier.predict(X_test_vectorized)))

print("Random Forest:")
print(classification_report(y_test, rf_classifier.predict(X_test_vectorized)))

print("Logistic Regression:")
print(classification_report(y_test, lr_classifier.predict(X_test_vectorized)))


import numpy as np
import matplotlib.pyplot as plt

# Define the classes and metrics
classes = ['-1.0', '0.0', '1.0']
metrics = ['Precision', 'Recall', 'F1-score', 'Support']

# Define the values for each metric for each class
precision = [0.88, 0.67, 0.53]
recall = [0.12, 0.15, 0.99]
f1_score = [0.22, 0.24, 0.69]
support = [57, 27, 81]

# Set the width of the bars
bar_width = 0.2
index = np.arange(len(classes))

# Plotting
plt.figure(figsize=(10, 6))

# Plot bars for precision
plt.bar(index - bar_width, precision, bar_width, label='Precision')
# Plot bars for recall
plt.bar(index, recall, bar_width, label='Recall')
# Plot bars for F1-score
plt.bar(index + bar_width, f1_score, bar_width, label='F1-score')
# Plot bars for support
plt.bar(index + 2*bar_width, support, bar_width, label='Support')

plt.xlabel('Classes')
plt.ylabel('Scores')
plt.title('Naive Bayes Classifier Metrics')
plt.xticks(index + bar_width, classes)
plt.legend()
plt.tight_layout()
plt.show()

# Define the classes and metrics
classes = ['-1.0', '0.0', '1.0']
metrics = ['Precision', 'Recall', 'F1-score', 'Support']

# Define the values for each metric for each class for SVM
svm_precision = [0.85, 0.63, 0.57]
svm_recall = [0.20, 0.35, 0.91]
svm_f1_score = [0.32, 0.45, 0.70]
svm_support = [57, 27, 81]

# Define the values for each metric for Random Forest
rf_precision = [0.78, 0.59, 0.57]
rf_recall = [0.25, 0.37, 0.91]
rf_f1_score = [0.37, 0.45, 0.70]
rf_support = [57, 27, 81]

# Define the values for each metric for Logistic Regression
lr_precision = [0.78, 0.59, 0.57]
lr_recall = [0.25, 0.37, 0.91]
lr_f1_score = [0.37, 0.45, 0.70]
lr_support = [57, 27, 81]

# Set the width of the bars
bar_width = 0.2
index = np.arange(len(classes))

# Plotting
plt.figure(figsize=(14, 8))

# Plot bars for SVM
plt.bar(index - 1.5*bar_width, svm_precision, bar_width, label='SVM Precision')
plt.bar(index - 0.5*bar_width, svm_recall, bar_width, label='SVM Recall')
plt.bar(index + 0.5*bar_width, svm_f1_score, bar_width, label='SVM F1-score')
plt.bar(index + 1.5*bar_width, svm_support, bar_width, label='SVM Support')

# Plot bars for Random Forest
plt.bar(index - 1.25*bar_width, rf_precision, bar_width, label='RF Precision')
plt.bar(index - 0.25*bar_width, rf_recall, bar_width, label='RF Recall')
plt.bar(index + 0.75*bar_width, rf_f1_score, bar_width, label='RF F1-score')
plt.bar(index + 1.75*bar_width, rf_support, bar_width, label='RF Support')

# Plot bars for Logistic Regression
plt.bar(index - 1.0*bar_width, lr_precision, bar_width, label='LR Precision')
plt.bar(index, lr_recall, bar_width, label='LR Recall')
plt.bar(index + 1.0*bar_width, lr_f1_score, bar_width, label='LR F1-score')
plt.bar(index + 2.0*bar_width, lr_support, bar_width, label='LR Support')

plt.xlabel('Classes')
plt.ylabel('Scores')
plt.title('Classification Metrics Comparison')
plt.xticks(index, classes)
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=5)

# Adding classifier names below x-axis
plt.text(-0.5, -0.25, 'SVM', ha='center', fontsize=12)
plt.text(2, -0.25, 'Random Forest', ha='center', fontsize=12)

plt.tight_layout()
plt.show()
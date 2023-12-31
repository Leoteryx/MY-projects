# -*- coding: utf-8 -*-
"""youtube_project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lpiv_ig7-cnpMQj6g-tt3cyKD7vmjZNh
"""

pip install streamlit

pip install --upgrade google-api-python-client

import streamlit as st

import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import seaborn as sns

Api_key ='AIzaSyAmg0kvBQshDg7Oz3PBNdzSwEyt3t3_TOU'
channel_ids =['UCU0U7reTj3KykVTxALcEg9Q',
              'UCnRGynbTJF0AoOjqanabIJw',
              'UCWKAAgM5L7bExQJkPZIbiaw',
              'UC83dMRaZBlOVn8jFkM1LWrA',
              'UCi3o8sgPl4-Yt501ShuiEgA',
              'UC7fQFl37yAOaPaoxQm-TqSA',
              'UC6NK95qassTilrIVwD5oA7Q',
              'UC3mb5QRlm4VQmOZD_P0ctGw',
              'UCZpwN3B2gqLX21WwWDF6N0w',
              'UCYHH2O-3PPL_o7nP7IBhwng'
              ]

youtube = build("youtube", "v3",developerKey = Api_key)

#CHANNEL_DETAILS
def get_channel_stats(youtube,channel_ids):
  all_data=[]
  request=youtube.channels().list(
            part='snippet,contentDetails,statistics',
            id=','.join(channel_ids))
  response = request.execute()

  for i in range(len(response['items'])):
      data = dict(channel_name=response['items'][i]['snippet']['title'],
              channel_id=response['items'][i]['id'] ,
              subscribers=response['items'][i]['statistics']['subscriberCount'],
              views=response['items'][i]['statistics']['viewCount'],
              playlist_id=response['items'][i]['contentDetails']['relatedPlaylists']['uploads'],
              total_videos=response['items'][i]['statistics']['videoCount']
              )
      all_data.append(data)

  return all_data

channel_statistics=get_channel_stats(youtube,channel_ids)

channel_data=pd.DataFrame(channel_statistics)

channel_data

channel_data['subscribers']=pd.to_numeric(channel_data['subscribers'])
channel_data['views']=pd.to_numeric(channel_data['views'])
channel_data['total_videos']=pd.to_numeric(channel_data['total_videos'])
channel_data.dtypes

channel_data

"""**playlist_data**"""

playlist_id0=channel_data.loc[channel_data['channel_name']=='Way2go தமிழ்','playlist_id'].iloc[0]
#playlist_id1=channel_data.loc[channel_data['channel_name']=='JTS Challengers','playlist_id'].iloc[0]
#playlist_id2=channel_data.loc[channel_data['channel_name']=='Tamil Trekker','playlist_id'].iloc[0]
#playlist_id3=channel_data.loc[channel_data['channel_name']=='Vaai Savadaal','playlist_id'].iloc[0]

#playlist ids
def get_playlist_info(youtube, channel_ids):
  playlist_info = []
  try:
        # Retrieve the channel's content details
        channels_response = youtube.channels().list(
            part='contentDetails',
            id=','.join(channel_ids)
        ).execute()
        for channel in channels_response['items']:
            channel_id = channel['id']
            content_details = channel['contentDetails']
            playlist_ids = content_details['relatedPlaylists']

            playlists_response = youtube.playlists().list(
                part='snippet',
                id=','.join(playlist_ids.values())
            ).execute()
            for playlist in playlists_response['items']:
                playlist_id = playlist['id']
                playlist_name = playlist['snippet']['title']

                playlist_info.append({
                    'channel_id': channel_id,
                    'playlist_id': playlist_id,
                    'playlist_name': playlist_name
                })
  except HttpError as e:
       print(e)
  return playlist_info

playlist_info = get_playlist_info(youtube, channel_ids)

playlist_data=pd.DataFrame(playlist_info)

playlist_data

"""video ids"""

#video ids
def get_video_ids(youtube,playlist_id):
  request=youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id0,
            maxResults=50)

  response = request.execute()

  video_ids=[]
  for i in range(len(response['items'])):
     video_ids.append(response['items'][i]['contentDetails']['videoId'])
     next_page_token=response.get('nextPageToken')
     more_pages=True
  while more_pages:
    if next_page_token is None:
      more_pages=False
    else:
      request=youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token)
      response = request.execute()

    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])
    next_page_token = response.get('nextPageToken')

  return video_ids

video_ids=get_video_ids(youtube,playlist_id0)

video_ids

"""VIDEO DETAILS"""

#video_details
def get_video_details(youtube,video_ids):
  all_video_stats=[]

  for i in range(0,len(video_ids),50):
       request=youtube.videos().list(
            part='snippet,statistics',
            id=','.join(video_ids[i:i+50]))
       response = request.execute()

       for video in response['items']:

        video_stats= dict(videoname=video['snippet']['title'],
                          vidoid=video['id'],
                          videodescription=video['snippet']['description'],
                          published_date=video['snippet']['publishedAt'],
                          views=video['statistics']['viewCount'],
                          likes=video['statistics']['likeCount'],
                          dislikes=video['statistics']['favoriteCount'],
                          comments=video['statistics']['commentCount']
                          )
        all_video_stats.append(video_stats)
  return all_video_stats

video_details=get_video_details(youtube,video_ids)

video_data=pd.DataFrame(video_details)

video_data['published_date']=pd.to_datetime(video_data['published_date']).dt.date
video_data['views']=pd.to_numeric(video_data['views'])
video_data['likes']=pd.to_numeric(video_data['likes'])
video_data['dislikes']=pd.to_numeric(video_data['dislikes'])
video_data['comments']=pd.to_numeric(video_data['comments'])
video_data

"""**comments**

"""

#comments
def get_comment_ids(youtube,video_ids):
  for video_id  in video_ids:
    comment_ids = []
    request = youtube.commentThreads().list(
    part='snippet',
    videoId=video_id,
    maxResults=100
    )
    response = request.execute()

    for comment in response['items']:
        comment_stats= dict(author_name=comment['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                          #authorchannel_id=comment['snippet']['topLevelComment']['snippet']['authorChannelId'],
                          videoId=comment['snippet']['topLevelComment']['snippet']['videoId'],
                          comment=comment['snippet']['topLevelComment']['snippet']['textDisplay'],
                          )
        comment_ids.append(comment_stats)
    return comment_ids

comment_details=get_comment_ids(youtube,video_ids)

comment_data=pd.DataFrame(comment_details)

comment_data
#comment_data['comment']=pd.to_numeric(comment_data['comment'])

"""store at mongodb"""

pip install pymongo

from pymongo import MongoClient
import datetime

client = MongoClient("mongodb+srv://kgrsuryateja33:surya12345678@mydb.jjv738i.mongodb.net/?retryWrites=true&w=majority")
mongo_username = 'kgrsuryateja33'
mongo_password = 'surya12345678'

mongo_database='yt_project'
mongo_db=client[mongo_database]

client.test

client.list_database_names()

db=client['yt_project']

data=db['channel_data']

data = channel_data.to_dict(orient='records')

collection = db['channel_data']
collection.insert_many(data)

#documents = collection.find()
#for document in documents:
 #   print(document)

data1=db['video_data']  #video_data

data1 = video_data.to_dict(orient='records')

for item in data1:
    for key, value in item.items():
        if isinstance(value, datetime.date):
            item[key] = datetime.datetime.combine(value, datetime.datetime.min.time())

collection = db['video_data']
collection.insert_many(data1)

#documents = collection.find()
#for document in documents:
 #   print(document)

data2=db['comment_data']

data2 = comment_data.to_dict(orient='records')

collection = db['comment_data']
collection.insert_many(data2)

#documents = collection.find()
#for document in documents:
 #  print(document)

data3=db['playlist_data']   #playlist_data

data3 = playlist_data.to_dict(orient='records')

collection = db['playlist_data']
collection.insert_many(data3)

#documents = collection.find()
#for document in documents:
 #   print(document)

""" **Migrate data to sqlite**"""

import pymongo
import sqlite3

# Connect to MongoDB
client = MongoClient("mongodb+srv://kgrsuryateja33:surya12345678@mydb.jjv738i.mongodb.net/?retryWrites=true&w=majority")
db =client['yt_project']

mongo_collection1 = db['channel_data']
mongo_collection2 = db['video_data']
mongo_collection3 = db['comment_data']
mongo_collection4 = db['playlist_data']


# Retrieve data from MongoDB
mongo_channeldata = list(mongo_collection1.find())
mongo_videodata = list(mongo_collection2.find())
mongo_commentdata = list(mongo_collection3.find())
mongo_playlistdata = list(mongo_collection4.find())

# Connect to SQLite
sqlite_conn = sqlite3.connect('example.db')
sqlite_cursor = sqlite_conn.cursor()

# Create the playlist table in SQLite
sqlite_cursor.execute('''
    CREATE TABLE IF NOT EXISTS channel (
        channel_name VARCHAR(255),
        subscribers INTEGER,
        views INTEGER,
        playlist_id VARCHAR(255),
        total_videos INTEGER
    )
''')

sqlite_cursor.execute('''
   CREATE TABLE IF NOT EXISTS video (
        videoname VARCHAR(255),
        vidoid VARCHAR(255),
        videodescription TEXT,
        published_date DATETIME,
        views INTEGER ,
        likes INTEGER,
        dislikes INTEGER,
        comments TEXT
    )
''')
sqlite_cursor.execute('''
    CREATE TABLE IF NOT EXISTS comment(
        author_name VARCHAR(255),
        videoId VARCHAR(255),
        comment TEXT
    )
''')

sqlite_cursor.execute('''
    CREATE TABLE IF NOT EXISTS playlist (
        channel_id VARCHAR(255),
        playlist_id VARCHAR(255),
        playlist_name VARCHAR(255)
    )
''')

# Migrate data to SQLite
for data in mongo_channeldata:                                        # we used channe_d
    sqlite_cursor.execute('''
        INSERT INTO channel (channel_name, subscribers, views, playlist_id, total_videos)
        VALUES (?, ?, ?, ?, ?)
    ''', (data['channel_name'], data['subscribers'], data['views'], data['playlist_id'], data['total_videos']))

for data in mongo_videodata:
    sqlite_cursor.execute('''
        INSERT INTO video (videoname, videodescription, published_date, views, likes, dislikes, comments)
       VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (data['videoname'], data['videodescription'], data['published_date'], data['views'], data['likes'], data['dislikes'], data['comments']))

for data in mongo_commentdata:
    sqlite_cursor.execute('''
        INSERT INTO comment (author_name, videoId, comment)
        VALUES (?, ?, ?)
    ''', (data['author_name'], data['videoId'], data['comment']))

for data in mongo_playlistdata:
    sqlite_cursor.execute('''
        INSERT INTO playlist (channel_id, playlist_id, playlist_name)
        VALUES (?, ?, ?)
    ''', (data['channel_id'], data['playlist_id'], data['playlist_name']))

# Commit changes and close connections
sqlite_conn.commit()
sqlite_conn.close()
client.close()

sqlite_conn = sqlite3.connect('example.db')
sqlite_cursor = sqlite_conn.cursor()


# Print channel_d table
sqlite_cursor.execute("SELECT * FROM channel")
channel_rows = sqlite_cursor.fetchall()
print("channel table:")
for row in channel_rows:
    print(row)

# Print video_d table
sqlite_cursor.execute("SELECT * FROM video")
video_rows = sqlite_cursor.fetchall()
print("video table:")
for row in video_rows:
    print(row)

# Print comment_d table
sqlite_cursor.execute("SELECT * FROM comment")
comment_rows = sqlite_cursor.fetchall()
print("comment table:")
for row in comment_rows:
    print(row)

# Print playlist_d table
sqlite_cursor.execute("SELECT * FROM playlist")
playlist_rows = sqlite_cursor.fetchall()
print("playlist table:")
for row in playlist_rows:
    print(row)

sqlite_conn.close()

#sqlite_conn = sqlite3.connect('example.db')
#sqlite_cursor = sqlite_conn.cursor()

#sqlite_cursor.execute("PRAGMA table_info(channel)")
#columns = sqlite_cursor.fetchall()
#print(columns)
#sqlite_conn.close()

"""**streamlit application**"""

!pip install streamlit
!pip install db-sqlite3
!pip install pyngrok --upgrade

# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py
# from pyngrok import ngrok
# import subprocess
# import streamlit as st
# import sqlite3
# 
# sqlite_conn = sqlite3.connect('example.db')
# sqlite_cursor = sqlite_conn.cursor()
# 
# def retrieve_channel_details(channel_id):
#     sqlite_cursor.execute("""
#         SELECT channel_name, subscribers, views, playlist_id, total_videos
#         FROM channel
#         WHERE channel_name = ?
#     """, (channel_id,))
#     channel_details = sqlite_cursor.fetchone()
# 
#     return channel_details
# 
# def retrieve_video_details(video_id):
#     sqlite_cursor.execute("""
#         SELECT videoname, vidoid, videodescription, published_date, views, likes, dislikes, comments
#         FROM video
#         WHERE views = ?
#     """, (video_id,))
#     video_details = sqlite_cursor.fetchone()
#     return video_details
# 
# def retrieve_comment_details(video_id):
#     sqlite_cursor.execute("""
#         SELECT author_name, videoId, comment
#         FROM comment
#         WHERE video_id = ?
#     """, (video_id,))
#     comment_details = sqlite_cursor.fetchone()
#     return comment_details
# 
# def retrieve_playlist_details(playlist_id):
#     sqlite_cursor.execute("""
#         SELECT channel_id, playlist_id, playlist_name
#         FROM playlist
#         WHERE playlist_id = ?
#     """, (playlist_id,))
#     playlist_details = sqlite_cursor.fetchone()
#     return playlist_details
# 
# def main():
#     st.title("YouTube Channel Data Analysis")
# 
#     # User input for YouTube channel ID
#     channel_id = st.text_input("Enter YouTube Channel ID")
# 
#     # Button to retrieve channel details
#     if st.button("Retrieve Channel Details"):
#         channel_details = retrieve_channel_details(channel_id)
#         if channel_details is not None:
#             st.write("Channel Name:", channel_details[0])
#             st.write("Subscribers:", channel_details[1])
#             st.write("Views:", channel_details[2])
#             st.write("Playlist ID:", channel_details[3])
#             st.write("Total Videos:", channel_details[4])
#         else:
#             st.write("Channel not found.")
# 
#     # User input for video ID
#     video_id = st.text_input("Enter Video ID")
# 
#     # Button to retrieve video details
#     if st.button("Retrieve Video Details"):
#         video_details = retrieve_video_details(video_id)
#         if video_details is not None:
#             st.write("Video Name:", video_details[0])
#             st.write("Video ID:", video_details[1])
#             st.write("Video Description:", video_details[2])
#             st.write("Published Date:", video_details[3])
#             st.write("Views:", video_details[4])
#             st.write("Likes:", video_details[5])
#             st.write("Dislikes:", video_details[6])
#             st.write("Comments:", video_details[7])
#         else:
#             st.write("Video not found.")
# 
#     sqlite_conn.close()
# 
# # Run the main function
# if __name__ == "__main__":
#     main()
#

!ls

!ngrok authtoken 2RSYaDxS4EWqbhfXoNjf1Q5yIUD_6d7nZvZSWupeccbx47GKM

!ngrok

from pyngrok import ngrok

#!nohub streamlit run app.py
!streamlit run app.py&>/dev/null&

!pgrep streamlit

publ_url =ngrok.connect(8501)

publ_url

#shutdown
#!kill 56065
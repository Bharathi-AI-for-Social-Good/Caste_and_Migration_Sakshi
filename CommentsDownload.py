import csv
from googleapiclient.discovery import build
import os

API_KEY = os.getenv('YOUTUBE_API_KEY')
# List of YouTube video IDs to fetch comments from
VIDEO_IDS = ['42YwWbstkZk','S6nUbK1GZEE', 'UectBiA0bRc', 'Kl3GRwd_XWU', 'VauuXsOenTM', 'Akz-dG1AYBI', 'GIi64QoxKIc']

def get_youtube_service():
    return build('youtube', 'v3', developerKey=API_KEY)

def get_all_replies(youtube, parent_id):
    replies = []
    request = youtube.comments().list(
        part='snippet',
        parentId=parent_id,
        maxResults=50,
        textFormat='plainText'
    )
    while request:
        response = request.execute()
        for item in response['items']:
            reply_text = item['snippet']['textDisplay']
            replies.append(reply_text)
        request = youtube.comments().list_next(request, response)
    return replies

def get_all_comments(video_id):
    youtube = get_youtube_service()
    all_comments = []

    request = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=1000,
        textFormat='plainText'
    )

    while request:
        response = request.execute()

        for item in response['items']:
            top_comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            all_comments.append(top_comment)

            comment_id = item['snippet']['topLevelComment']['id']
            replies = get_all_replies(youtube, comment_id)
            all_comments.extend(replies)

            if len(all_comments) >= 1500:
                break

        request = youtube.commentThreads().list_next(request, response)

    return all_comments

def save_to_single_column_csv(comments, filename='youtube_comments.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Comment'])
        for comment in comments:
            writer.writerow([comment])

if __name__ == '__main__':
    all_comments = []
    for video_id in VIDEO_IDS:
        print(f"Fetching from video: {video_id}")
        comments = get_all_comments(video_id)
        all_comments.extend(comments)

    save_to_single_column_csv(all_comments)
    print("Saved comments and replies to 'youtube_comments.csv'")

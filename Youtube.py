from googleapiclient.discovery import build
import pandas as pd

api_key = "YOUR_API_KEY"
youtube = build("youtube", "v3", developerKey=api_key)

data = []


search_response = youtube.search().list(
    q="Spotify Premium Review", # Search for videos with this search term (Change if needed)
    part="snippet",
    type="video",
    maxResults=20,  # Fetch XX number of videos (Change if needed)
    publishedAfter="2024-01-01T00:00:00Z" # Only pick videos uploaded after this date (Change date or comment this line if needed)
).execute()

# Get each video ID and fetch comments
for item in search_response["items"]:
    video_id = item["id"]["videoId"]
    video_title = item["snippet"]["title"]
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        comments_response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100, # Number of comments to fetch per video
            textFormat="plainText"
        ).execute()

        for comment_thread in comments_response["items"]:
            comment = comment_thread["snippet"]["topLevelComment"]["snippet"]["textDisplay"]

            # Append data as a dictionary
            data.append({
                "platform": "YouTube",
                "video_title": video_title,
                "video_url": video_url,
                "comment": comment,
                "date": pd.to_datetime(comment_thread["snippet"]["topLevelComment"]["snippet"]["publishedAt"]).strftime('%d/%m/%Y'),
            })

    except Exception as e:
        print(f"Could not retrieve comments for video {video_id}: {e}")

# Create a DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv("youtube_comments.csv", index=False)
print("CSV file saved as youtube_comments.csv")

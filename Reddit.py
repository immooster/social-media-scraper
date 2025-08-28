import praw
import pandas as pd

reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    user_agent="myScraper"
)

data = []

# Change subreddit and search terms
subreddits = ["Spotify"]
search_terms = ["Spotify Premium", "Spotify review", "Spotify ads"]

for subreddit_name in subreddits:
    subreddit = reddit.subreddit(subreddit_name)
    for term in search_terms:
        for post in subreddit.search(term, limit=5): # Limit to XX number of posts per search (Change if needed)
            post.comments.replace_more(limit=0)
            for comment in post.comments.list():
                data.append({
                    "platform": "Reddit",
                    "subreddit": subreddit_name,
                    "search_term": term,
                    "post_title": post.title,
                    "comment_body": comment.body,
                    "comment_score": comment.score,
                    "comment_author": str(comment.author),
                    "date": pd.to_datetime(comment.created_utc, unit='s').strftime('%d/%m/%Y'),
                })

# Convert to DataFrame and save CSV
df = pd.DataFrame(data)


# Drop cell if any comment is deleted or removed
df = df[~df['comment_body'].str.contains('\[deleted\]', na=False)]
df = df[~df['comment_body'].str.contains('\[removed\]', na=False)]

# Drop cell if the date is before a certain date
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df[df['date'] >= '2024-01-01'] # Change date or comment this section if needed

# Save DataFrame to CSV
df.to_csv("reddit_posts.csv", index=False)
print("Saved Reddit posts to reddit_posts.csv")

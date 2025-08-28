import pandas as pd
from langdetect import detect, LangDetectException

def is_english(text):
    try:
        return detect(str(text)) == 'en'
    except LangDetectException:
        return False

reddit_df = pd.read_csv("reddit_posts.csv")
youtube_df = pd.read_csv("youtube_comments.csv")

# Standardise Reddit
reddit_cleaned = reddit_df.rename(columns={
    "post_title": "title",
    "comment_body": "comment",
    "subreddit": "source",
    "search_term": "search_term",
})[["platform", "source", "search_term", "title", "comment", "comment_score", "comment_author", "date"]]

# Standardise YouTube
youtube_cleaned = youtube_df.rename(columns={
    "video_title": "title",
    "comment": "comment",
    "video_url": "url"
})[["platform", "title", "url", "comment", "date"]]

# Normalise columns across all
combined_df = pd.concat([
    reddit_cleaned,
    youtube_cleaned.assign(source="YouTube"),
], ignore_index=True)[["platform", "source", "title", "comment", "date"]]

combined_df["text"] = combined_df.apply(
    lambda row: (
        (str(row["title"]) + " " + str(row["comment"]))
        if row["source"] in ["sitejabber", "uk.trustpilot"]
        else str(row["comment"])
    ),
    axis=1
)

# Filter to keep only English-language entries
combined_df = combined_df[combined_df["text"].apply(is_english)]

# Remove duplicates based on title and comment
combined_df.drop_duplicates(subset=["title", "comment"], inplace=True)

# Remove the helper column
combined_df = combined_df.drop(columns=["title", "comment"])

combined_df.to_csv("combined_reviews.csv", index=False, encoding="utf-8-sig")
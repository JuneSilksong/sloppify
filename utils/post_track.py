import os
import json

PROCESSED_POSTS_FILE = "processed_posts_tts.json"

def load_processed_posts():
    """
    Load the dictionary of processed posts from disk.
    Returns an empty dict if the file does not exist.
    """
    if os.path.exists(PROCESSED_POSTS_FILE):
        with open(PROCESSED_POSTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_processed_posts(processed_posts):
    """
    Save the processed posts dictionary to disk.
    """
    with open(PROCESSED_POSTS_FILE, "w", encoding="utf-8") as f:
        json.dump(processed_posts, f, ensure_ascii=False, indent=2)


def is_post_processed(post_id: str) -> bool:
    """
    Check if the given post_id has already been processed.
    """
    posts = load_processed_posts()
    return post_id in posts


def mark_post_as_processed(post_id: str):
    """
    Mark the given post_id as processed and persist the change.
    """
    posts = load_processed_posts()
    posts[post_id] = True
    save_processed_posts(posts)

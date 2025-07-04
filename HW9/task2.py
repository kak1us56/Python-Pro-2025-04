import requests
import json
from collections import Counter
from typing import Any

# Task 2

BASE_URL = "https://jsonplaceholder.typicode.com"

class Comment:
    def __init__(self, id: int, post_id: int, name: str, email: str, body: str):
        self.id = id
        self.post_id = post_id
        self.name = name
        self.email = email
        self.body = body

class CommentModerator:
    def __init__(self):
        self.comments: list[Comment] = []
        self.flagged_comments: list[Comment] = []

    def fetch_comments(self):
        comments_url = f"{BASE_URL}/comments"

        try:
            all_comments = requests.get(comments_url).json()
            self.comments = [Comment(c["postId"], c["id"], c["name"], c["email"], c["body"]) for c in all_comments]
        except requests.exceptions.RequestException as e:
            print(e)
            return

    def flag_suspicious_comments(self):
        flagged = []
        suspicious_words = ["buy", "discount", "offer", "free"]

        for comment in self.comments:
            body = comment.body.lower()

            keyword_found = any(word in body for word in suspicious_words)

            if keyword_found:
                flagged.append(comment)

        self.flagged_comments = flagged

    def group_by_post(self) -> dict[int, list[Comment]]:
        grouped ={}

        for comment in self.flagged_comments:
            if comment.post_id not in grouped:
                grouped[comment.post_id] = []
            grouped[comment.post_id].append(comment)

        return grouped

    def top_spammy_emails(self, n: int = 5) -> list[Any]:
        email_counts = Counter()

        for comment in self.flagged_comments:
            email_counts[comment.email] += 1

        return email_counts.most_common(n)

    def export_flagged_to_json(self, filename: str = "flagged_comments.json"):
        data_to_export = [
            {
                "id": c.id,
                "postId": c.post_id,
                "name": c.name,
                "email": c.email,
                "body": c.body
            }
            for c in self.flagged_comments
        ]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data_to_export, f, ensure_ascii=False, indent=2)

a = CommentModerator()
a.fetch_comments()
a.flag_suspicious_comments()
a.export_flagged_to_json()
print(a.flagged_comments)
print(a.group_by_post())
print(a.top_spammy_emails())
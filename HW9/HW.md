# TASK 1
```python
"""
TASK 1: Fetch and Analyze User Posts

you are tasked with building a mini analytics tool for a fake blog platform using the JSONPlaceholder API

- fetch all users from https://jsonplaceholder.typicode.com/users
- for each user, fetch their posts from https://jsonplaceholder.typicode.com/posts?userId={user_id}
- create a class `User` that stores the user's ID, name, and their posts
- each post should be represented by a `Post` class
- for each user, compute and store the average length of their post titles and bodies
- implement a method that returns the user with the longest average post body length
- implement a method that returns all users who have written more than 5 posts with titles longer than 40 characters
"""

BASE_URL = "https://jsonplaceholder.typicode.com"

class Post:
    def __init__(self, id: int, title: str, body: str):
        self.id = id
        self.title = title
        self.body = body

class User:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.posts: list[Post] = []

    def add_post(self, post: Post):
        pass

    def average_title_length(self) -> float:
        pass

    def average_body_length(self) -> float:
        pass

class BlogAnalytics:
    def __init__(self):
        self.users: list[User] = []

    def fetch_data(self):
        pass

    def user_with_longest_average_body(self) -> User:
        pass

    def users_with_many_long_titles(self) -> list[User]:
        pass

```

# TASK 2
```python
"""
TASK 2: Comment Moderation System

you're building a simple backend moderation system for post comments

- fetch all comments from https://jsonplaceholder.typicode.com/comments
- create a class `Comment` to store comment data
- build a class `CommentModerator` with methods to:
    - identify comments containing suspicious content (e.g., includes words like "buy", "free", "offer", or repeated exclamation marks)
    - group flagged comments by postId
    - provide a summary report: number of flagged comments per post, and a global list of the top 5 most spammy emails (authors of flagged comments)
- the system should support exporting flagged comments to a local JSON file called `flagged_comments.json`
- handle HTTP errors gracefully and skip any malformed data entries
"""

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
        pass

    def flag_suspicious_comments(self):
        pass

    def group_by_post(self) -> dict[int, list[Comment]]:
        pass

    def top_spammy_emails(self, n: int = 5) -> list[str]:
        pass

    def export_flagged_to_json(self, filename: str = "flagged_comments.json"):
        pass

```

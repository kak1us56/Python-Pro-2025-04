import requests

# Task 1
BASE_URL = "https://jsonplaceholder.typicode.com"

class Post:
    def __init__(self, id: int or None, title: str, body: str):
        self.id = id
        self.title = title
        self.body = body

class User:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.posts: list[Post] = self.get_posts()

    def get_posts(self):
        post_url = f"{BASE_URL}/posts?userId={self.id}"
        posts = requests.get(post_url).json()
        return [Post(p["id"], p["title"], p["body"]) for p in posts]

    def add_post(self, post: Post):
        payload = {
            "userId": self.id,
            "title": post.title,
            "body": post.body
        }

        response = requests.post(f"{BASE_URL}/posts", json=payload)
        result = response.json()

        self.posts.append(Post(result["id"], result["title"], result["body"]))

    def average_title_length(self) -> float:
        sum_title_length = 0

        for post in self.posts:
            sum_title_length += len(post.title)

        average_title_length = sum_title_length / len(self.posts)
        return average_title_length


    def average_body_length(self) -> float:
        sum_body_length = 0

        for post in self.posts:
            sum_body_length += len(post.body)

        average_body_length = sum_body_length / len(self.posts)
        return average_body_length


Leanne = User(1, "Leanne Graham")
print(Leanne.average_body_length())
Leanne.add_post(Post(None, "Leanne Graham", "Leanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne GrahamLeanne Graham"))
print(Leanne.average_body_length())

class BlogAnalytics:
    def __init__(self):
        self.users: list[User] = []

    def fetch_data(self):
        users_url = f"{BASE_URL}/users"
        all_users = requests.get(users_url).json()

        self.users = [User(u["id"], u["name"]) for u in all_users]

    def user_with_longest_average_body(self) -> User:
        user_with_longest_average_body = self.users[0]

        for user in self.users:
            if user.average_body_length() > user_with_longest_average_body.average_body_length():
                user_with_longest_average_body = user

        return user_with_longest_average_body

    def users_with_many_long_titles(self) -> list[User]:
        users_with_many_long_titles = []

        for user in self.users:
            user_posts = requests.get(f"{BASE_URL}/posts?userId={user.id}").json()
            amount_posts = 0

            for user_post in user_posts:
                if len(user_post["title"]) > 40:
                    amount_posts += 1

            if amount_posts > 5:
                users_with_many_long_titles.append(user)

        return users_with_many_long_titles

p = BlogAnalytics()
p.fetch_data()
print(p.users_with_many_long_titles())
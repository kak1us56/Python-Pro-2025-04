# SRP
```python
# class UserManager:
#     def create_user(self, data):
#         self.save_to_database()
#         self.send_welcome_message(data["email"])

#     def save_to_database(self):
#         pass

#     def send_welcome_message(self, email: str):
#         pass


class UserRepository:
    def save(self, data): ...


class MailingService:
    def send_welcome_message(self, message): ...


class UserManager:
    def __init__(self, repo: UserRepository, mailing_service: MailingService) -> None:
        self.repo: UserRepository = repo
        self.mailing: MailingService = mailing_service

    def create_user(self, data):
        self.repo.save(data)
        self.mailing.send_welcome_message(data)


def main():
    repo = UserRepository()
    mailing = MailingService()

    manager = UserManager(repo, mailing)
    manager.create_user({...})
```


# Liskov
```python
class A:
    def foo(self, x: str):
        print("foo from A")


class B(A):
    def foo(self, x: int):
        print("foo from B")


def process(instance: A):
    instance.foo(x="12")


def main():
    instance = B()
    process(instance)


main()

```

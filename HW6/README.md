# AGENDA

- What are compound statements in Python?
  - Introduction to control flow in Python
  - Overview of compound statement types
- `if/elif/else` statements
- `match/case` statements (pattern matching in Python 3.10+)
- `for` and `while` loops
- `with` statement and context managers
- `yield` and generator functions
- `try/except/finally` for exception handling
- Improve project with compound statements
- How Python’s approach compares to other languages (briefly)
- CPython exceptions
- Imrove existing project

# Links

- [Generators](https://python.plainenglish.io/python-generators-when-to-use-59a96ec933ec)
- https://refactoring.guru/design-patterns/iterator
- https://realpython.com/python-iterators-iterables
- https://pythongeeks.org/python-generators-vs-iterators
- https://towardsdatascience.com/mastering-iterators-and-generators-in-python-ca30939d962

## Other materials

1. Python documentation on `contextlib` module: The `contextlib` module in Python provides utilities for working with context managers. It contains the necessary functions and classes for creating and using context managers. You can find the documentation at:
   - [https://docs.python.org/3/library/contextlib.html](https://docs.python.org/3/library/contextlib.html)
2. Real Python - "Python Context Managers and the "`with`" Statement" tutorial: This tutorial from the Real Python website explains the concept of context managers in Python and how to use the `with` statement effectively. It provides code examples and practical use cases.
   - [https://realpython.com/python-with-statement/](https://realpython.com/python-with-statement/)
3. Python documentation on `with` statement: The official Python documentation explains the `with` statement in detail and how it works in conjunction with context managers. You can find the documentation at:
   - [https://docs.python.org/3/reference/compound_stmts.html#the-with-statement](https://docs.python.org/3/reference/compound_stmts.html#the-with-statement)
4. Python contextlib - Context Manager Types: This section of the Python documentation covers the various context manager types available in the contextlib module. It includes examples and explanations of each type.
   - [https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager](https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager)

# LESSON MATERIALS

### status code match/case

```python
status_code: int = 300

match status_code:
    case 200 | 300:
        print("OK")
    case 400:
        print("Bad Request")
    case 500:
        print("Server Error")
    case _:
        print("Unknown error")
```

### points match/case

```python
piont: tuple[float, float] = (12.3, 89.2)

match point:
    case (0, 0):
        print("Zero point")
```

### while, iterator

```python
users = ["john", "marry"]
iterator = iter(users)


while True:
    try:
        print(next(iterator))
        # iterator.__next__()
    except StopIterationError:
        break

for user in users:
    print(user)
```

### context manager PoC

```python
import requests


class OpenAIClient:
    def __init__(self):
        self._client: requests.Client | None = None

    def __enter__(self):
        self._client = requests.Client(base_url="https://openai.com/api/v1/chat")
        return self

    def __exit__(self):
        self._client.close()

    @property
    def client(self) -> requests.Client:
        if self._client is None:
            raise Exception("Client is not initialized")
        else:
            return self._client

    def get_complition(self):
        response = self.client.chat("Who is Tim?")
        return response.text



with OpenAIClient() as client:
    result = client.get_complition()
```

### generators

#### files reading

```python
def read_file(filename: str):
    with open(filename) as file:
        while (line := file.readline()) is not None:
            yield line


for line in read_file("rockyou.txt"):
    print(line)
```

#### gen id

```python
students = {
    1: "John",
    2: "Marry",
}


def get_next_id():
    used_ids: set = set(students.keys())

    while True:
        id_ = max(used_ids) + 1
        used_ids.add(id_)

        yield id_

id_gen = get_next_id()

def add(name: str):
    students[next(id_gen)] = name

    students[next(id_gen)] = name


add("Mark")

print(students)
```

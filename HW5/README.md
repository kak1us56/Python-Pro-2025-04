# FRAME

```python
def foo(arg: int):
    # ...
    age: int = 31
    frame = inspect.currentframe()
    print(frame.f_globals)
    print(frame.f_locals)
```

# ENCLOSING

```python
x = 1


def counter():
    global x
    count = 0

    def increment():
        nonlocal count

        count += 1
        return count

    return increment


inc = counter()
print(inc())
print(inc())
```


# DECORATOR FOR HTML
```python
def italic(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"<i>{result}</i>"

    return wrapper

def bold(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return f"<b>{result}</b>"

    return wrapper


@bold
@italic
def greeting():
    return "Hello!"


print(greeting())
```


# Price example

```python
from typing import Any


class Price:
    def __init__(self, value: int, currency: str):
        self.value: int = value
        self.currency: str = currency

    def __add__(self, other: Any) -> "Price":
        if not isinstance(other, Price):
            raise ValueError("Can perform operations only with `Price` objects")
        else:
            if self.currency != other.currency:
                raise ValueError("Currencies must match")
            else:
                return Price(self.value + other.value, self.currency + other.currency)


phone = Price(500, "usd")
tablet = Price(800, "uah")

total: Price = phone + tablet
print(f"{total.value} {total.currency}")
```

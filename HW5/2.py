def foo():
    print("I am foo")


def caller(func, *args, **kwargs):
    result = func(*args, **kwargs)
    print(f"Function {func.__name__} returned {result}")

caller(foo)
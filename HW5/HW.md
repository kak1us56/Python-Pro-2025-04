# Price Class

- Implement a `Price` class:
  - Two `Price` instances (with the same currency) must support addition and subtraction.
  - (Optional) If currencies differ, apply middle ("CHF") conversion logic.
  - The result currency must match `self` (the left operand).
  - If `a.currency != b.currency`, both convert to "CHF", sum/subtract, then convert back to `a.currency`

**Example:**

```python
a = Price(100, "USD")
b = Price(150, "USD")
c = a + b      # 250 USD
d = b - a      # 50 USD
```

# Authorization Decorator (optional)

```python
"""
About the code:

`users` list includes multiple users (define them by yourself)
`command()` is only a single function that mimics the business logic
`auth()` is a decorator that requires user authorization to perform tasks


NOTES
"""

class User:
    username: str
    password: str
users = [
    User(...),
    # ...
]

def auth():
    # TODO: complete the decorator

@auth
def command(payload):
	print(f"Executing command by authorized user.\nPayload: {payload}")

while user_input := input("Enter anything: "):
    command(user_input)
```

**TASK:**

- complete ONLY the `auth()` decorator. other code changes are also available but not required
- if the function is decorated with `auth` - the application requires `username` and `password` to be entered by user (think about UX by yourself)
  - ASK for credentials UNTIL they are NOT CORRECT
  - IF credentials are CORRECT - EXECUTE the command (actually just prints the command)
  - IF User has entered credentials CORRECTLY once - it is CACHED and used to call future commands WITHOUT additional AUTHORIZATION

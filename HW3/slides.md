# PLAN

- iteration 0. business idea
- iteration 1. project details
- iteration ...
- iteration 8. optimization

---

# ITERATION 0. BUSINESS IDEA

<br>

## ISSUE

create a digital solution to managing students and their marks

## SOLUTION

CLI (command-line interface)

---

# ITERATION 1. POC. MVP

<br>

## Proof of Concept (hypothesis)

- improve teaches efficiency
- market

## Minimum Viable Product

- what kind of data?
- performance limitations?
- view (UI)
- technical stack
  - python3.12
- define the backlog (_features list / implementation plan / estimation_)

---

# ITERATION 2. PROVIDE USER INTERFACE

<br>

## ISSUE

there is no user interface

## SOLUTION

use infinite polling and _CLI prompt_ to interact with user

## POC

```py
while True:
    user_command = input("enter the command...")

    match user_command:
        case "show students":
            ...
        case "add student":
            ...
        case "quit":
            raise SystemExit(1)
        case _:
            raise NotImplementedError("command not found")
```

---

# ITERATION 3. FEATURE REQUEST

<br>

## ISSUE

we need to stored some detailed about each student in our system

## SOLUTION

update the internal `student` data structure with `info` field

---

# ITERATION 4. FEATURE REQUEST

<br>

## ISSUE

_too much information on a display 😖_

## SOLUTION

create another function to get the 'rich' information about student

_common function names for such tasks:_

- `get(identified)`
- `retrieve(identified)`
- `detail(identified)`
- `details(identified)`

---

# ITERATION 5. FIXING BUG

<br>

## ISSUE

what if students have _similar names_ (aka similar identifiers in our data structure)?

## SOLUTION

`Student.id` unique parameter

## POC

```python
data = [
    {
        "id": 1,  # unique
        # ...
    },
    {
        "id": 2,  # unique
        # ...
    },
]
```

---

# ITERATION 6. FEATURE REQUEST

<br>

## ISSUE

no way to remove student from journal

## SOLUTION

- search for item
- remove the item (change the state of the storage)

_common function names for such tasks:_

- `del(identified)` - conflicts with built-in `del` function
- `delete(identified)`
- `remove(identified)`
- `destroy(identified)`

---

# ITERATION 7. FEATURE REQUEST

<br>

## ISSUE

- user is not mutable
  - adding marks
- feature place / naming dilema...
  - adding marks is updating the student or separate feature
  - data perspective, feature perspective, user perspective

## SOLUTION

find and update the item in the storage

_common function names for such tasks:_

- `update(identified, data)`
- `change(identified, data)`
- `modify(identified, data)`
- `alter(identified, data)`
- `edit(identified, data)`

---

# ITERATION 8. FEATURE REQUEST (HOMEWORK)

<br>

## ISSUE

can't easily add marks for students

## SOLUTION

managing marks is separate from managing students

---

# ITERATION 9. OPTIMIZATION

<br>

## ISSUE

- ~code sucks~
- the code is unreadable and some data structures are not optimal.

## SOLUTION

improve the storage with more efficient data structure ( `list` -> `dict` )

remove the id from the `Student` representation

---

# ITERATION 10. EXTENDING STUCTURE

<br>

## ISSUE

- `marks` represent only a single subject
  - how to know what this mark belongs to?

## SOLUTION

use `dict[str, list[int]]` instead of `list[int]`

## POC

```python
marks = {
    "math": [...],
    "chemistry": [...],
    "biology": [...]
    ...
}
```

---

# ITERATION 11. NEXT STEPS

<br>

## PROBLEM

parser does not allow us to get the 'detailed information' about Student

## SOLUTION

update the parser

```python
...
    def _parse(data):
        separator_indexes = []

        for index, char in enumerate(data):
            if char == ";":
                separator_indexes += [index]

        # if len(separator_indexes) == 1, then we don't have an `info`
        # else we do have

        ...
```

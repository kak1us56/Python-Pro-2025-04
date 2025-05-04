"""
1. Application - Python
2. User - Teacher in the scool
3. Iterface - TUI (Terminal User Interface)


struct Student:
    name: str
    marks: list[int]

struct Teacher: no structure since authentication process

========================
DATA TYPES
========================
- mutability
    - immutable
        - int, tuple, str
    - mutable
        - list, dict, set
- collection?
    - list, tuple, set, dict, str, byte
    - container / flat


- list : ``dynamic array`` (1.125 * len(self)). universal
- tuple : ``array``. memory
- dict / set: ``hashmap``. fast operations. size?
"""

import operator
from typing import Any

# ─────────────────────────────────────────────────────────
# STORAGE SIMULATION
# ─────────────────────────────────────────────────────────
storage: list[dict] = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "marks": [7, 8, 9, 10, 6, 7, 8],
        "info": "Alice Johnson is 18 y.o. Interests: math",
    },
    {
        "id": 2,
        "name": "Michael Smith",
        "marks": [6, 5, 7, 8, 7, 9, 10],
        "info": "Michael Smith is 19 y.o. Interests: science",
    },
    {
        "id": 3,
        "name": "Emily Davis",
        "marks": [9, 8, 8, 7, 6, 7, 7],
        "info": "Emily Davis is 17 y.o. Interests: literature",
    },
    {
        "id": 4,
        "name": "James Wilson",
        "marks": [5, 6, 7, 8, 9, 10, 11],
        "info": "James Wilson is 20 y.o. Interests: sports",
    },
    {
        "id": 5,
        "name": "Olivia Martinez",
        "marks": [10, 9, 8, 7, 6, 5, 4],
        "info": "Olivia Martinez is 18 y.o. Interests: art",
    },
    {
        "id": 6,
        "name": "Emily Davis",
        "marks": [4, 5, 6, 7, 8, 9, 10],
        "info": "Daniel Brown is 19 y.o. Interests: music",
    },
    {
        "id": 7,
        "name": "Sophia Taylor",
        "marks": [11, 10, 9, 8, 7, 6, 5],
        "info": "Sophia Taylor is 20 y.o. Interests: physics",
    },
    {
        "id": 8,
        "name": "William Anderson",
        "marks": [7, 7, 7, 7, 7, 7, 7],
        "info": "William Anderson is 18 y.o. Interests: chemistry",
    },
    {
        "id": 9,
        "name": "Isabella Thomas",
        "marks": [8, 8, 8, 8, 8, 8, 8],
        "info": "Isabella Thomas is 19 y.o. Interests: biology",
    },
    {
        "id": 10,
        "name": "Benjamin Jackson",
        "marks": [9, 9, 9, 9, 9, 9, 9],
        "info": "Benjamin Jackson is 20 y.o. Interests: history",
    },
]


# ─────────────────────────────────────────────────────────
# CRUD
# ─────────────────────────────────────────────────────────
def add_student(student: dict) -> dict | None:
    """Try to add another yet student to the storage.

    NOTES:
    The generated id is INCREMENTED from the MAX existing ID.
    """

    # extract ids from storage
    last_id = len(storage)

    # NOTE: performanve improvement with ``operator``
    next_id = max(storage, key=operator.itemgetter("id"))["id"] + 1
    student["id"] = next_id

    if len(student) != 2:
        return None

    if not student.get("name") or not student.get("marks"):
        return None
    else:
        # action
        storage.append(student)
        return student


def show_students():
    print("=========================\n")
    for student in storage:
        print(f"{student['id']}. Student {student['name']}\n")
    print("=========================\n")


def show_student(student: dict) -> None:
    print(
        "=========================\n"
        f"[{student['id']}] Student {student['name']}\n"
        f"Marks: {student['marks']}\n"
        f"Info: {student['info']}\n"
        "=========================\n"
    )


def search_student(student_id: int) -> dict | None:
    for student in storage:
        if student["id"] == student_id:
            return student

    return None


def delete_student(student_id: int) -> None:
    student: dict | None = search_student(student_id)

    if student is None:
        print(f"Student {student_id} not found")
        return

    student_name = student["name"]
    for index, _item in enumerate(storage, 0):
        if _item["id"] == student_id:
            del storage[index]
            print(f"Deleted ")
            return


def update_student(student_id: int, raw_input: str) -> dict | None:
    parsing_result = raw_input.split(";")
    if len(parsing_result) != 2:
        return None

    new_name, new_info = parsing_result

    student: dict | None = search_student(student_id)
    if student is None:
        return None

    student["name"] = new_name
    student["info"] = new_info

    return student


# ─────────────────────────────────────────────────────────
# OPERATIONAL LAYER
# ─────────────────────────────────────────────────────────
def ask_student_payload() -> dict:
    ask_prompt = (
        "Enter student's payload data using text template: "
        "John Doe;1,2,3,4,5\n"
        "where 'John Doe' is a full name and [1,2,3,4,5] are marks.\n"
        "The data must be separated by ';'"
    )

    def parse(data) -> dict:
        name, raw_marks = data.split(";")

        return {
            "name": name,
            "marks": [int(item) for item in raw_marks.replace(" ", "").split(",")],
        }

    user_data: str = input(ask_prompt)
    return parse(user_data)


def student_management_command_handle(command: str):
    if command == "show":
        show_students()
    elif command == "add":
        data = ask_student_payload()
        if data:
            student: dict | None = add_student(data)
            print(f"Student: {student['name']} is added")
        else:
            print("The student's data is NOT correct. Please try again")
    elif command == "search":
        student_id: str = input("\nEnter student's ID: ")
        if student_id:
            student: dict | None = search_student(student_id=int(student_id))
            if student is not None:
                show_student(student)
            else:
                print(f"Student {student_id} not found")
        else:
            print("Student's ID is required to search")
    elif command == "delete":
        student_id: str = input("\nEnter student's ID: ")

        if student_id:
            delete_student(student_id=int(student_id))
        else:
            print("Student's name is required to search")
    elif command == "update":
        student_id: str = input("\nEnter student's ID: ")

        if student_id:
            student: dict | None = search_student(student_id=int(student_id))
            if student is None:
                print(f"Student {student_id} not found")
                return

        show_student(student)
        print(
            f"\n\nTo update user's data, specify `name` and `info`, with `;` separator.\n"
        )

        user_input: str = input("Enter: ")
        updated_student: dict | None = update_student(
            student_id=int(student_id), raw_input=user_input
        )
        if updated_student is None:
            print("Erorr on updating student")
        else:
            print(f"Student {updated_student['name']} is updated")


def handle_user_input():
    OPERATIONAL_COMMANDS = ("quit", "help")
    STUDENT_MANAGEMENT_COMMANDS = ("show", "add", "search", "delete", "update")
    AVAILABLE_COMMANDS = (*OPERATIONAL_COMMANDS, *STUDENT_MANAGEMENT_COMMANDS)

    HELP_MESSAGE = (
        "Hello in the Journal! User the menu to interact with the application.\n"
        f"Available commands: {AVAILABLE_COMMANDS}"
    )

    print(HELP_MESSAGE)

    while True:
        command = input("\n Select command: ")

        if command == "quit":
            print("\nThanks for using the Journal application")
            break
        elif command == "help":
            print(HELP_MESSAGE)
        else:
            student_management_command_handle(command)


# ─────────────────────────────────────────────────────────
# ENTRYPOINT
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    handle_user_input()

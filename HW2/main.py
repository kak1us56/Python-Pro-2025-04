"""
1. Application - Python
2. User - Teacher in the scool
3. Iterface - TUI (Terminal User Interface)


struct Student:
    name: str
    marks: list[int]

struct Teacher: no structure since authentication process
"""

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


# CRUD
def add_student(name: str, marks: list[int], details: str | None = "") -> dict | None:
    if not name:
        return None
    else:
        student_id = max((student["id"] for student in storage), default=0) + 1
        student = {
            "id": student_id,
            "name": name,
            "marks": marks,
            "info": details
        }

        storage.append(student)

        return student


def show_students():
    print("=========================\n")
    for student in storage:
        print(f"{student['id']}. Student {student['name']}\n")
    print("=========================\n")


def search_student(student_id: int) -> None:
    for student in storage:
        info = (
            "=========================\n"
            f"[{student['id']}] Student: {student['name']}\n"
            f"Marks: {student['marks']}\n"
            f"{'Info: ' + student['info'] + '\n' if student.get('info') else ''}"
            "=========================\n"
        )

        if student["id"] == student_id:
            print(info)
            return

    print(f"Student with {student_id} not found")


def ask_student_payload() -> dict:
    ask_prompt = "Enter student's name: "

    def parse(data) -> dict:
        info = ''

        if len(data.split(';')) == 2:
            try:
                name, info = data.split(';')
            except ValueError:
                print("Entered incorrect data")
        else:
            name = data

        added_student = {
            "name": name,
            "marks": [],
        }

        if info != '':
            added_student["info"] = info
        else:
            added_student["info"] = ""

        return added_student


    user_data: str = input(ask_prompt)

    ask_details = input('Do you want to add student details? (y/n): ')

    if ask_details == "y":
        student_info = input("Enter student details: ")
        user_data += ';' + student_info
    else:
        return parse(user_data)

    return parse(user_data)


def student_management_command_handle(command: str):
    if command == "show":
        show_students()
    elif command == "add":
        data = ask_student_payload()
        if data:
            student: dict | None = add_student(data['name'], data['marks'], data['info'])
            print(f"Student: {student['name']} is added")
        else:
            print("The student's data is NOT correct. Please try again")
    elif command == "search":
        student_id: str = input("\nEnter student's ID: ")
        if student_id:
            search_student(student_id=int(student_id))
        else:
            print("Student's name is required to search")


def handle_user_input():
    OPERATIONAL_COMMANDS = ("quit", "help")
    STUDENT_MANAGEMENT_COMMANDS = ("show", "add", "search")
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

def main():
    handle_user_input()

if __name__ == "__main__":
    main()

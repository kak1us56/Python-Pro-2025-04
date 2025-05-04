# ─────────────────────────────────────────────────────────
# STORAGE SIMULATION
# ─────────────────────────────────────────────────────────
storage: dict[int, dict] = {
    1: {
        "name": "Alice Johnson",
        "marks": [7, 8, 9, 10, 6, 7, 8],
        "info": "Alice Johnson is 18 y.o. Interests: math",
    },
    2: {
        "name": "Michael Smith",
        "marks": [6, 5, 7, 8, 7, 9, 10],
        "info": "Michael Smith is 19 y.o. Interests: science",
    },
    3: {
        "name": "Emily Davis",
        "marks": [9, 8, 8, 7, 6, 7, 7],
        "info": "Emily Davis is 17 y.o. Interests: literature",
    },
    4: {
        "name": "James Wilson",
        "marks": [5, 6, 7, 8, 9, 10, 11],
        "info": "James Wilson is 20 y.o. Interests: sports",
    },
    5: {
        "name": "Olivia Martinez",
        "marks": [10, 9, 8, 7, 6, 5, 4],
        "info": "Olivia Martinez is 18 y.o. Interests: art",
    },
    6: {
        "name": "Emily Davis",
        "marks": [4, 5, 6, 7, 8, 9, 10],
        "info": "Daniel Brown is 19 y.o. Interests: music",
    },
    7: {
        "name": "Sophia Taylor",
        "marks": [11, 10, 9, 8, 7, 6, 5],
        "info": "Sophia Taylor is 20 y.o. Interests: physics",
    },
    8: {
        "name": "William Anderson",
        "marks": [7, 7, 7, 7, 7, 7, 7],
        "info": "William Anderson is 18 y.o. Interests: chemistry",
    },
    9: {
        "name": "Isabella Thomas",
        "marks": [8, 8, 8, 8, 8, 8, 8],
        "info": "Isabella Thomas is 19 y.o. Interests: biology",
    },
    10: {
        "name": "Benjamin Jackson",
        "marks": [9, 9, 9, 9, 9, 9, 9],
        "info": "Benjamin Jackson is 20 y.o. Interests: history",
    },
}


# ─────────────────────────────────────────────────────────
# CRUD
# ─────────────────────────────────────────────────────────
def add_student(student: dict) -> dict | None:
    if not student.get("name") or not student.get("marks"):
        return None
    else:
        # action
        next_id = max(storage.keys()) + 1
        storage[next_id] = student
        return student


def show_students():
    print("=========================\n")
    for id_, student in storage.items():
        print(f"{id_}. Student {student['name']}\n")
    print("=========================\n")


def show_student(student: dict) -> None:
    print(
        "=========================\n"
        f"Student {student['name']}\n"
        f"Marks: {student['marks']}\n"
        f"{'Info: ' + student['info'] + '\n' if student.get('info') else ''}"
        "=========================\n"
    )


def update_student(id_: int, raw_input: str) -> dict | None:
    student: dict | None = storage.get(id_)
    if student is None:
        return None

    if raw_input == "name":
        updated_name: str = input("New name: ")
        student["name"] = updated_name

        ask_prompt_update: str = input("Would you like to update the info? [y/n]: ")
        if ask_prompt_update == "y":
            updated_info: str = input("New info: ")
            student["info"] = updated_info
    elif raw_input == "info":
        updated_info: str = input("New info: ")

        if updated_info.strip() in student["info"]:
            student["info"] = student["info"].replace(updated_info.strip(), updated_info.strip())
        elif updated_info.strip() != student["info"]:
            student["info"] += f" | {updated_info.strip()}"
        else:
            student["info"] = updated_info.strip()

        ask_prompt_update: str = input("Would you like to update the name? [y/n]: ")
        if ask_prompt_update == "y":
            updated_name: str = input("New name: ")
            student["name"] = updated_name
    else:
        print("Invalid input")

    return student

def add_marks(student: dict) -> None:
    ask_prompt = (
        "Enter student`s marks, that you want to add, using template: "
        "8,3,12,7,4\n"
        "Marks must be separated by ';'"
    )

    students_marks: str = input(ask_prompt)

    try:
        student["marks"] += [int(item) for item in students_marks.replace(" ", "").split(",")]
        print("Marks were successfully added.")
    except ValueError:
        print("Invalid marks, please try again.")


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
        info = ''

        if len(data.split(';')) == 2:
            name, raw_marks = data.split(";")
        else:
            name, raw_marks, info = data.split(";")

        added_student = {
            "name": name,
            "marks": [int(item) for item in raw_marks.replace(" ", "").split(",")],
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
            student: dict | None = add_student(data)
            if student is None:
                print("Error adding student")
            else:
                print(f"Student: {student['name']} is added")
        else:
            print("The student's data is NOT correct. Please try again")
    elif command == "search":
        student_id: str = input("\nEnter student's ID: ")
        if not student_id:
            print("Student's ID is required to search")
            return

        student: dict | None = storage.get(int(student_id))
        if student is None:
            print("Error adding student")
        else:
            show_student(student)
    elif command == "delete":
        student_id: str = input("\nEnter student's ID: ")
        if not student_id:
            print("Student's id is required to delete")
            return

        id_ = int(student_id)
        if storage.get(id_):
            del storage[id_]

    elif command == "update":
        student_id: str = input("\nEnter student's ID: ")
        if not student_id:
            print("Student ID must be specified for update")
            return

        id_ = int(student_id)
        student: dict | None = storage.get(id_)
        if student is None:
            print(f"Student {student_id} not found")
            return

        show_student(student)
        print(
            f"\n\nWhat would you like to update?\n"
        )

        user_input: str = input("Name or info: ")
        updated_student: dict | None = update_student(id_=id_, raw_input=user_input)

        if updated_student is None:
            print("Error on updating student")
        else:
            print(f"Student {updated_student['name']} is updated")
    elif command == "add marks":
        student_id: str = input("\nEnter student's ID: ")
        if not student_id:
            print("Student's id is required to add marks")
            return

        id_ = int(student_id)
        student: dict | None = storage.get(id_)
        if student is None:
            print(f"Student {student_id} not found")
            return

        add_marks(student)


def handle_user_input():
    OPERATIONAL_COMMANDS = ("quit", "help")
    STUDENT_MANAGEMENT_COMMANDS = ("show", "add", "search", "delete", "update", "add marks")
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

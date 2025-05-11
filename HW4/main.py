import csv
from pathlib import Path
# ─────────────────────────────────────────────────────────
# STORAGE SIMULATION
# ──────────────────────────────────────────────────────

STORAGE_FILE_NAME = Path(__file__).parent.parent / "HW4/storage.csv"


# ─────────────────────────────────────────────────────────
# INFRASTRUCTURE
# ─────────────────────────────────────────────────────────

class Repository:
    """
    RAM: John, Marry, Mark
    SSD: John, Marry
    """
    def __init__(self):
        self.file = open(STORAGE_FILE_NAME, "r")
        self.students = self.get_storage()

        # close after reading

        self.file.close()

    def get_storage(self):
        self.file.seek(0)
        reader = csv.DictReader(self.file, fieldnames=["id", "name", "marks", "info"], delimiter=";")
        next(reader)

        students = []
        for row in reader:
            # Fix: Cleanly parse marks from CSV string
            raw_marks = row["marks"]
            row["marks"] = [mark.strip() for mark in raw_marks.split(",") if mark.strip().isdigit()]
            students.append(row)
        return students

    def add_student(self, student: dict):
        student_id = str(len(self.students) + 1)
        student['id'] = student_id

        student_to_write = {
            'id': student['id'],
            'name': student['name'],
            'marks': ','.join(map(str, student['marks'])),
            'info': student.get('info', ''),
        }

        with open(STORAGE_FILE_NAME, "a", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["id", "name", "marks", "info"], delimiter=";")
            writer.writerow(student_to_write)

        self.students.append(student)

        # self.students.append(student)
        # writer = csv.DictWriter(self.file, fieldnames=["id", "name", "marks", "info"])
        # writer.writerow(student)

    def delete_student(self, student_id: int):
        self.students = [s for s in self.students if s['id'] != str(student_id)]

        with open(STORAGE_FILE_NAME, "w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["id", "name", "marks", "info"], delimiter=";")
            writer.writeheader()
            for student in self.students:
                writer.writerow(student)

    def update_student(self, student_id: str, new_name: str, new_info: str) -> bool:
        updated = False
        for student in self.students:
            if student["id"] == student_id:
                student["name"] = new_name
                student["info"] = new_info
                updated = True
                break

        if updated:
            with open(STORAGE_FILE_NAME, "w", newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["id", "name", "marks", "info"], delimiter=";")
                writer.writeheader()
                for s in self.students:
                    writer.writerow(s)

        return updated

    def add_mark(self, student_id: str, new_marks: list[int]) -> bool:
        updated = False
        for student in self.students:
            if student["id"] == student_id:
                current_marks = student["marks"]
                current_marks += [str(mark) for mark in new_marks]
                student["marks"] = current_marks
                updated = True
                break

        if updated:
            with open(STORAGE_FILE_NAME, "w", newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["id", "name", "marks", "info"], delimiter=";")
                writer.writeheader()
                for s in self.students:
                    writer.writerow({
                        "id": s["id"],
                        "name": s["name"],
                        "marks": ",".join(map(str, s["marks"])),
                        "info": s.get("info", ""),
                    })

        return updated


    # only the idea. we should perform writes only if we know user quit the application
    # better to create: `.save()` and call it on `quit` or any other command that is not covered
    def __del__(self):
        try:
            with open(STORAGE_FILE_NAME, "w", newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["id", "name", "marks", "info"], delimiter=";")
                writer.writeheader()
                for student in self.students:
                    writer.writerow({
                        "id": student.get("id", ""),
                        "name": student.get("name", ""),
                        "marks": ",".join(map(str, student.get("marks", []))),
                        "info": student.get("info", ""),
                    })
        except Exception as e:
            print(f"Warning: Failed to auto-save on exit: {e}")


repo = Repository()

def inject_repository(func):
    def inner(*args, **kwargs):
        return func(*args, repo=repo, **kwargs)

    return inner



# ─────────────────────────────────────────────────────────
# DOMAIN (student, users, notification)
# ─────────────────────────────────────────────────────────
class StudentService:
    def __init__(self):
        self.repository = Repository()

    @inject_repository
    def add_student(self, student: dict, repo: Repository) -> dict | None:
        if not student.get("name") or not student.get("marks"):
            return None

        repo.add_student(student)
        return student

    @inject_repository
    def show_student_by_id(self, student_id: str, repo: Repository):
        student = next((s for s in repo.students if s["id"] == student_id), None)
        if student:
            self.show_student(student)
        else:
            print(f"Student with ID {student_id} not found.")

    @inject_repository
    def show_students(self, repo: Repository):
        print("=========================\n")
        for student in repo.students:
            print(f"{student['id']}. Student {student['name']}\n")
        print("=========================\n")

    @inject_repository
    def delete_student(self, student_id: int, repo: Repository):
        student_exists = any(s['id'] == student_id for s in repo.students)
        if not student_exists:
            return False

        repo.delete_student(student_id)
        return True

    @inject_repository
    def add_mark(self, student_id: str, marks: list[int], repo: Repository) -> bool:
        return repo.add_mark(student_id, marks)

    def show_student(self,student: dict) -> None:
        print(
            "=========================\n"
            f"Student {student['name']}\n"
            f"Marks: {student['marks']}\n"
            f"Info: {student['info']}\n"
            "=========================\n"
        )

    @inject_repository
    def update_student(self, student_id: str, raw_input: str, repo: Repository) -> bool:
        parsing_result = raw_input.split(";")
        if len(parsing_result) != 2:
            return False

        new_name, new_info = parsing_result

        return repo.update_student(student_id, new_name, new_info)


# ─────────────────────────────────────────────────────────
# OPERATIONAL (APPLICATION) LAYER
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
    students_service = StudentService()
    if command == "show":
        students_service.show_students()
    elif command == "add":
        data = ask_student_payload()
        if data:
            student: dict | None = students_service.add_student(data)
            if student is None:
                print("Error adding student")
            else:
                print(f"Student: {student['name']} is added")
        else:
            print("The student's data is NOT correct. Please try again")
    elif command == "add marks":
        student_id = input("\nEnter student's ID: ").strip()
        raw_marks = input("Enter marks to add (comma-separated): ").strip()

        if not student_id or not raw_marks:
            print("Student ID and marks are required.")
            return

        try:
            marks = [int(m.strip()) for m in raw_marks.split(",") if m.strip()]
        except ValueError:
            print("All marks must be valid integers.")
            return

        if not marks:
            print("No valid marks provided.")
            return

        success = students_service.add_mark(student_id, marks)
        if success:
            print(f"Marks {marks} added to student {student_id}.")
        else:
            print(f"Student {student_id} not found.")


    # elif command == "search":
    #     student_id: str = input("\nEnter student's ID: ")
    #     if not student_id:
    #         print("Student's ID is required to search")
    #         return
    #
    #     students = get_storage()
    #
    #     student: dict | None = storage.get(int(student_id))
    #     if student is None:
    #         print("Error adding student")
    #     else:
    #         show_student(student_id, students)
    #         print(f"Student {student_id} not found")
    elif command == "delete":
        student_id: str = input("\nEnter student's ID: ").strip()
        if not student_id:
            print("Student's ID is required to delete")
            return

        success = students_service.delete_student(student_id)
        if success:
            print(f"Student {student_id} deleted successfully.")
        else:
            print(f"Student {student_id} not found.")

    elif command == "show student":
        student_id = input("\nEnter student's ID: ").strip()
        if not student_id:
            print("Student's ID is required to search")
            return

        students_service.show_student_by_id(student_id)

    elif command == "update":
        student_id: str = input("\nEnter student's ID: ").strip()
        if not student_id:
            print("Student ID must be specified for update")
            return

        students = repo.students
        student = next((s for s in students if s["id"] == student_id), None)

        if student is None:
            print(f"Student {student_id} not found")
            return

        # Show current data
        print(
            f"\nCurrent data:\nName: {student.get('name', '')}\nInfo: {student.get('info', '')}\n"
            f"\nTo update, enter new data in format:\nNew name;New info"
        )

        user_input: str = input("Enter: ")
        updated = StudentService().update_student(student_id, user_input)

        if not updated:
            print("Error updating student. Please check your input format.")
        else:
            print(f"Student {student_id} updated successfully.")

    #
    # elif command == "update":
    #     student_id: str = input("\nEnter student's ID: ")
    #     if not student_id:
    #         print("Student ID must be specified for update")
    #         return
    #
    #     id_ = int(student_id)
    #     student: dict | None = storage.get(id_)
    #     if student is None:
    #         print(f"Student {student_id} not found")
    #         return
    #
    #     show_student(student)
    #     print(
    #         f"\n\nTo update user's data, specify `name` and `info`, with `;` separator.\n"
    #     )
    #
    #     user_input: str = input("Enter: ")
    #     updated_student: dict | None = update_student(id_=id_, raw_input=user_input)
    #
    #     if updated_student is None:
    #         print("Erorr on updating student")
    #     else:
    #         print(f"Student {updated_student['name']} is updated")


# ─────────────────────────────────────────────────────────
# PRESENTATION LAYER
# ─────────────────────────────────────────────────────────
def handle_user_input():
    OPERATIONAL_COMMANDS = ("quit", "help")
    STUDENT_MANAGEMENT_COMMANDS = ("show", "add", "search", "delete", "update", "add marks", "show student")
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

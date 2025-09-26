import enum

class Role(enum.StrEnum):
    STUDENT = enum.auto()
    TEACHER = enum.auto()

class User:
    def __init__(self, name: str, email: str, role: Role) -> None:
        self.name = name
        self.email = email
        self.role = role

    def send_notification(self, notification) -> None:
        # TODO: print out or log the notification
        print(notification)

class Notification:
    def __init__(self, subject: str, message: str, attachment: str = "") -> None:
        self.subject = subject
        self.message = message
        self.attachment = attachment  # Optional extra info

    def format(self) -> str:
        # TODO: implement basic notification formatting
        # TODO: think about `__str__` usage instead of `format`
        formatted_message = f"Notification!!!\nSubject: {self.subject}\nMessage: {self.message}"
        if self.attachment:
            formatted_message += f"\nAttachment: {self.attachment}\n"
        return formatted_message

    def __str__(self) -> str:
        return self.format()

class StudentNotification(Notification):
    def format(self) -> str:
        # TODO: add "Sent via Student Portal" to the message
        formatted_message = f"Notification!!!\nSubject: {self.subject}\nMessage (Sent via Student Portal): {self.message}"
        if self.attachment:
            formatted_message += f"\nAttachment: {self.attachment}\n"
        return formatted_message

class TeacherNotification(Notification):
    def format(self) -> str:
        # TODO: add "Teacher's Desk Notification" to the message
        formatted_message = f"Notification!!!\nSubject: {self.subject}\nMessage (Teacher's Desk Notification): {self.message}"
        if self.attachment:
            formatted_message += f"\nAttachment: {self.attachment}\n"
        return formatted_message

def main():
    # TODO: create users of both types
    # TODO: create notifications
    # TODO: have users print (aka send) their notifications
    student1 = User('John', 'student.john@gmail.com', Role.STUDENT)
    teacher1 = User('Ulia', 'teacher.ulia@gmail.com', Role.TEACHER)

    student1.send_notification(StudentNotification('Math', 'I have a problem', 'screenshot.jpg'))
    teacher1.send_notification(TeacherNotification('Python', 'Solve the problem'))

if __name__ == "__main__":
    main()
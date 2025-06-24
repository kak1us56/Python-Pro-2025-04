"""
- acvtive record pattern
    - store methods to work with entities as close as possible
"""

import enum
import smtplib
from email.mime.text import MIMEText


# ─────────────────────────────────────────────────────────
# MAILING
# ─────────────────────────────────────────────────────────
class Message:
    def __init__(self, from_addr: str, subject: str, message: str) -> None:
        self.msg = MIMEText(message)
        self.msg["From"] = from_addr
        self.msg["Subject"] = subject

    def __str__(self) -> str:
        return str(self.msg)

    @property
    def representation(self) -> str:
        return self.msg.as_string()

    @property
    def sender(self) -> str:
        return self.msg["From"]

    @property
    def subject(self) -> str:
        return self.msg["Subject"]


class HRMessage(Message):
    def __init__(self, from_addr: str, subject: str, message: str) -> None:
        super().__init__(
            from_addr="hr@apple.com",
            subject=subject,
            message="".join((message, "\n\nHR Department")),
        )


class SupportMessage(Message):
    def __init__(self, from_addr: str, subject: str, message: str) -> None:
        super().__init__(
            from_addr="support@apple.com",
            subject=subject,
            message="".join((message, "\n\nSupport Department")),
        )


class AdminMessage(Message):
    def __init__(self, from_addr: str, subject: str, message: str) -> None:
        super().__init__(
            from_addr="admin@apple.com",
            subject=subject,
            message="".join((message, "\n\nApple Admin")),
        )


class SMTPService:
    def __init__(self, host: str = "localhost", port: int = 1025) -> None:
        self.host = host
        self.port = port

    def __enter__(self):
        """Open the connection."""

        self.server = smtplib.SMTP(host=self.host, port=self.port)
        print("Open SMTP Server Connection")
        return self

    def __exit__(self, *args, **kwargs):
        """Close the connection."""

        self.server.quit()
        print("Close SMTP Server Connection")

    def send(self, from_: str, to: str, message: Message) -> None:
        self.server.sendmail(msg=str(message), from_addr=from_, to_addrs=to)


# ─────────────────────────────────────────────────────────
# USERS
# ─────────────────────────────────────────────────────────
class Role(enum.StrEnum):
    ADMIN = enum.auto()
    HR = enum.auto()
    SUPPORT = enum.auto()
    CUSTOMER = enum.auto()


class User:
    def __init__(self, email: str, role: Role) -> None:
        self.email = email
        self.role = role


# ─────────────────────────────────────────────────────────
# ENTRYPOINT
# ─────────────────────────────────────────────────────────
def main():
    # I/O Operations
    # ........................................
    to = "john@email.com"

    # Logic
    # ........................................
    user = User(email="internal_user@apple.com", role=Role.HR)
    message = SupportMessage(
        from_addr=user.email,
        subject="iPhone black screen",
        message="Hey John, Could you take some pictures of your screen?",
    )
    message_2 = HRMessage(
        from_addr=user.email,
        subject="iPhone black screen",
        message="Hey John, Could you take some pictures of your screen?",
    )

    with SMTPService() as mailing:
        mailing.send(from_=user.email, to=to, message=message)
        mailing.send(from_=user.email, to=to, message=message_2)


main()

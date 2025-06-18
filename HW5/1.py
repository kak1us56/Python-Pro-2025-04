import inspect
from typing import Any

from jupyter_server.auth import authorized


class User:
    def __init__(self, login: str, password: str, balance: int):
        self.login: str = login
        self.password: str = password
        self.balance: int = balance

class Database:
    users = {
        1: User(login="john", password="john123", balance=0),
        2: User(login="marry", password="yrram123", balance=0),
        3: User(login="alice", password="ecila123", balance=0),
        4: User(login="bob", password="bob321", balance=0),
        5: User(login="charlie", password="eilrahc123", balance=0),
        6: User(login="diana", password="anaid123", balance=0),
        7: User(login="eric", password="cire123", balance=0),
        8: User(login="frank", password="knarf123", balance=0),
        9: User(login="grace", password="ecarg123", balance=0),
        10: User(login="hannah", password="hannah321", balance=0),
    }

class Price:
    def __init__(self, amount: int, currency: str):
        self.amount: int = amount
        self.currency: str = currency

    def __add__(self, other: Any):
        if not isinstance(other, Price):
            raise ValueError('Can perform operations only with "Price" objects')
        else:
            if self.currency != other.currency:
                raise ValueError('Currencies must match')
            else:
                return Price(self.amount + other.amount, self.currency)
    def __sub__(self, other: Any):
        if not isinstance(other, Price):
            raise ValueError('Can perform operations only with "Price" objects')
        else:
            if self.currency != other.currency:
                raise ValueError('Currencies must match')
            else:
                return Price(self.amount - other.amount, self.currency)

phone = Price(500, "usd")
tablet = Price(800, "usd")

total: Price = phone + tablet
sub: Price = tablet - phone
print(f"{total.amount} {total.currency}")
print(f"{sub.amount} {sub.currency}")

class PaymentSystem:
    user: User = None

    def __init__(self):
        self.connected_to_the_atm = False


    def auth(self) -> None:
        authorizing = True
        ask_prompt: str = "Enter login and password to execute the command\n"

        while authorizing:
            print(ask_prompt)
            login: str = input("Login: ")
            password: str = input("Password: ")

            for x in range(1, 11):
                if Database.users[x].login == login and Database.users[x].password == password:
                    self.user = Database.users[x]
                    print("Login successful\n")

                    authorizing = False
                    break
            else:
                print("Login failed\n")

    def auth_required(func):
        def wrapper(self, *args, **kwargs):
            if self.user is None:
                self.auth()
            return func(self, *args, **kwargs)
        return wrapper

    @auth_required
    def deposit(self):
        amount: int = int(input("Amount: "))
        self.user.balance += amount
        print(f"Deposit {amount} to {self.user.balance}")
        print(f"TOTAL: {self.user.balance}")

    @auth_required
    def withdraw(self):
        amount: int = int(input("Amount: "))
        self._validate_money()
        self._connect_to_the_atm()
        self._count_the_cash(amount)
        self._get_money(amount)

    def _validate_money(self):
        if self.user.balance < 0:
            print("Cannot deposit money")

    def _connect_to_the_atm(self):
        self.connected_to_the_atm = True
        print("Connected to ATM")

    def _count_the_cash(self, amount: int):
        if self.connected_to_the_atm is True:
            print(f"Counting {amount} in the ATM")
        else:
            print("Something went wrong")

    def _get_money(self, amount: int):
        if self.connected_to_the_atm is True:
            self.user.balance -= amount
            print(f"Returning money from ATM")
        else:
            print("Something went wrong")

    @auth_required
    def balance(self):
        print(self.user_repr)

    @property
    def user_repr(self):
        # self.msg = ...
        return f"User {self.user.login}, balance: {self.user.balance}\n"

    @user_repr.setter
    def user_repr(self, value):
        if "admin:" in value:
            return value.replace("admin:", "")
        else:
            raise ValueError("Can not set value")


    # def __getattr__(self, item: str):
    #     print(f"Attribute: {item} not found")

    # NOTE: bad idea...
    # def __getattribute__(self, name: str):
    #     breakpoint()  # TODO: remove
    #     if name.startswith("_"):
    #         stack = inspect.stack()
    #         print("Stack at attribute")
    #
    #         for i, frame in enumerate(stack[0:4]):
    #             print(f"Frame {i}: {frame.function}, {frame.filename}")
    #
    #         if not any(
    #             (frame.frame.f_locals.get("self", None) is self for frame in stack[1:3])
    #         ):
    #             raise AttributeError(f"Access to attribute {name} restricted")
    #
    #     return super().__getattribute__(name)


def main():
    ps = PaymentSystem()

    while True:
        commands: tuple = ("deposit", "withdraw", "balance")

        print(f"Available commands: {', '.join(commands)}")

        command: str = input("Enter command: ")

        match command:
            case "deposit":
                ps.deposit()
            case "withdraw":
                ps.withdraw()
            case "balance":
                ps.balance()
            case _:
                print(f"Unknown command: {command}")

    # user = Database.users[1]
    # payment_system = PaymentSystem(user=user)

    # payment_system.deposit(100)
    # payment_system.withdraw(10)
    # payment_system.balance()

    # payment_system.user_repr = "admin:hacked"
    # payment_system.balance()

    # payment_system._get_money(20)
    # payment_system.balance()

if __name__ == "__main__":
    main()

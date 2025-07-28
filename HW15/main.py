import psycopg
from dataclasses import dataclass
from pprint import pprint as print
from datetime import date
from typing import Literal

connection_payload = {
    "dbname": "hw15",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432"
}

class DatabaseConnection:
    def __enter__(self):
        self.conn = psycopg.connect(**connection_payload)
        self.cur = self.conn.cursor()

        return self

    def __exit__(self, exc_type, *_):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()

        self.cur.close()
        self.conn.close()

    def query(self, sql: str, params: tuple | None = None):
        self.cur.execute(sql, params)
        return self.cur.fetchall()

@dataclass
class User:
    name: str
    phone: str
    role: Literal["ADMIN", "USER", "SUPPORT"]
    id: int | None = None

    @classmethod
    def all(cls) -> list["User"]:
        with DatabaseConnection() as db:
            rows = db.query("SELECT name, phone, role, id FROM users")
            return [cls(*row) for row in rows]

    @classmethod
    def get(cls, param: Literal["id", "name", "phone", "role"], value: str | int) -> list["User"]:
        with DatabaseConnection() as db:
            match param:
                case "id":
                    rows = db.query("SELECT name, phone, role, id FROM users WHERE id = %s", (value,))
                case "name":
                    rows = db.query("SELECT name, phone, role, id FROM users WHERE name = %s", (value,))
                case "phone":
                    rows = db.query("SELECT name, phone, role, id FROM users WHERE phone = %s", (value,))
                case "role":
                    rows = db.query("SELECT name, phone, role, id FROM users WHERE role = %s", (value,))

            return [cls(*row) for row in rows]

    @classmethod
    def delete(cls, param: Literal["id", "name", "phone", "role"], value: str | int):
        with DatabaseConnection() as db:
            match param:
                case "id":
                    db.query("DELETE FROM users WHERE id = %s RETURNING id", (value,))
                case "name":
                    db.query("DELETE FROM users WHERE name = %s RETURNING name", (value,))
                case "phone":
                    db.query("DELETE FROM users WHERE phone = %s RETURNING phone", (value,))
                case "role":
                    db.query("DELETE FROM users WHERE role = %s RETURNING role", (value,))

            print(f"user with {param}={value} is deleted")

    def create(self) -> "User":
        with DatabaseConnection() as db:
            db.cur.execute("INSERT INTO users (name, phone, role) VALUES (%s, %s, %s) RETURNING id", (self.name, self.phone, self.role),)

            self.id = db.cur.fetchone()[0]
            return self

    def update(self, **payload) -> "User | None":
        fields = ", ".join([f"{key} = %s" for key in payload])
        values = tuple(payload.values())

        if self.id is None:
            raise ValueError("Can`t update user without ID")

        with DatabaseConnection() as db:
            db.cur.execute(
                f"UPDATE users SET {fields} WHERE id = %s RETURNING id, name, phone, role",
                (*values, self.id),
            )

            row = db.cur.fetchone()

        if not row:
            return None
        else:
            _, name, phone, role = row
            self.name = name
            self.phone = phone
            self.role = role

            return self

@dataclass
class Dish:
    name: str
    price: float
    id: int | None = None

    @classmethod
    def all(cls) -> list["Dish"]:
        with DatabaseConnection() as db:
            rows = db.query("SELECT name, price, id FROM dishes")
            return [cls(*row) for row in rows]

    @classmethod
    def get(cls, param: Literal["id", "name", "price"], value: str | int) -> list["Dish"]:
        with DatabaseConnection() as db:
            match param:
                case "id":
                    rows = db.query("SELECT name, price, id FROM dishes WHERE id = %s", (value,))
                case "name":
                    rows = db.query("SELECT name, price, id FROM dishes WHERE name = %s", (value,))
                case "price":
                    rows = db.query("SELECT name, price, id FROM dishes WHERE price = %s", (value,))

            return [cls(*row) for row in rows]

    @classmethod
    def delete(cls, param: Literal["id", "name", "price"], value: str | int):
        with DatabaseConnection() as db:
            match param:
                case "id":
                    db.query("DELETE FROM dishes WHERE id = %s RETURNING id", (value,))
                case "name":
                    db.query("DELETE FROM dishes WHERE name = %s RETURNING name", (value,))
                case "price":
                    db.query("DELETE FROM dishes WHERE price = %s RETURNING price", (value,))

            print(f"dish with {param}={value} is deleted")

    def create(self) -> "Dish":
        with DatabaseConnection() as db:
            db.cur.execute("INSERT INTO dishes (name, price) VALUES (%s, %s) RETURNING id", (self.name, self.price))

            self.id = db.cur.fetchone()[0]
            return self

    def update(self, **payload) -> "Dish | None":
        fields = ", ".join([f"{key} = %s" for key in payload])
        values = tuple(payload.values())

        if self.id is None:
            raise ValueError("Can`t update user without ID")

        with DatabaseConnection() as db:
            db.cur.execute(
                f"UPDATE dishes SET {fields} WHERE id = %s RETURNING id, name, price",
                (*values, self.id),
            )

            row = db.cur.fetchone()

        if not row:
            return None
        else:
            _, name, price = row
            self.name = name
            self.price = price

            return self

@dataclass
class Order:
    date: date
    total: float
    status: Literal["PENDING", "DELIVERED", "PROCESSING"]
    user_id: int
    id: int | None = None

    @classmethod
    def all(cls) -> list["Order"]:
        with DatabaseConnection() as db:
            rows = db.query("SELECT date, total, status, user_id, id FROM orders")
            return [cls(*row) for row in rows]

    @classmethod
    def get(cls, param: Literal["id", "date", "total", "status", "user_id"], value: str | int) -> list["Order"]:
        with DatabaseConnection() as db:
            match param:
                case "id":
                    rows = db.query("SELECT date, total, status, user_id, id FROM orders WHERE id = %s", (value,))
                case "date":
                    rows = db.query("SELECT date, total, status, user_id, id FROM orders WHERE date = %s", (value,))
                case "status":
                    rows = db.query("SELECT date, total, status, user_id, id FROM orders WHERE status = %s", (value,))
                case "total":
                    rows = db.query("SELECT date, total, status, user_id, id FROM orders WHERE total = %s", (value,))
                case "user_id":
                    rows = db.query("SELECT date, total, status, user_id, id FROM orders WHERE user_id = %s", (value,))

            return [cls(*row) for row in rows]

    @classmethod
    def delete(cls, param: Literal["id", "date", "total", "status", "user_id"], value: str | int):
        with DatabaseConnection() as db:
            match param:
                case "id":
                    db.query("DELETE FROM orders WHERE id = %s RETURNING id", (value,))
                case "date":
                    db.query("DELETE FROM orders WHERE date = %s RETURNING date", (value,))
                case "total":
                    db.query("DELETE FROM orders WHERE total = %s RETURNING total", (value,))
                case "status":
                    db.query("DELETE FROM orders WHERE status = %s RETURNING status", (value,))
                case "user_id":
                    db.query("DELETE FROM orders WHERE user_id = %s RETURNING user_id", (value,))

            print(f"order with {param}={value} is deleted")

    def create(self) -> "Order":
        with DatabaseConnection() as db:
            db.cur.execute("INSERT INTO orders (date, total, status, user_id) VALUES (%s, %s, %s, %s) RETURNING id", (self.date, self.total, self.status, self.user_id))

            self.id = db.cur.fetchone()[0]
            return self

    def update(self, **payload) -> "Order | None":
        fields = ", ".join([f"{key} = %s" for key in payload])
        values = tuple(payload.values())

        if self.id is None:
            raise ValueError("Can`t update user without ID")

        with DatabaseConnection() as db:
            db.cur.execute(
                f"UPDATE orders SET {fields} WHERE id = %s RETURNING id, date, total, status, user_id",
                (*values, self.id),
            )

            row = db.cur.fetchone()

        if not row:
            return None
        else:
            _, date, total, status, user_id = row
            self.date = date
            self.total = total
            self.status = status
            self.user_id = user_id

            return self

@dataclass
class OrderItem:
    order_id: int
    dish_id: int
    quantity: int
    id: int | None = None

    @classmethod
    def all(cls) -> list["OrderItem"]:
        with DatabaseConnection() as db:
            rows = db.query("SELECT order_id, dish_id, quantity, id FROM order_items")
            return [cls(*row) for row in rows]

    @classmethod
    def get(cls, param: Literal["id", "order_id", "dish_id", "quantity"], value: str | int) -> list["OrderItem"]:
        with DatabaseConnection() as db:
            match param:
                case "id":
                    rows = db.query("SELECT order_id, dish_id, quantity, id FROM order_items WHERE id = %s", (value,))
                case "order_id":
                    rows = db.query("SELECT order_id, dish_id, quantity, id FROM order_items WHERE order_id = %s", (value,))
                case "dish_id":
                    rows = db.query("SELECT order_id, dish_id, quantity, id FROM order_items WHERE dish_id = %s", (value,))
                case "quantity":
                    rows = db.query("SELECT order_id, dish_id, quantity, id FROM order_items WHERE quantity = %s", (value,))

            return [cls(*row) for row in rows]

    @classmethod
    def delete(cls, param: Literal["id", "order_id", "dish_id", "quantity"], value: str | int):
        with DatabaseConnection() as db:
            match param:
                case "id":
                    db.query("DELETE FROM order_items WHERE id = %s RETURNING id", (value,))
                case "order_id":
                    db.query("DELETE FROM order_items WHERE order_id = %s RETURNING order_id", (value,))
                case "dish_id":
                    db.query("DELETE FROM order_items WHERE dish_id = %s RETURNING dish_id", (value,))
                case "quantity":
                    db.query("DELETE FROM order_items WHERE quantity = %s RETURNING quantity", (value,))

            print(f"order_item with {param}={value} is deleted")

    def create(self) -> "OrderItem":
        with DatabaseConnection() as db:
            db.cur.execute("INSERT INTO order_items (order_id, dish_id, quantity) VALUES (%s, %s, %s) RETURNING id", (self.order_id, self.dish_id, self.quantity),)

            self.id = db.cur.fetchone()[0]
            return self

    def update(self, **payload) -> "OrderItem | None":
        fields = ", ".join([f"{key} = %s" for key in payload])
        values = tuple(payload.values())

        if self.id is None:
            raise ValueError("Can`t update user without ID")

        with DatabaseConnection() as db:
            db.cur.execute(
                f"UPDATE order_items SET {fields} WHERE id = %s RETURNING id, order_id, dish_id, quantity",
                (*values, self.id),
            )

            row = db.cur.fetchone()

        if not row:
            return None
        else:
            _, order_id, dish_id, quantity = row
            self.order_id = order_id
            self.dish_id = dish_id
            self.quantity = quantity

            return self


# user = User("mark", '+3809482642234', "USER").create()
# user.update(name="max")

print(User.all())
print(User.get("id", 1))

print(Order.all())
# order = Order('30-09-2024', 15, 'DELIVERED', 8).create()
# order.update(total=1500)

print(Dish.all())
print(OrderItem.all())
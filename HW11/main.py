from datetime import datetime, timedelta
import queue
import threading
import time
import random
from typing import Literal

OrderRequestBody = tuple[str, datetime]
ReadyOrderRequestBody = tuple[str, datetime, Literal["Uklon", "Uber"]]

PROVIDERS: list = ["Uklon", "Uber"]

storage = {
    "users": [],
    "dishes": [
        {
            "id": 1,
            "name": "Salad",
            "value": 1099,
            "restaurant": "Silpo",
        },
        {
            "id": 2,
            "name": "Soda",
            "value": 199,
            "restaurant": "Silpo",
        },
        {
            "id": 3,
            "name": "Pizza",
            "value": 599,
            "restaurant": "Kvadrat",
        },
    ],
    # ...
}


class Scheduler:
    def __init__(self):
        self.orders: queue.Queue[OrderRequestBody] = queue.Queue()
        self.ready_orders: queue.Queue[ReadyOrderRequestBody] = queue.Queue()

    def process_orders(self) -> None:
        print("SCHEDULER PROCESSING...")

        while True:
            order = self.orders.get(True)

            time_to_wait = order[1] - datetime.now()

            if time_to_wait.total_seconds() > 0:
                self.orders.put(order)
                time.sleep(0.5)
            else:
                amount_uklon = 0
                amount_uber = 0

                for order in self.ready_orders.queue:
                    if order[2] == "Uklon":
                        amount_uklon += 1
                    else:
                        amount_uber += 1

                if self.ready_orders.qsize() == 0 or amount_uklon == amount_uber:
                    selected_provider: Literal["Uklon", "Uber"] = random.choice(PROVIDERS)
                    self.ready_orders.put((order[0], order[1], selected_provider))
                elif amount_uber > amount_uklon:
                    self.ready_orders.put((order[0], order[1], "Uklon"))
                else:
                    self.ready_orders.put((order[0], order[1], "Uber"))

                print(f"\n\t{order[0]} SENT TO SHIPPING DEPARTMENT")

    def process_delivery(self) -> None:
        while True:
            order = self.ready_orders.get(True)

            if order[2] == "Uklon":
                time.sleep(5)
                print(f"{order[0]} is delivered by Uklon")
            else:
                time.sleep(3)
                print(f"{order[0]} is delivered by Uber")


    def add_order(self, order: OrderRequestBody) -> None:
        self.orders.put(order)
        print(f"\n\t{order[0]} ADDED FOR PROCESSING")


def main():
    scheduler = Scheduler()
    thread = threading.Thread(target=scheduler.process_orders, daemon=True)
    thread.start()
    delivery_thread = threading.Thread(target=scheduler.process_delivery, daemon=True)
    delivery_thread.start()

    # user input:
    # A 5 (in 5 days)
    # B 3 (in 3 days)
    while True:
        order_details = input("Enter order details: ")
        data = order_details.split(" ")
        order_name = data[0]
        delay = datetime.now() + timedelta(seconds=int(data[1]))
        scheduler.add_order(order=(order_name, delay))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        raise SystemExit(0)
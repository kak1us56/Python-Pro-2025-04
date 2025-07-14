Use this python code as an example:

```python
from datetime import datetime, timedelta
import queue
import threading
import time

OrderRequestBody = tuple[str, datetime]


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

    def process_orders(self) -> None:
        print("SCHEDULER PROCESSING...")

        while True:
            order = self.orders.get(True)

            time_to_wait = order[1] - datetime.now()

            if time_to_wait.total_seconds() > 0:
                self.orders.put(order)
                time.sleep(0.5)
            else:
                print(f"\n\t{order[0]} SENT TO SHIPPING DEPARTMENT")

    def add_order(self, order: OrderRequestBody) -> None:
        self.orders.put(order)
        print(f"\n\t{order[0]} ADDED FOR PROCESSING")


def main():
    scheduler = Scheduler()
    thread = threading.Thread(target=scheduler.process_orders, daemon=True)
    thread.start()

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
```

Extend it according to the next requirements:

- after order is ready (time_to_wait.total_seconds() <= 0), instead of just printing out details - add another task to another queue for DELIVERY PROCESS
- another Thread (daemon) that is processing tasks must be setup for this application
  - so the another handler takes care about ORDERS DELIVERY TASKS without affecting user interaction with the application or orders scheduling
- how to logic of delivery should be implemented?
  - first of all you have to extend your code with available providers: "uklon" and "uber"
  - after the order is ready - select RANDOM provider from the available list
  - if the delivery provider is uklon - wait for 5 seconds (use `time.sleep()`) and print that order is delivered
  - if the delivery provider is uber - wait for 3 seconds (use `time.sleep()`) and print that order is delivered

Optional improvements:

- if you wanna optimize your application you would need to track how many orders are currently in processing for each provider. Based on that, instead of selecting a random provider you can take the one, that has LESS orders in processing to secure the balance.

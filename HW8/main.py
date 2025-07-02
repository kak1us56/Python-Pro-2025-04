"""

INPUT: medium.com/feed, news.google.com?today=true

SOLUTION:

    Thread 1 (main): user input urls
        > medium.com/feed
        > news.google.com?today

    Thread 2 (daemon):
        - crawler()
"""

import asyncio
import functools
import random
from pprint import pprint as print
from threading import Thread
from typing import Literal

Status = Literal["done", "pending"]

results: dict[str, Status] = {}
tasks: set[asyncio.Task] = set()
refresh_time: int = 1


async def crawler():
    global tasks

    while True:
        if not tasks:
            await asyncio.sleep(1)
        else:
            done, pending = await asyncio.wait(tasks, timeout=refresh_time)
            tasks -= done
            # print(f"Complete with {len(done)} tasks. Pending: {len(pending)}")


async def parse_url(url: str):
    results[url] = "pending"
    await asyncio.sleep(random.randint(5, 10))
    results[url] = "done"


def parse_url_task(loop, coro):
    task = loop.create_task(coro)
    tasks.add(task)


def ask_for_urls(loop: asyncio.AbstractEventLoop):
    while True:
        command = input("Enter URL address: ")
        if command == "results":
            print(results)
        elif command == "tasks":
            print(tasks)
        # ADD FLOW
        else:
            url = command

            callback = functools.partial(parse_url_task, loop, parse_url(url))
            loop.call_soon_threadsafe(callback)

            print(f"Created another task. The len of tasks {len(tasks)}.")


def main():
    loop = asyncio.new_event_loop()

    thread = Thread(target=loop.run_until_complete, args=(crawler(),), daemon=True)
    thread.start()

    ask_for_urls(loop)


main()

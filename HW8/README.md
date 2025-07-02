# asyncio examples

## basic cancel task
```python
import asyncio


async def bar():
    try:
        print("bar started")
        await asyncio.sleep(4)
        print("bar completed")
    except asyncio.CancelledError as error:
        print(f"Error: {error}")


async def foo():
    files = []

    try:
        print("foo started")
        await asyncio.sleep(5)
        print("foo completed")
    except asyncio.CancelledError as error:
        print(f"Error: {error}")



async def main():
    loop = asyncio.get_running_loop()
    task: asyncio.Task = loop.create_task(foo())

    # task.cancel()
    loop.call_later(delay=2, callback=task.cancel)
    await task

asyncio.run(main())
```


## wait_for asyncio

```python
import asyncio


async def foo():
    try:
        print("foo started")
        await asyncio.sleep(5)
        print("foo completed")
    except asyncio.CancelledError as error:
        print(f"Error: {error}")


async def main():
    await asyncio.wait_for(foo(), timeout=2)


asyncio.run(main())
```



## asyncio.wait()

```python
import asyncio


async def callback(name: str, blocking_time: float = 10.0):
    try:
        print(f"{name} started. blocking time: {blocking_time}")
        await asyncio.sleep(blocking_time)
        # print(f"{name} completed")
    except asyncio.CancelledError:
        print(f"Cancelled: {name}")


async def main():
    loop = asyncio.get_running_loop()
    tasks = {
        loop.create_task(callback(name="foo", blocking_time=5)),
        loop.create_task(callback(name="bar", blocking_time=2)),
        loop.create_task(callback(name="baz", blocking_time=0.5)),
        loop.create_task(callback(name="baz2", blocking_time=0.5)),
    }

    print("created tasks")

    refresh_time = 0.3

    while tasks:
        done, pending = await asyncio.wait(tasks, timeout=refresh_time)
        if done:
            tasks -= done
            print(f"Completed {len(done)} tasks")

        if pending:
            print(f"Waiting for {len(pending)} tasks")


asyncio.run(main())
```

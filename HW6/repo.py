import time
import logging

# TimerContext
class TimerContext:
    def __enter__(self):
        self.start = time.time()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start
        logging.info(f'Elapsed time: {elapsed:.2f} seconds')

logging.basicConfig(level=logging.INFO)

with TimerContext():
    time.sleep(2)

with TimerContext():
    for _ in range(10000000):
        pass

with TimerContext():
    sum(i**i for i in range(5000))


# Configuration Context Manager
GLOBAL_CONFIG = {"feature_a": True, "max_retries": 3}

class Configuration:
    def __init__(self, updates, validator = None):
        self.updates = updates
        self.validator = validator
        self.original = GLOBAL_CONFIG.copy()

    def __enter__(self):
        updated_config = GLOBAL_CONFIG.copy()
        updated_config.update(self.updates)

        if self.validator and not self.validator(updated_config):
            raise ValueError("Invalid configuration")

        GLOBAL_CONFIG.update(self.updates)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        GLOBAL_CONFIG.clear()
        GLOBAL_CONFIG.update(self.original)

def validate_config(config):
    return config.get("max_retries", 0) >= 0

# Valid Config
with Configuration({"feature_a": False, "max_retries": 5}, validator=validate_config):
    print(GLOBAL_CONFIG)

# Invalid Config
try:
    with Configuration({"feature_a": False, "max_retries": -1}, validator=validate_config):
        print(GLOBAL_CONFIG)
except ValueError as e:
    print(e)


# class Repository:
#     def __init__(self, filename: str):
#         self.filename = filename
#         self.file:IOTextWSr
#
#
#     def __enter__(self):
#         file = open(self.filename, "r")
#         setattr(self, "_file", file)
#         self.data = file.read()
#
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         if self._file is None:
#             return
#         else:
#             self._file.write(self.data)
#             self._file.close()
#         # if (file := getattr(self, "_file", None)) is not None:
#         #     print("Closing the file ")
#         #     file.close()
#         #     return
#         # else:
#         #     return
#
#     def add_student(self):





# with Repository("storage.json") as repo:
#     students = repo.get_students()
#     repo.add_student()
#     repo.get_student()


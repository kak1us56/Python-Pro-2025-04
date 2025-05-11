"""
1. JSON
{
    "name": "John",
    "surname": "Doe",
},
{
    "name": "Marry",
    "surname": "Black",
}

json.load() - read from a file and converts json into python object
json.dump() - writes ...
json.loads() -
json.dumps()


2. CSV
name,surname
john,doe
marry,black

3. XML
...

4. PICKLE
...
"""
from pathlib  import Path

students = {}

PROJECT_ROOT = Path(__file__).parent.parent
print(str(PROJECT_ROOT))
file = open(PROJECT_ROOT / 'students.txt')
# content: str = file.read(3)
# content = file.readlines()
content = file.read()
print(content)

# 0123456................
# John Doe|nMarry Black\n
# pointer = file.tell()
# print(pointer)
#
# file.seek(0)
# content = file.read()
# print(content)

file.close()

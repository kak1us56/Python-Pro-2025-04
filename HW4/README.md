## OS perspective

- files are managed by OS
- FS tree (logical structure)
- permissions
  - for security purposes
  - range 000 - 777
  - some files require specific permissions
    - like SSH keys, etc
- can multiple processes read a single file?
  - yes
  - `FILE_SHARE_READ` flag on Windows
- can multiple processes write to a single file?
  - yes
  - currently operatyng systems handle this process pretty much gracefully so we won't get into this very deeply
  - using locks
    - `fcntl.flock` for Unix locks
    - `FILE_SHARE_WRITE` flag on Windows

## Python API. File Descriptor

- file object in python glossary
- `io` module classes hierarchy
- only a single function: `open()`
  - path name. `absolute`, `relative`
  - mode: `r w a`
  - type: text bytes
  - possible permissions issue on OS
    - `chmod` on Unix
    - on Windows just don't create files in `System32` folder
      - use `Desktop` or project folder instead
- `file` object

  - common methods:
  - `file.read()` read all the file
  - `file.read(n)` read `n` chars
  - `file.readlines()` => read all the file
  - `file.tell()` return pointer number
  - `file.seek(n)` move file pointer to `n` index position
  - `file.close()` close the file

- _built-in_ library for common data formats: `json`, `csv`, `xml`, `pickle`

## `json` module

- `json.load()` – reads from a file and converts json into python objects.
- `json.dump()` – writes python objects as json to a file.
- `json.loads()` and json.dumps() – work with json strings (not directly with files).

```python
import json

with open("data.json", "r") as f:
    data = json.load(f)

with open("output.json", "w") as f:
    json.dump(data, f)
```

## `yaml` module

```python
import yaml

with open("config.yaml", "r") as f:
    data = yaml.safe_load(f)

with open("output.yaml", "w") as f:
    yaml.dump(data, f)
```

## `csv` module

- `csv.reader()` – reads rows from a csv file as lists.
- `csv.writer()` – writes rows to a csv file.
- `csv.DictReader()` and csv.DictWriter() – works with csv files as dictionaries.

```python
import csv
with open("data.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Age"])
    writer.writerow(["Alice", "30"])
```

## `configparser` module

- `configparser.ConfigParser()`

```python
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

# Read values
db_host = config["database"]["host"]

# Write values
config["database"]["host"] = "localhost"
with open("config.ini", "w") as configfile:
    config.write(configfile)
```

## `xml` module

- `ElementTree.parse()` – reads and parses an XML file.
- `ElementTree.write()` – writes an XML file.

```python
import xml.etree.ElementTree as ET

tree = ET.parse("data.xml")
root = tree.getroot()

for child in root:
    print(child.tag, child.attrib)

tree.write("output.xml")
```

## `pickle` module

- `pickle.dump()` – saves a Python object to a file.
- `pickle.load()` – loads a Python object from a file.

```python
import pickle

data = {"name": "Alice", "age": 30}

# Save to a file
with open("data.pkl", "wb") as f:
    pickle.dump(data, f)

# Load from a file
with open("data.pkl", "rb") as f:
    loaded_data = pickle.load(f)
```

## `zipfile` module

```python
import zipfile

# Create a zip file
with zipfile.ZipFile("output.zip", "w") as z:
    z.write("file.txt")

# Extract a zip file
with zipfile.ZipFile("output.zip", "r") as z:
    z.extractall("extracted_files")
```

## tarfile (skip this one)

```python
import tarfile

# Create a tar.gz file
with tarfile.open("output.tar.gz", "w:gz") as tar:
    tar.add("file.txt")

# Extract a tar.gz file
with tarfile.open("output.tar.gz", "r:gz") as tar:
    tar.extractall("extracted_files")
```


## `pathlib` module

- `pathlib` module implements common operations with file system

```python
from pathlib import Path

# Cross-platform way to handle paths
file_path = Path("data") / "input.txt"
```

## not existing file error

```python
try:
    with open("nonexistent.txt", "r") as f:
        data = f.read()
except FileNotFoundError:
    print("File not found. Please check the file path.")
```

## file locking mechanism (skip)

```python
import fcntl

with open("file.txt", "w") as f:
    fcntl.flock(f, fcntl.LOCK_EX)
    f.write("Locked writing")
    fcntl.flock(f, fcntl.LOCK_UN)
```

## Binary Files

```python
# Reading binary file
with open("image.jpg", "rb") as img:
data = img.read()
```

## Changing File Permissions

```python
import os

# Change file permissions to read-only
os.chmod("file.txt", 0o444)
```

## Temporary Files

```python
import tempfile

with tempfile.NamedTemporaryFile(delete=False) as temp:
    temp.write(b"Temporary data")
```

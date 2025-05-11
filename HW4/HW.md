
- Persistent storage (as FILE) is added (or plugged) to the project
- All USER OPERATIONS now work with persistent storage instead of in-memory object
- Data must be stored in `.csv` format
- `class Repository` is responsible for the next operations:
    - reading `.csv` file content into local variable `students` to operate in application on startup
    - writing to the `.csv` file the content of `students` that is currently active in the state of this class
    - the `students` variable could be optimized to `dict` representation for optimization (P.S. might be better solution if you don't wanna refactor your existing solution too much)
    - `.add_student(student: dict)` to add student to the storage
    - `.get_student(id_: int)` to add student to the storage
    - `.update_student(id_: int, data: dict)` to partially update student (meaning that `data.keys()` must be appropriate student fields)
    - `.delete_student(id_: int)` to remove student from the storage
    - `.add_mark(id_: int, mark: int)` quickly add mark to specified user
- Repository object could be injected to each place of usage. P.S. If you prefer different way - please, go ahead


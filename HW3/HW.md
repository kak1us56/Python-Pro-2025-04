- "Add Student" feature is updated
  - USER can set `info` along with `name` and `marks`
  - `info` is OPTIONAL
- "Add Mark" must be implemented.
  - Detailed: You have to create User Interface for that feature in existing CLI application. Turn on your imagination
- "Smart Update" feature is implemented.
  - Instead of updating the whole user all the time (`name` and `info` fields) now the UPDATE FEATURE allows user to update only specified fields (`name` of `info` or both)
  - IF USER entered `info` the SYSTEM performs next validation
    - IF USER entered a string that is completely DIFFERENT FROM what we CURRENTLY have in storage - AUGMENT entered information to the existing value in storage
    - IF USER entered a string that INCLUDES the information, that exists in storage - REPLACE (update) it the storage
  - You have to THINK about the BEST UI/UX implementation

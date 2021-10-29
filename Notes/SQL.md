# SQL notes
- Data types in databases
    - SQLite types
        - TEXT
        - NUMERIC (DATES, ETC)
        - INTEGER
        - REAL  
        - BLOB
    - MySQL
        - CHAR(size)
        - VARCHAR(size)
        - SMALLINT
        - INT
        - BIGINT
        - FLOAT
        - DOUBLE
        - ...
- Example create table in SQLite
```sql 
CREATE TABLE flights {
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origin TEXT NOT NULL, 
    destination TEXT NOT NULL, 
    duration INTEGER NOT NULL
};
```
- Constraints
    - CHECK - (numbers are in a certain range, etc)
    - DEFAULT
    - NOT NULL
    - PRIMARY KEY
    - UNIQUE
- Adding data
    - INSERT command
```sql
INSERT INTO flights (origin, destination, duration) VALUES ("New York", "London", 415);
```
- Get data back out
    - SELECT
```sql
SELECT * from flights; 
```


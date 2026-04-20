CREATE TABLE IF NOT EXISTS employees (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    role       TEXT    NOT NULL,
    position   TEXT    NOT NULL,
    department TEXT    NOT NULL,
    age        INTEGER NOT NULL,
    hire_date  TEXT    NOT NULL,
    status     TEXT    NOT NULL DEFAULT '在籍中'
               CHECK (status IN ('在籍中', '退職済'))
);

DROP TABLE IF EXISTS base;

CREATE TABLE base (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    deep_sleep TEXT NOT NULL,
    light_sleep TEXT NOT NULL,
    sleep_time TEXT NOT NULL,
    sleep_status TEXT NOT NULL /*最後這裡不行有逗號 */
);
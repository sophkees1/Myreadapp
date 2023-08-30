-- CREATE SCHEMA
CREATE SCHEMA IF NOT EXISTS read;

-- set default schema 
SET SEARCH_PATH TO read;

-- create custom type
CREATE TYPE state AS ENUM (
    'pending',
    'reading',
    'complete'
);

-- create table called bookclub
CREATE TABLE bookclub (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    title VARCHAR(300) NOT NULL,
    description TEXT,
    status state NOT NULL DEFAULT 'pending',
    pct_read SMALLINT NOT NULL DEFAULT 0,
    start_read_date DATE,
    end_read_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    -- CONDITIONS
    /*
    if status = 'complete', then we want pct_read = 100
    else pct_read between 0 and 99 and status <> 'complete'
    */
    CHECK(
        pct_read = 100 AND status = 'complete'
        OR
        pct_read BETWEEN 0 AND 99 AND status <> 'complete'
    )
);

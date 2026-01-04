-- 1. Create the Table (The Structure)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,         -- Auto-incrementing ID (1, 2, 3...)
    username VARCHAR(50),          -- Text up to 50 letters
    email VARCHAR(100) UNIQUE,     -- Must be unique (no duplicate emails)
    age INT                        -- A n
);

-- 2. Insert Data (The Content)
INSERT INTO users (username, email, age) 
VALUES 
    ('Kishan', 'kishan@iitbhu.ac.in', 21),
    ('Alice', 'alice@amazon.com', 25),
    ('Bob', 'bob@google.com', 30);

-- 3. View the Data (The Check)
SELECT * FROM users;

DROP TABLE posts;
DROP TABLE users;
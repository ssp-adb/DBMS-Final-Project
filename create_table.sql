CREATE TABLE game_table (
    game_id INT PRIMARY KEY,
    game_name VARCHAR(200),
    publisher VARCHAR(50),
    developer VARCHAR(200),
    platform_id INT,
    rating VARCHAR(10)
);

CREATE TABLE platform_table (
    platform_id INT PRIMARY KEY,
    platform_name VARCHAR(50)
);

CREATE TABLE rating_table (
    rating VARCHAR(10) PRIMARY KEY,
    age INT
);

CREATE TABLE score_table (
    game_id INT PRIMARY KEY,
    critic_score FLOAT,
    critic_count INT,
    user_score FLOAT,
    user_count INT
);

CREATE TABLE sales_table (
    game_id INT PRIMARY KEY,
    na_sales FLOAT,
    eu_sales FLOAT,
    jp_sales FLOAT,
    other_sales FLOAT,
    global_sales FLOAT
);

CREATE TABLE comment_table (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT NOT NULL,
    comment_text TEXT NOT NULL
);

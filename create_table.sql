CREATE TABLE game_table (
    game_id INT PRIMARY KEY,
    game_name VARCHAR(200),
    publisher VARCHAR(50),
    developer VARCHAR(200),
    platform_id INT,
    rating VARCHAR(10),
    year INT,
    genre VARCHAR(50)
);
LOAD DATA LOCAL INFILE './data/game_table.csv' IGNORE INTO TABLE game_table
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES (game_name, publisher, developer, rating, game_id, platform_id, year, genre);


CREATE TABLE platform_table (
    platform_id INT PRIMARY KEY,
    platform VARCHAR(50)
);
LOAD DATA LOCAL INFILE './data/platform_table.csv' IGNORE INTO TABLE platform_table 
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES (platform, platform_id);


CREATE TABLE rating_table (
    rating VARCHAR(10) PRIMARY KEY,
    age INT
);
LOAD DATA LOCAL INFILE './data/rating_table.csv' IGNORE INTO TABLE rating_table
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES (rating, age);


CREATE TABLE score_table (
    game_id INT PRIMARY KEY,
    critic_score INT,
    critic_count INT,
    user_score FLOAT,
    user_count INT
);
LOAD DATA LOCAL INFILE './data/score_table.csv' IGNORE INTO TABLE score_table 
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' 
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES (critic_score, critic_count, user_score, user_count, game_id);


CREATE TABLE sales_table (
    game_id INT PRIMARY KEY,
    na_sales FLOAT,
    eu_sales FLOAT,
    jp_sales FLOAT,
    other_sales FLOAT,
    global_sales FLOAT
);
LOAD DATA LOCAL INFILE './data/sales_table.csv' IGNORE INTO TABLE sales_table
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES (na_sales, eu_sales, jp_sales, other_sales, global_sales, game_id);


CREATE TABLE comment_table (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT NOT NULL,
    comment_text TEXT NOT NULL
);

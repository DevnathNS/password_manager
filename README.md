# password_manager
Password Manager using Python and MySQL

# Installation

## 1. Manual Installation

### MySQL Commands to Set Up the Database and Tables

```
-- Create the database
CREATE DATABASE password_manager;

-- Use the created database
USE password_manager;

-- Create the `users` table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    master_password VARCHAR(64) NOT NULL
);

-- Create the `user_platforms` table
CREATE TABLE user_platforms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    platform VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

## 2. Using Docker
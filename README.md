# password_manager
Password Manager using Python and MySQL

# Installation

## 1. Manual Installation

### MySQL Commands to Set Up the Database and Tables

```sql
CREATE DATABASE password_manager;

USE password_manager;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    master_password VARCHAR(64) NOT NULL
);

CREATE TABLE user_platforms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    platform VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### Configure MySQL User and Privileges

```sql
CREATE USER 'pm_user'@'localhost' IDENTIFIED BY 'secure_password';

GRANT ALL PRIVILEGES ON password_manager.* TO 'pm_user'@'localhost';

FLUSH PRIVILEGES;
```

### Update db_config in Your Python Code
```python
db_config = {
    'host': 'localhost',
    'user': 'pm_user',
    'password': 'secure_password',
    'database': 'password_manager'
}

```

## 2. Using Docker

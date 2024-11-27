import mysql.connector
import hashlib

def create_new_user():
    print("=== New User Registration ===")
    username = input("Enter a unique username: ")

    if is_username_taken(username):
        print("Username already exists. Please choose a different username.")
        return

    master_password = input("Set your master password: ")
    hashed_master_password = hash_password(master_password)

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    insert_user_query = "INSERT INTO users (username, master_password) VALUES (%s, %s)"
    user_data = (username, hashed_master_password)
    cursor.execute(insert_user_query, user_data)

    conn.commit()
    conn.close()

    print("User registration successful!")

def is_username_taken(username):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    check_username_query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(check_username_query, (username,))
    result = cursor.fetchone()

    conn.close()

    return result is not None

def hash_password(password):
    # Hash the password using SHA-256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

def login_user():
    print("=== Existing User Login ===")
    username = input("Enter your username: ")
    password = input("Enter your master password: ")

    # Validate the user's credentials
    user_data = validate_user_credentials(username, password)

    if user_data:
        print("Login successful!")
        user_menu(username)
    else:
        print("Invalid username or password. Please try again.")

def validate_user_credentials(username, password):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    get_user_query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(get_user_query, (username,))
    user_data = cursor.fetchone()

    if user_data and check_password(password, user_data[2]):
        conn.close()
        return user_data
    else:
        conn.close()
        return None

def user_menu(username):
    while True:
        print("""
        User Menu:
        1. Remove a Platform
        2. Add a Platform
        3. Update Password to a Platform
        4. Get Existing Password to a Platform
        5. Change Master Password
        6. Logout
        """)

        choice = input("Enter your choice [1-6]: ")

        if choice == '1':
            remove_platform(username)
        elif choice == '2':
            add_platform(username)
        elif choice == '3':
            update_password(username)
        elif choice == '4':
            get_password(username)
        elif choice == '5':
            change_master_password(username)
        elif choice == '6':
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

def remove_platform(username):
    platform = input("Enter the platform to remove: ")

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    check_platform_query = "SELECT * FROM user_platforms WHERE user_id = (SELECT id FROM users WHERE username = %s) AND platform = %s"
    cursor.execute(check_platform_query, (username, platform))
    result = cursor.fetchone()

    if result:
        remove_platform_query = "DELETE FROM user_platforms WHERE user_id = (SELECT id FROM users WHERE username = %s) AND platform = %s"
        cursor.execute(remove_platform_query, (username, platform))

        conn.commit()
        conn.close()

        print(f"Platform '{platform}' removed successfully.")
    else:
        print(f"Platform '{platform}' does not exist for the user.")

def add_platform(username):
    platform = input("Enter the platform name: ")
    password = input("Enter the password for the platform: ")

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    insert_platform_query = "INSERT INTO user_platforms (user_id, platform, password) VALUES ((SELECT id FROM users WHERE username = %s), %s, %s)"
    cursor.execute(insert_platform_query, (username, platform, password))

    conn.commit()
    conn.close()

    print(f"Platform '{platform}' added successfully.")

def update_password(username):
    platform = input("Enter the platform name to update the password: ")
    new_password = input("Enter the new password: ")

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    update_password_query = "UPDATE user_platforms SET password = %s WHERE user_id = (SELECT id FROM users WHERE username = %s) AND platform = %s"
    cursor.execute(update_password_query, (new_password, username, platform))

    conn.commit()
    conn.close()

    print(f"Password for platform '{platform}' updated successfully.")

def get_password(username):
    platform = input("Enter the platform name to get the password: ")

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    get_password_query = "SELECT password FROM user_platforms WHERE user_id = (SELECT id FROM users WHERE username = %s) AND platform = %s"
    cursor.execute(get_password_query, (username, platform))
    result = cursor.fetchone()

    if result:
        print(f"Password for platform '{platform}': {result[0]}")
    else:
        print(f"No password found for platform '{platform}'.")

    conn.close()

def change_master_password(username):
    new_password = input("Enter your new master password: ")
    hashed_new_password = hash_password(new_password)

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    update_master_password_query = "UPDATE users SET master_password = %s WHERE username = %s"
    cursor.execute(update_master_password_query, (hashed_new_password, username))

    conn.commit()
    conn.close()

    print("Master password changed successfully.")

def check_password(input_password, stored_hashed_password):
    input_password_hashed = hash_password(input_password)    
    return input_password_hashed == stored_hashed_password


# database configuration

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': '<your password>'
}

print("""
(1) Login [Existing User]
(2) New User [Register]
""")

choice = input("Enter your choice [1/2]: ")

if choice == '1':
    login_user()
elif choice == '2':
    create_new_user()
    login_user()
else:
    print("Invalid choice. Please enter either 1 or 2.")
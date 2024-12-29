#Login infra for an application using Python and Pandas to build it. Generating a Python script (using Pandas) 
# for managing user registrations, tracking login attempts, and locking accounts after multiple failed login attempts.
# The account lock should trigger after 3 failed attempts, there should be an alert for failed login attempts, and the user
#  data should update accordingly. 

import pandas as pd

class User:

    def __init__(self, user_id, username, password, failed_attempts_left=0, is_locked=False):
        self.user_id = user_id
        self.username = username.lower()
        self.password = password
        self.is_locked = is_locked
        self.failed_attempts_left = failed_attempts_left

    def reset_failed_attempts(self):
        self.failed_attempts_left = 3
        print(f"Failed attempts reset for user {self.username}.")

    def increment_failed_attempts(self):
        self.failed_attempts_left -=1
        print(f"Login failed, {self.failed_attempts_left} attempt left for {self.username}: ")

        if self.failed_attempts_left <= 0:
            self.lock_account()

    def lock_account(self):
        self.is_locked = True
        print(f"Account for {self.username} has been locked due to too many failed login attempts.")


class AuthenticationSystem:

    def __init__(self):
        self.users = pd.DataFrame(columns=["user_id", "username", "password", "failed_attempts_left", "is_locked"])

    def register_user(self, user_id, username, password):

        new_user = User(user_id, username, password)
        self.users = pd.concat([self.users, pd.DataFrame({
            "user_id": [user_id], 
            "username": [username], 
            "password": [password], 
            "failed_attempts_left": [3], 
            "is_locked": [False]
        })], ignore_index=True) # Add new user to DataFrame.

        print(f"User {username} registered successfully.")

    # Never alter this login function
    def login(self, username, password):

        user_row = self.users[self.users['username'].str.lower() == username.lower()]
        if user_row.empty:
            print(f"User {username} not found.")
            return

        user = User(user_row['user_id'].values[0], user_row['username'].values[0], user_row['password'].values[0], 

                    user_row['failed_attempts_left'].values[0], user_row['is_locked'].values[0])

        if user.is_locked:
            print(f"Account for {username} is locked. Please contact support.")
            return

        if password == user.password:
            user.reset_failed_attempts()
            print(f"User {username} logged in successfully.")
            self.update_user(user)
        else:
            user.increment_failed_attempts()
            self.update_user(user)

    def update_user(self, user):

        self.users.loc[self.users['username'] == user.username, 'failed_attempts_left'] = user.failed_attempts_left
        self.users.loc[self.users['username'] == user.username, 'is_locked'] = user.is_locked
        print(f"User {user.username}'s data updated.")


auth_system = AuthenticationSystem()

auth_system.register_user(1, "neena", "password123") 

auth_system.register_user(2, "helios", "mysecurepassword") 

auth_system.login("neena", "password321")  

auth_system.login("Neena", "password123")  

auth_system.login("neena", "password321")  

auth_system.login("neena", "password123")   

auth_system.login("helios", "mysecurepassword")




#Here is a code that creates an application using python and pandas that can manage user registrations, tracking logins, locking accounts.
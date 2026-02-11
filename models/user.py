import bcrypt  # Import bcrypt for password hashing and checking
from pydantic import BaseModel

class user:
    def __init__ (self, user_id, name, email, password, user_type, password_is_hashed=False):
        self.user_id = user_id  # Store the user's ID
        self.name = name  # Store the user's name
        self.email = email  # Store the user's email address
        if password_is_hashed:
            self.password = password  # Assume password is already hashed (bytes)
        else:
            self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Hash and store the user's password securely, can get rid of bcrypt.gensalt() as it may slow down the system in high levels of production.
        self.user_type = user_type  # Store the user's type (e.g., 'admin', 'parent', 'teacher', or 'student')

    def display_info(self):
        print('User Information:')  # Print header for user info
        print('User ID: ' + str(self.user_id))  # Print the user's ID
        print('Name: ' + self.name)  # Print the user's name
        print('Email: ' + self.email)  # Print the user's email
        print('User Type: ' + self.user_type)  # Print the user's type

    def change_password(self, new_password):
        self.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())  # Hash and update the password
        print('Password changed successfully.')  # Confirm password change

    def check_password(self, password):
        if bcrypt.checkpw(password.encode('utf-8'), self.password):  # Check if provided password matches stored hashed password
            print('Password is correct.')  # Reply that password is correct
            return True
        else:
            print('Password is incorrect.')  # Reply that password is incorrect
            return False

    def get_user_id(self):  # Returns the user's unique ID
        return self.user_id

    def get_email(self):  # Returns the user's email address
        return self.email

    def get_user_type(self):  # Returns the user's type (e.g. student, teacher)
        return self.user_type

    def set_email(self, new_email):  # Updates the user's email with a new value
        self.email = new_email  # Assigns the new email to the user's email attribute
        print('Email updated successfully.')  # Prints confirmation message

    def set_user_type(self, new_user_type):  # Updates the user's type (e.g. from student to admin)
        self.user_type = new_user_type  # Assigns the new type to the user's user_type attribute
        print('User type updated successfully.')  # Prints confirmation message


# Pydantic model for incoming user registration data
class UserCreate(BaseModel):
    user_id: int
    name: str
    email: str
    password: str
    user_type: str

# Existing Pydantic model for response
class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    user_type: str

    
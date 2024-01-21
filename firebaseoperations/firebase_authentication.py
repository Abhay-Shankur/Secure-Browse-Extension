import firebase_admin
from firebase_admin import auth


def sign_up(email, password):
    try:
        # Create a new user account
        user = auth.create_user(email=email, password=password)
        print(f"User created successfully: {user.uid}")
        return user.uid
    except Exception as e:
        print(f"Error creating user: {e}")
        return None


def sign_in(email, password):
    try:
        # TODO: Signin
        # Sign in with email and password
        # user = auth.get_user_by_email(email)
        # auth.generate_sign_in_with_email_link(email, ACTIOn)
        auth_user = auth.sign_in_with_email_and_password(email=email, password=password)
        print(f"User signed in successfully: {auth_user.uid}")
        return auth_user.uid
    except Exception as e:
        print(f"Error signing in: {e}")
        return None


def check_authentication(uid):
    try:
        # Get user data
        user = auth.get_user(uid)
        print(f"User is signed in: {user.uid}")
        return user
    except Exception as e:
        print(f"User is not signed in: {e}")
        return None



# # Example usage:
# if __name__ == "__main__":
#     # Replace 'path/to/your/credentials.json' with your Firebase credentials file path
#     credentials_path = 'path/to/your/credentials.json'
#
#     # Replace 'your-app-name' with your Firebase app name
#     app_name = 'your-app-name'
#
#     # Create an instance of FirebaseAuthentication
#     firebase_auth = FirebaseAuthentication(cred_path=credentials_path, app_name=app_name)
#
#     # Example: Sign up a new user
#     new_user_uid = firebase_auth.sign_up(email='example@example.com', password='password123')
#
#     # Example: Sign in the user
#     signed_in_user_uid = firebase_auth.sign_in(email='example@example.com', password='password123')
#
#     # Example: Check if the user is signed in
#     if signed_in_user_uid:
#         firebase_auth.check_authentication(uid=signed_in_user_uid)
#
#     # Example: Close the Firebase connection
#     firebase_auth.close_connection()

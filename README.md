# Your Project Name

This project is test project implementing django auth.

## Description

This project is divided into two main parts:

1. **Django Web Version**: The web version is a website for users. The code for the web version is located in the web folder.

2. **API**: The API provides a set of endpoints for interacting with the project's data. The code for the API is located in the api folder.

## Installation and Running

To run the project, follow these steps:

1. Install Python.
2. Clone the repository: `git clone https://github.com/your_project.git`.
3. Navigate to the project directory: `cd your_project`.
4. Install dependencies: `pip install -r requirements.txt`.
5. Apply migrations: `python manage.py migrate`.
6. Run the server: `python manage.py runserver`.

## API Endpoints

Here is a list of endpoints available in the API:

1. **Send Code**: 
   - Endpoint: `/api/login/send-code/`
   - Description: Sends a verification code to the provided phone number.
   - Method: POST
   - Parameters: `phone_number` (in form data)
   - Response: JSON {"code_sent": "true"} on success
   
2. **Verify Code**: 
   - Endpoint: `/api/login/verify-code/`
   - Description: Verifies the code sent to the phone number.
   - Method: POST
   - Parameters: `inserted_code`, `phone_number` (in form data)
   - Response: JSON {"auth": true, "token": <token>} on success, {"error": 'Invalid auth code'} on failure
   
3. **Add User**: 
   - Endpoint: `/api/login/add-user/`
   - Description: Creates a new user.
   - Method: POST
   - Parameters: `token`, `phone_number`, `first_name`, `last_name`, `username`, `password` (in form data)
   - Response: JSON with user data on success, {'error': '<error_message>'} on failure
   
4. **Verificate User**: 
   - Endpoint: `/api/login/verificate-user/`
   - Description: Verifies user credentials and returns an authorization token.
   - Method: POST
   - Parameters: `username`, `password` (in form data)
   - Response: JSON with user data and authorization token on success, {'error': '<error_message>'} on failure
   
5. **Logout User**: 
   - Endpoint: `/api/logout/`
   - Description: Logs out the user.
   - Method: GET
   - Headers: `Authorization` with token
   - Response: {'error': '<error_message>'} on failure
   
6. **Get User by ID**: 
   - Endpoint: `/api/user/<id>/`
   - Description: Retrieves user information by ID.
   - Method: GET
   - Parameters: `id` (in URL path), `Authorization` with token (in headers)
   - Response: JSON with user data (excluding invited users) on success, {'error': '<error_message>'} on failure
   
7. **Apply Invite Code**: 
   - Endpoint: `/api/user/<id>/apply-invite-code/`
   - Description: Applies an invite code to the user.
   - Method: POST
   - Parameters: `invite_code` (in form data), `Authorization` with token (in headers)
   - Response: JSON with updated user information on success, {'error': '<error_message>'} on failure
   
8. **Get Invited Users**: 
   - Endpoint: `/api/user/<id>/get-invited-users/`
   - Description: Retrieves the list of invited users.
   - Method: GET
   - Parameters: `id` (in URL path), `Authorization` with token (in headers)
   - Response: JSON with the list of invited users on success, {'error': '<error_message>'} on failure

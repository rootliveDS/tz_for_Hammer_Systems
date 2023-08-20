Phone Number Authorization API
===============================================================================================  

pythonanywhere -  https://beritedeveng.pythonanywhere.com/api/  
postman - https://universal-astronaut-310693.postman.co/workspace/Team-Workspace~251543b8-bf42-4fca-83da-d8a7a1238431/collection/29202813-fc7fde85-54f9-46a3-899f-6292ea2c67c5?action=share&creator=29202813

This API provides functionality for phone number authorization, user profiles, and invitation codes.

Endpoints

Request Authorization Code
===============================================================================================
Send a request to get an authorization code for a given phone number.  
URL: /api/request-auth-code/  

Method: POST  

Data Params:  
phone_number: The phone number to send the authorization code to (e.g., +79236151151).

Success Response:  
Code: 200  
Content: { "message": "Authorization code sent successfully. Your authorization_code is: 2991"}  


Error Response:    
Code: 400  
Content: { "error": "Phone number is required." }  

Verify Authorization Code  
===============================================================================================
Verify the authorization code for a given phone number and grant access if valid.


URL: /api/verify-auth-code/{phone_number}/  

Method: POST   

URL Params:  
phone_number: The phone number to verify the authorization code for (e.g., +79236151151).  

Data Params:  
authorization_code: The authorization code provided by the user.  

Success Response:    
Code: 200  
Content: { "message": "Authorization successful." }  
  
Error Response:  
Code: 400  
Content: { "error": "Phone number and authorization code are required." }  
Code: 400  
Content: { "error": "Invalid authorization code." }  
Code: 400  
Content: { "error": "User not found." }  
Code: 400  
Content: { "message": "Phone number is already authorized." }  


User Profile  
===============================================================================================
View and manage user profiles, including invitation codes.  

URL: /api/user-profile/{phone_number}/  

Method: GET, POST  

URL Params:  
phone_number: The phone number of the user profile to view/manage (e.g., +79236151151).  

Data Params (for POST request):  
personal_code: The invitation code to activate (if applicable).  

Success Response:  
Code: 200  
Content: { "phone_number": "+79236151151", "is_authorized": true, "personal_code": "ABC123", "invited_phone": ["9876543210", "5555555555"] } 

Error Response:  
Code: 404  
Content: { "error": "User not found." }  
Code: 400  
Content: { "error": "Invite code is required." }  
Code: 400  
Content: { "error": "Invalid invite code." }  
Code: 401  
Content: { "error": "Unauthorized request." }  
Code: 400  
Content: { "message": "The user has already been added to the invite." }  

Usage  
===============================================================================================
Send a POST request to /api/request-auth-code/ with the phone_number parameter to receive an authorization code.  
Verify the authorization code by sending a POST request to /api/verify-auth-code/{phone_number}/ with the authorization_code parameter.  

Access user profiles via GET requests to /api/user-profile/{phone_number}/.  

Activate invitation codes by sending a POST request to /api/user-profile/{phone_number}/ with the personal_code parameter.  


Installation  
===============================================================================================
Clone this repository.  

Install the required packages using pip install -r requirements.txt.  

Run the development server using python3 manage.py runserver.

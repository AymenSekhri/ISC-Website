# ISC-Server

## Installation

```
python pip install -r requirements.txt
python manage.py runserver 0.0.0.0:80
```

## TODO list

Client Side :

- Frontend  for "Forgot password" page.
- Frontend  for "Reset password" page.
- Frontend  for "Thank your for registration" page.
- Frontend  for "Your password has been reset, login now" page.
- Frontend  for "Edit User Information" page.
- Frontend  for "User Profile" page.
- Frontend  for "Home page" page.
- Frontend  for "Download Study Materials" page.
- Adding more styles to the error retured by the server when there is an error with signup and login forms.
- Fixing the navigation bar (there is a little more margin in the left)

Server Side :

- Backend for "Edit User Informations" page.
- Backend for "User Profile" page.
- Backenend  for "Download Study Materials" page.
- Setup email server to send the Password Reset Token
- Creating new admin page instead of Django's


## Information

- HTML files are in the path 
```
ISC-Server/ISC_Server/UsersApp/templates/UsersApp/
```

- CSS/JS files are in the path 
```
ISC-Server/ISC_Server/UsersApp/static/UsersApp/
```
- When you issue a password reset the token will be printed in the console screen (green color) since i have not setup the the email server yet.

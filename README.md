# ISC-Server

## Information

- it is just one app for the whole website which is `UsersApp`. The app `MainApp` was used just for testing.
- You can access admin page and view/edit/delete database's items via the link `localhost/admin`
use the following information to login
```
User Name : 0xcc
Password : 123
```
- You will have better experience and productivity if you open the project using Visual Studio 2017 or higher.
- HTML files are in the path 
```
ISC-Server/ISC_Server/UsersApp/templates/UsersApp/
```

- CSS/JS files are in the path 
```
ISC-Server/ISC_Server/UsersApp/static/UsersApp/
```
- When you issue a password reset the token will be printed in the console screen (green color) since i have not setup the the email server yet.

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
- Fixing the lag in the siliding bar on the home page

Server Side :

- Backend for "Edit User Information" page.
- Backend for "User Profile" page.
- Backend for "Download Study Materials" page.
- Setup an email server to send the Password Reset Token
- Creating a new admin page instead of Django's

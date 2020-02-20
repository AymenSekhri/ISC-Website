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

## API list

# api/register
# api/login
# api/logout
# api/loginInfo
# api/forgotpassword
# api/resetpassword
# api/events
# api/events/create
# api/events/<int:id>
# api/events/<int:id>/manage
# api/events/<int:id>/list
# api/events/<int:id>/postpone
# api/events/<int:id>/enroll
# api/events/<int:id>/decision
# api/news/create
# api/news/<int:id>
# api/news/<int:id>/edit
# api/news/<int:id>/delete
# api/projects/create
# api/projects/<int:id>
# api/projects/<int:id>/edit
# api/projects/<int:id>/delete
# api/team/add
# api/team/<int:id>
# api/team/<int:id>/edit
# api/team/<int:id>/delete
# api/users
# api/users/<int:id>
# api/users/<int:id>/edit
# api/users/<int:id>/delete
# api/contact



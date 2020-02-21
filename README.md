# Information

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

# Installation

```
python pip install -r requirements.txt
python manage.py runserver 0.0.0.0:80
```

# API list

## api/register
Register new user.
### Request:POST
* firstName[max=30,min=3]</br>
* familyName[max=30,min=3]</br>
* email</br>
* pass1[min=8]</br>
* pass2[min=8]</br>
* number[max=20]</br>
* year[max=4]</br>
### Response
*Status</br>
### Status Codes
SUCCESS = 0</br>
USEREXISTS = 1</br>
EMAILEXISTS = 2</br>
PASSMISSMATCH = 3</br>
## api/login
Signin.
### Request:POST
* email
* password
### Response
* Status
### Status Codes
* SUCCESS = 0
* EMAIL_NOT_FOUND = 1
* PASS_MISMATCH = 2

This api sets "session_id" and "user_id" in response cookie.
## api/logout
Signout.
## api/loginInfo
Get information about the user of current session.
### api/forgotpassword
Forgot password form.
## api/resetpassword
Resetpassword form.
## api/events
Get list of all events.
## api/events/create
Create new event.
## api/events/<int:id>
Get information about an event.
## api/events/<int:id>/manage
Cancel/delete event or send email to accepted users.
## api/events/<int:id>/list
Get list of users who enrolled the event.
## api/events/<int:id>/postpone
Postpone an event or postpone enrollment deadline.
## api/events/<int:id>/enroll
Enroll an event.
## api/events/<int:id>/decision
Make decision about an enrollment.
## api/news
Get a list of the news.
## api/news/create
Create new News post.
## api/news/<int:id>
Get details of a news post.
## api/news/<int:id>/edit
Edit a News post.
## api/news/<int:id>/delete
Delete a News post.
## api/projects/create
Create new project post.
## api/projects
Get a list of the projects.
## api/projects/<int:id>
Get details of project post.
## api/projects/<int:id>/edit
Edit project post.
## api/projects/<int:id>/delete
Delete project post.
## api/team
Get a list of the team members.
## api/team/add
Add new team member.
## api/team/<int:id>
Get details of a team member.
## api/team/<int:id>/edit
Edit details of a team member.
## api/team/<int:id>/delete
Delete a team member.
## api/users
Get a list of the users.
## api/users/<int:id>
Get the details of a user.
## api/users/<int:id>/edit
Edit the details of a user.
## api/users/<int:id>/delete
Delete a user.
## api/contact
Contact us form.



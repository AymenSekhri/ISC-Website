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

### api/register
Register new user.
### api/login
Signin.
### api/logout
Signout.
### api/loginInfo
Get information about the user of current session.
### api/forgotpassword
Forgot password form.
### api/resetpassword
Resetpassword form.
### api/events
Get list of all events.
### api/events/create
Create new event.
### api/events/<int:id>
Get information about an event.
### api/events/<int:id>/manage
Cancel/delete event or send email to accepted users.
### api/events/<int:id>/list
Get list of users who enrolled the event.
### api/events/<int:id>/postpone
Postpone an event or postpone enrollment deadline.
### api/events/<int:id>/enroll
Enroll an event.
### api/events/<int:id>/decision
Make decision about an enrollment.
### api/news
Get a list of the news.
### api/news/create
Create new News post.
### api/news/<int:id>
Get details of a news post.
### api/news/<int:id>/edit
Edit a News post.
### api/news/<int:id>/delete
Delete a News post.
### api/projects/create
Create new project post.
### api/projects
Get a list of the projects.
### api/projects/<int:id>
Get details of project post.
### api/projects/<int:id>/edit
Edit project post.
### api/projects/<int:id>/delete
Delete project post.
### api/team
Get a list of the team members.
### api/team/add
Add new team member.
### api/team/<int:id>
Get details of a team member.
### api/team/<int:id>/edit
Edit details of a team member.
### api/team/<int:id>/delete
Delete a team member.
### api/users
Get a list of the users.
### api/users/<int:id>
Get the details of a user.
### api/users/<int:id>/edit
Edit the details of a user.
### api/users/<int:id>/delete
Delete a user.
### api/contact
Contact us form.



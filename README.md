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

# TODO list

* Add a model for notifications.
* Add Upload Profile Picture feature.
* Adjust Privilege levels for each API.
* Build 'Contact us' from.
* Set up email server and add 'send email' code in the required APIs.
* Log requests.
# [API Documentation](https://github.com/AymenSekhri/ISC-Server/blob/master/API%20documentations.md)

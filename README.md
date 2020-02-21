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
#### Request: POST
* firstName[max=30,min=3]</br>
* familyName[max=30,min=3]</br>
* email</br>
* pass1[min=8]</br>
* pass2[min=8]</br>
* number[max=20]</br>
* year[max=4]</br>
#### Response
* Status</br>
#### Status Codes
* SUCCESS = 0</br>
* USEREXISTS = 1</br>
* EMAILEXISTS = 2</br>
* PASSMISSMATCH = 3</br>
## api/login
Signin.
#### Request: POST
* email
* password
#### Response
* Status
#### Status Codes
* SUCCESS = 0
* EMAIL_NOT_FOUND = 1
* PASS_MISMATCH = 2

This api sets "session_id" and "user_id" in response cookie.

## api/logout
Signout.
#### Request: GET
#### Response
* Status
#### Status Codes
* SUCCESS = 0

This API requires a logged in user and valid session_id in cookies otherwise 400 htttp status code is returned.
## api/loginInfo
Get information about the user of current session.
#### Request: GET
#### Response
* Status
* Data
	* id
	* firstName
	* familyName
	* email
	* number
	* privLevel
#### Status Codes
* SUCCESS = 0

This API requires a logged in user and valid session_id in cookies otherwise 400 htttp status code is returned.
## api/forgotpassword
Forgot password form.
#### Request: POST
* email
#### Response
* Status
#### Status Codes
* SUCCESS = 0
* EMAIL_NOT_FOUND = 1
* INVALID_TOKEN = 2

This API sends the token to the user's email, which will be used to change password in 'api/resetpassword' API.
## api/resetpassword
Resetpassword form.

#### Request: POST
* password
* token
#### Response
* Status
#### Status Codes
* SUCCESS = 0
* EMAIL_NOT_FOUND = 1
* INVALID_TOKEN = 2

## api/events
Get list of all events.
#### Request: GET
#### Response
* Status
* Data
	* id
	* name
	* picture
	* description
	* deadline_date
	* event_date
	* eventStatus
	
#### Status Codes
* SUCCESS = 0

## api/events/create
Create new event.

#### Request: POST
* eventName
* description
* deadline_date (format: "D-M-Y")
* event_date (format: "D-M-Y H:M")
* maxNumberOfEnrolment
* enrollmentData

#### Response
* Status
#### Status Codes
* SUCCESS = 0
* EVENTEXISTS = 1
* INVALIDDATEFORMAT = 2
* EVENTDOESNOTEXISTS = 3

This API requires a logged in user with appropriate privilege level and valid session_id in cookies otherwise 400 htttp status code is returned.</br>
The 'enrollmentData' will contain the question that will be asked to enroll the event.</br>

## api/events/<int:id>
Get information about an event.
#### Request: GET
#### Response
* Status
* Data
	* name
	* picture
	* description
	* maxNumberOfEnrolment
	* numberOfEnrolment
	* posting_date
	* event_date
	* deadline_date
	* eventEnrolmentData
	* eventStatus
	
#### Status Codes
* SUCCESS = 0

If an event's id that doesn't exist is being accessed, a 404 http status code will be returned.</br>
## api/events/<int:id>/manage
Cancel/delete event or send email to accepted users.

#### Request: POST
* cmd

#### Response
* Status
#### Status Codes
* SUCCESS = 0
* EVENTDOESNOTEXISTS = 1

This API requires a logged in user with appropriate privilege level and valid session_id in cookies otherwise 400 htttp status code is returned.</br>
To Cancel an event send cmd='cnl'<br>
To Remove an event send cmd='rm'<br>

## api/events/<int:id>/list
Get list of users who enrolled the event.
#### Request: GET
#### Response
* Status
* Data
	* id
	* name
	* email
	* year
	* enrolemnt_date
	* enrolmentResponse
	* decision
	
#### Status Codes
* SUCCESS = 0

## api/events/<int:id>/postpone
Postpone an event or postpone enrollment deadline.
#### Request: POST
* cmd
* newDate (format: "D-M-Y" or "D-M-Y H:M")
#### Response
* Status
#### Status Codes
* SUCCESS = 0
* EVENTEXISTS = 1
* INVALIDDATEFORMAT = 2
* EVENTDOESNOTEXISTS = 3

This API requires a logged in user with appropriate privilege level and valid session_id in cookies otherwise 400 htttp status code is returned.</br>
To Postpone an event send cmd='pse' and newDate with format "D-M-Y H:M"<br>
To Postpone Enrollment Deadline send cmd='pdl' and newDate with format "D-M-Y"<br>


## api/events/<int:id>/enroll
Enroll an event.
#### Request: POST
* response

#### Response
* Status
#### Status Codes
* SUCCESS = 0
* DUPLICATES = 1
* EVENTDOESNOTEXISTS = 2
* MAXNUMBEROFENROLMENTS = 3
* ENROLLMENTDOESNOTEXISTS = 4
* ENROLLMENTPASTDEADLINE = 5

This API requires a logged in user and valid session_id in cookies otherwise 400 htttp status code is returned.</br>
The 'response' field will contain the answers of the question from that associated to the event.</br>


## api/events/<int:id>/decision
Make decision about an enrollment.

#### Request: POST
* userID
* decision

#### Response
* Status
#### Status Codes
* SUCCESS = 0
* EVENTEXISTS = 1
* INVALIDDATEFORMAT = 2
* EVENTDOESNOTEXISTS = 3

This API requires a logged in user with appropriate privilege level and valid session_id in cookies otherwise 400 htttp status code is returned.</br>
This API will apply the decision on the user specified by 'userID' field which is enrolled the event specified by the event' id <int:id> in the URL.</br>
The 'decision' can be either of the following values :
	* PENDING = 0
    * ACCEPTED = 1
    * REJECTED = 2

## api/news
Get a list of the news.
#### Request: GET

#### Response
* Status
* Data
	* id
	* title
	* user
	* tags
	* date

#### Status Codes
* SUCCESS = 0

## api/news/create
Create new News post.

#### Request: POST
* title
* content
* tags

#### Response
* Status
#### Status Codes
* SUCCESS = 0

This API requires a logged in user with appropriate privilege level and valid session_id in cookies otherwise 400 htttp status code is returned.</br>

## api/news/<int:id>
Get details of a news post.

#### Request: GET

#### Response
* Status
* Data
	* id
	* title
	* user
	* tags
	* date
	* content
	
#### Status Codes
* SUCCESS = 0

If a post's id that doesn't exist is being accessed, a 404 http status code will be returned.</br>

## api/news/<int:id>/edit
Edit a News post.

#### Request: POST
* title
* content
* tags

#### Response
* Status
#### Status Codes
* SUCCESS = 0

This API requires a logged in user with appropriate privilege level and valid session_id in cookies otherwise 400 htttp status code is returned.</br>
If a post's id that doesn't exist is being accessed, a 404 http status code will be returned.</br>

## api/news/<int:id>/delete
Delete a News post.

#### Request: GET
#### Response
* Status
#### Status Codes
* SUCCESS = 0

This API requires a logged in user with appropriate privilege level and valid session_id in cookies otherwise 400 htttp status code is returned.</br>
If a post's id that doesn't exist is being accessed, a 404 http status code will be returned.</br>

## api/projects/create
Create new project post.

#### Request: POST
* title
* content
* tags

#### Response
* Status
#### Status Codes
* SUCCESS = 0

This API requires a logged in user with appropriate privilege level and valid session_id in cookies otherwise 400 htttp status code is returned.</br>

## api/projects
Get a list of the projects.

#### Request: GET

#### Response
* Status
* Data
	* id
	* title
	* user
	* tags
	* date
	
#### Status Codes
* SUCCESS = 0

## api/projects/<int:id>
Get details of project post.

#### Request: GET

#### Response
* Status
* Data
	* id
	* title
	* user
	* tags
	* date
	* content
	
#### Status Codes
* SUCCESS = 0

If a post's id that doesn't exist is being accessed, a 404 http status code will be returned.</br>

## api/projects/<int:id>/edit
Edit project post.

#### Request: POST
* title
* content
* tags

#### Response
* Status
#### Status Codes
* SUCCESS = 0

This API requires a logged in user with appropriate privilege level and valid session_id in cookies otherwise 400 htttp status code is returned.</br>
If a post's id that doesn't exist is being accessed, a 404 http status code will be returned.</br>

## api/projects/<int:id>/delete
Delete project post.

#### Request: GET
#### Response
* Status
#### Status Codes
* SUCCESS = 0

This API requires a logged in user with appropriate privilege level and valid session_id in cookies otherwise 400 htttp status code is returned.</br>
If a post's id that doesn't exist is being accessed, a 404 http status code will be returned.</br>

## api/team
Get a list of the team members.

#### Request: GET
#### Response
* Status
* Data
	* id
	* userID
	* firstName
	* lastName
	* title
	* bio
	* contacts
	* date

#### Status Codes
* SUCCESS = 0

## api/team/add
Add new team member.

#### Request: POST
* userID
* title
* bio
* contacts

#### Response
* Status

#### Status Codes
* SUCCESS = 0
* INVALID_USER = 1
* DUPLICATED_USER = 2

This API requires a logged in user with appropriate privilege level and valid session_id in cookies otherwise 400 htttp status code is returned.</br>

## api/team/<int:id>/edit
Edit details of a team member.

#### Request: POST
* title
* bio
* contacts

#### Response
* Status

#### Status Codes
* SUCCESS = 0
* INVALID_USER = 1


This API requires a logged in user with appropriate privilege level and valid session_id in cookies otherwise 400 htttp status code is returned.</br>
If a member's id that doesn't exist is being accessed, a 404 http status code will be returned.</br>

## api/team/<int:id>/delete
Delete a team member.

#### Request: GET
#### Response
* Status
#### Status Codes
* SUCCESS = 0

This API requires a logged in user with appropriate privilege level and valid session_id in cookies otherwise 400 htttp status code is returned.</br>
If a member's id that doesn't exist is being accessed, a 404 http status code will be returned.</br>

## api/users
Get a list of the users.

#### Request: GET
#### Response
* Status
* Data
	* id
	* firstName
	* familyName
	* number
	* year
	
#### Status Codes
* SUCCESS = 0

This API requires a logged in user with appropriate privilege level and valid session_id in cookies otherwise 400 htttp status code is returned.</br>

## api/users/<int:id>
Get the details of a user.

#### Request: GET
#### Response
* Status
* Data
	* id
	* firstName
	* familyName
	* privLevel
	* regDate
	* email
	* number
	* year
	
#### Status Codes
* SUCCESS = 0

This API requires a logged in user with appropriate privilege level and valid session_id in cookies otherwise 400 htttp status code is returned.</br>
If a user's id that doesn't exist is being accessed, a 404 http status code will be returned.</br>

## api/users/<int:id>/edit
Edit the details of a user.

#### Request: POST
* firstName
* familyName
* email
* number

#### Response
* Status
#### Status Codes
* SUCCESS = 0

## api/users/<int:id>/delete
Delete a user.

#### Request: GET
#### Response
* Status
#### Status Codes
* SUCCESS = 0

This API requires a logged in user with appropriate privilege level and valid session_id in cookies otherwise 400 htttp status code is returned.</br>
If a user's id that doesn't exist is being accessed, a 404 http status code will be returned.</br>

## api/contact
Contact us form.



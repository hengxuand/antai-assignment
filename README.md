Antai assignment API

GitHub link: https://github.com/hengxuand/antai-assignment
Server link: https://antai-assignment.herokuapp.com/

Server design

The backend server is using python and Flask. It uses SQLite for the database. Before starting the server, run “python3 createdb.py” to initialize the database. Then run “python3 app.py” to start the server. In the database, there is one table called “members” which contains three columns, “id”, “username”, and “email”. Id column is unique member identifiers. 

The deployment of the server is using Heroku which provides amazing platform services for deploying web servers with many programming languages.

API design

My server is a RESTful api server. It supports CRUD and pagination. To make requests, you simply append API routes after the Heroku server link. The following list shows steps and details to make requests. The software used here is Postman.










Get members’ information

Request method: GET
URL pattern: https://antai-assignment.herokuapp.com/api/member?items=20&page=1
Parameters: items, page
Returning data: A list of JSON objects containing the first 20 members’ information in this particular case. 

The server takes the parameters {items} and {page} and decides the content to return. For example, if you pass items=3 and page=2, the information of members from 4th to 6th will be returned.











Add new member

Request method: POST
URL pattern: https://antai-assignment.herokuapp.com/api/member
Parameters: username, email. Parameters need to be built into the request’s body for POST requests.
Returning data: A JSON object sent from the server. The status indicated whether the adding process was successful.

The server, firstly, generates a new unique id for the new member and then stores a new entry into the database with the username, email, and id.










Update member’s information

Request method: PATCH
URL pattern: https://antai-assignment.herokuapp.com/api/member
Parameters: id, username, email. Parameters need to be built into the request’s body for PATCH requests.
Returning data: A JSON object sent from the server. The status indicated whether the updating process was successful.

The server finds the entry in database with id. If the member does not exist, it will return “status”: “fail”. If the member exists, it will update username and email using provided parameters and return “status”: “success”.










Delete one member

Request method: DELETE
URL pattern: https://antai-assignment.herokuapp.com/api/member
Parameters: id. Parameters need to be built into the request’s body for DELETE requests.
Returning data: A JSON object sent from the server. The status indicated whether the deletion process was successful.

The server finds the entry in database with the id. If the member does not exist, it will return “status”: “fail”. If the member exists, it will delete the entry and return “status”: “success”.










Search members based on given term

Request method: GET
URL pattern: https://antai-assignment.herokuapp.com/api/search?term=hengxuan
Parameters: term
Returning data: A list of JSON objects containing members whose username matches or contains the given term. 

The server takes the parameters {term} to match with username column in database. The more specific term gives more accurate results.











Send greeting email to one member

Request method: Post
URL pattern: https://antai-assignment.herokuapp.com/api/greeting
Parameters: id. Parameters need to be built into the request’s body for POST requests.
Returning data: A JSON object sent from the server. The status indicated whether the sending  process was successful.

The server finds the entry in database based on the given id. If the member does not exist, it will return “status”: “fail”. If the member exists, it will call SendGrid API and send a greeting email to the email address of the entry.


    My personal email received the greeting email from the server.


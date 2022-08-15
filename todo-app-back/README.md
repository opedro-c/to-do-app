# To-Do API

The To-Do API is built with Flask and is intended to provide an authorization layer with JWT and manage the client tasks in the SQLite3 database.

## Summary

- User
	- [Register User](#register-user)
	- [Get Access Token](#get-access-token)
	- [Get User Status](#get-user-status)
    - [List all users](#list-all-users)
- Task
	- [Get User Tasks](#get-user-tasks)
	- [Create new task](#create-new-task)
	- [Update task](#update-task)
	- [Delete task](#delete-task)

### Authentication

| Security Scheme Type      | HTTP   |
|---------------------------|--------|
| HTTP Authorization Scheme | bearer |
 | Bearer format             | JWT    |

### Register User

|  Method        | POST             |
|----------------|------------------|
 | URL            | auth/register    |
| Request schema | application/json |

Request body fields:

- **_required_** name: string
- **_required_** email: string
- **_required_** password: string

Responses:

- 201 &#8594; Successfully registered
- 400 &#8594; Invalid data provided

Request sample:

```json
{
	"name": "Foo Bar",
	"email": "foo@bar.com",
	"password": "strongandcomplicatedpassword"
}
```

Response sample:

```json
{
	"status": "success",
	"message": "Successfully registered",
	"auth_token": "786e91a0-1be4-4328-96f7-3539bbbfa9f9"
}
```

### Get Access Token

| Method         | POST             |
|----------------|------------------|
| URL            | auth/login       |
| Request schema | application/json |

Request body fields:

- **_required_** email: string
- **_required_** password: string

Responses:

- 200 &#8594; Success
- 400 &#8594; Invalid data provided

Request sample:

```json
{
	"email": "foo@bar.com",
	"password": "strongandcomplicatedpassword"
}
```

Response sample:

```json
{
	"status": "success",
	"message": "Successfully logged in",
	"auth_token": "786e91a0-1be4-4328-96f7-3539bbbfa9f9"
}
```

### Get User Status

| Method        | GET         |
|---------------|-------------|
| Authorization | bearerAuth  |
 | URL           | auth/status |

Responses:

- 200 &#8594; Success
- 401 &#8594; Unauthorized

Response sample:

```json
{
	"status": "success",
	"data": 
		{
			"id": 1234,
			"name": "Foo Bar"
		}
}
```

### List All Users

 | Method | GET   |
|--------|-------|
| URL    | users |

Responses:

- 200 &#8594; Success

Response sample:

```json
[
	{
		"name": "User1",
		"email": "user1@email.com"
	},
	{
		"name": "User2",
		"email": "user2@email.com"
	}
]
```

## Task

### Get User Tasks

| Method | GET   |
|--------|-------|
|  URL   | /task |

Responses:

- 200 &#8594; Success
- 401 &#8594; Unauthorized

Response sample:

```json
[
	{
		"id": 456,
		"name": "Do something important",
		"description": "That's really important",
		"done": false,
		"date": "2011-11-11"
	},
	{
		"id": 123,
		"name": "Wash dishes",
		"description": "That's really boring",
		"done": true,
		"date": "2011-11-10"
	}
]
```

### Create new task

| Method          | POST             |
|-----------------|------------------|
| Authorization   | bearerAuth       |
 | URL             | /task            |
|  Request schema | application/json |

Request body fields:

- **_required_** name: string
- **_required_** date: string (ISO format)
- description: string
- done: boolean

Responses:

- 201 &#8594; Successfully created
- 400 &#8594; Invalid data provided
- 401 &#8594; Unauthorized

Request sample:

```json
{
	"name": "Do something important",
	"description": "That's really important",
	"done": false,
	"date": "2011-11-11"
}
```

Response sample:

```json
{
	"name": "Do something important",
	"description": "That's really important",
	"done": false,
	"date": "2011-11-11"
}
```

### Update task

| Method          | PUT               |
|-----------------|-------------------|
| Authorization   | bearerAuth        |
| URL             | /task/{{task_id}} |
|  Request schema | application/json  |

Request body fields:

- name: string
- date: string (ISO format)
- description: string
- done: boolean

Responses:

- 200 &#8594; Success
- 400 &#8594; Invalid data provided
- 401 &#8594; Unauthorized

Request sample:

```json
{
	"name": "Do something important",
	"description": "That's really important",
	"done": false,
	"date": "2011-11-11"
}
```

Response sample:

```json
{
	"name": "Do something important",
	"description": "That's really important",
	"done": false,
	"date": "2011-11-11"
}
```

### Delete task

| Method        | Delete            |
|---------------|-------------------|
| Authorization | bearerAuth        |
 | URL           | /task/{{task_id}} |

Responses:

- 200 &#8594; Success
- 400 &#8594; Invalid data provided
- 401 &#8594; Unauthorized

Response sample:

```json
true
```

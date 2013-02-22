#Introduction#

[saborear](https://github.com/diesire/saborear) is a simple rating REST web service example.

##Server##

Data is retrieved in JSON format

Server currently supports the following requests:

###Root###

*	uri: `/`, method: `GET`, description: returns a list of supported operations. 
	
	Return
	
		[{"operations": ["GET", "POST"], "route_id": "ratings", "uri": "/ratings"},
		{"operations": ["GET"], "route_id": "users", "uri": "/users"},
		{"operations": ["GET"], "route_id": "targets", "uri": "/targets"}]


###Ratings###

*	uri: `/ratings`, method: `GET`, description: returns a list of rating objects

	Return
	
		[{"id": "511fab02561193519fbc979b", "uri": "/ratings/511fab02561193519fbc979b"},
		{"id": "511fac1256119351ca606b75", "uri": "/ratings/511fac1256119351ca606b75"}
	
*	uri: `/ratings`, method: `POST`, description: adds a new rating

	Param
	
		{"comment": "Regular",
		"user_id": "test",
		"target_id": "Quesu",
		"value": "5"}
	
	Return
	
		Status code: 201
	
*	uri: `/ratings/<id>` method: `GET`, description: returns the requested rating object
	
	Return
	
		{"comment": "Regular",
		"user_id": "test",
		"target_id": "Quesu",
		"value": "5",
		"id": "511fab02561193519fbc979b"}
	
*	uri: `/ratings/<id>` method: `PUT`, description: modifies the requested rating object
	
	Param
	
		{"comment": "Regular",
		"user_id": "test",
		"target_id": "Quesu",
		"value": "5"}
	
	Return
	
		Status code: 201
	
*	uri: `/ratings/<id>` method: `DELETE`, description: deletes the requested rating object
	
	Return
	
		Status code: 202

###Users###
	
*	uri: `/users` method: `GET`, description: returns a list of registered user id's

	Return
	
		[{"user_id": "test", "uri": "/users/test"},
		{"user_id": "tutorial", "uri": "/users/tutorial"}]

*	uri: `/users/<user_id>` method: `GET`, description: returns the requested user info and a list of user's ratings
	
	Return
	
		{"ratings": [{"id": "511fab02561193519fbc979b", "uri": "/ratings/511fab02561193519fbc979b"},
		{"id": "511fac1256119351ca606b75", "uri": "/ratings/511fac1256119351ca606b75"},
		{"id": "511fc82a5611935477798fa5", "uri": "/ratings/511fc82a5611935477798fa5"}],
		"user_id": "test"}

###Targets###
	
*	uri: `/targets` method: `GET`, description: returns a list of target id's

	Return
	
		[{"target_id": "Quesu", "uri": "/targets/Quesu"},
		{"target_id": "Casa Pepe", "uri": "/targets/Casa Pepe"}]
	
*	uri: `/targets/<target_id>` method: `GET`, description: returns the target object

	Return

		{"ratings":
		[{"id": "511fc3bc5611935477798f9f", "uri": "/ratings/511fc3bc5611935477798f9f"},		
		{"id": "511fc5a65611935477798fa4", "uri": "/ratings/511fc5a65611935477798fa4"}],
		"target_id": "Casa Pepe"}
	
#Install#

Nothing to do, only download.

##Requiremets##

###Server###

1.	python ;-) [Python downloads](http://www.python.org/download/)
2.	bottle [Bottle home](http://bottlepy.org/docs/dev/index.html). Lightweight WSGI micro web-framework for Python

		easy_install -U bottle
3.	mongoDB [MongoDB home](http://www.mongodb.org). Open source, Document-oriented NOSQL database.
	*	Homebrew (MacOS X)
	
			brew update
			brew install mongodb
4.	pymongo [PyMongo home](http://api.mongodb.org/python/current/). MongoDB library written in Python

		easy_install -U pymongo

###Client###

1.	python ;-) [Python downloads](http://www.python.org/download/)
2.	request [Request home](http://docs.python-requests.org/en/latest/index.html). Simple HTTP library


#Running#

*	Run MongoDB `mongod`
*	Run server `python saborear.py`
*	Run client `python saborear-client.py` and click `Enter` when paused.


#Testing#

Use your preferred REST client or install [Simple REST Client](https://chrome.google.com/extensions/detail/fhjcajmcbmldlhcimfajhfbgofnpcjmb).

##Rate a meal##

*	Open [`http://localhost:8080/ratings`](http://localhost:8080/ratings)
*	Select POST
*	Enter data: `{"user_id":"tutorial", "target_id":"Casa Pepe", "value":10, "comment":"Muy bueno"}`
*	Status 201 created? Good
*	Check Location in response header for created rating **URI**
	*	`Location: /ratings/511fab02561193519fbc979b` where `511fab02561193519fbc979b`is the created rating **id**

##Get all ratings##

*	Open [`http://localhost:8080/ratings`](http://localhost:8080/ratings)
*	Select GET
*	Status 200 OK? Good
*	Check Data fron response, there is a list of rating in JSON format. Each element has **id** and **URI**

##Get meal rating##

*	Open [`http://localhost:8080/{rating_URI}`](http://localhost:8080/ratings/511fab02561193519fbc979b)
*	Select GET
*	Status 200 OK? Good
*	Check Data fron response, there is a rating in JSON format.
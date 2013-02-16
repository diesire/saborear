#Introduction#

[saborear](https://github.com/diesire/saborear) is a simple rating REST web service example.

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
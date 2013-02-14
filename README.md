#Install#
1.	python
2.	bottle [Bottle home](http://bottlepy.org/docs/dev/index.html)

		easy_install -U bottle
3.	mongoDB [MongoDB home](http://www.mongodb.org)
	*	Homebrew (MacOS X)
	
			brew update
			brew install mongodb
4.	pymongo

		easy_install -U pymongo

#Running#

*	Run MongoDB `mongod`
*	Run server `python saborear.py`

#Testing#
Use your preferred REST client or install [Simple REST Client](https://chrome.google.com/extensions/detail/fhjcajmcbmldlhcimfajhfbgofnpcjmb).

##Rate a restaurant##

*	Open `http://localhost:8080/rating`
*	Select PUT
*	Enter data: `{"_id": "doc1", "name": "Test Document 1"}`

##Get restaurant rating##
*	Open `http://localhost:8080/rating/doc1`
*	Select GET
import json
import bottle
import logging
from bottle import *
from pymongo import Connection
from bson.objectid import ObjectId
from bson import json_util

#Logger config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger('saborear')
#logger.warning('Protocol problem: %s', 'connection reset', extra=d)

#Mongo config
_testing_collection = 'rating_testing'
_release_collection = 'rating'

connection = Connection('localhost', 27017)
db = connection.mydatabase
collection = db[_testing_collection]


# Ratings
@route('/ratings', method='GET')
def get_ratings():
    ratings = collection.find()
    json_docs = []
    for doc in ratings:
        _normalize_object(doc)
        json_docs.append({'id': doc['id'], 'URI': '/ratings/{}'.format(doc['id'])})
    json_docs = json.dumps(json_docs)
    logger.info('json_docs: %s', json_docs)
    response.set_header('Content-Type', 'application/json')
    return json_docs


@route('/ratings', method='POST')
def post_ratings():
    #{"user_id":"test", "target_id":"la cullar", "value":"2", "comment":"Malo, malo"}
    data = request.body.readline()
    logger.debug('data %s', data)
    if not data:
        logger.warning('Status 400 - No data received')
        abort(400, 'No data received')
    entity = json.loads(data)
    logger.debug('entity %s', entity)
    try:
        doc_id = collection.save(entity)
        response.set_header('Location', '/ratings/{}'.format(str(doc_id)))
        response.status = 201
        logger.debug('Rating {} inserted'.format(str(doc_id)))
    except ValidationError as ve:
        abort(400, str(ve))


@route('/ratings/<rating_id>', method='GET')
def get_rating(rating_id):
    
    entity = collection.find_one({'_id': ObjectId(rating_id)})
    #normalize
    entity["id"] = str(entity["_id"])
    del entity["_id"]
    response.set_header('Content-Type', 'application/json')
    if not entity:
        abort(404, 'No document with id %s' % rating_id)
    return json.dumps(entity)


#normalize nongodb _id
def _normalize_object(obj):
        "Normalize mongo object for json serialization"
        if isinstance(obj, dict):
            if "_id" in obj: 
                obj["id"] = str(obj["_id"])
                del obj["_id"]
        if isinstance(obj, list):
            for a in obj: 
                _normalize_object(a)

#Main
if __name__ == '__main__':        
    # To run the server, type-in $ python server.py
    bottle.debug(True) # display traceback 
    run(host='localhost', port=8080, reloader=True)
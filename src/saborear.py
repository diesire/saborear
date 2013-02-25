#-*- coding: utf-8 -*-

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

#Mongo config
_testing_collection = 'rating_testing'
_release_collection = 'rating'

connection = Connection('localhost', 27017)
db = connection.mydatabase
collection = db[_testing_collection]

#Root
@route('/', method='GET')
def index():
    "Devuelve una lista con las operaciones válidas"
    response.set_header('Content-Type', 'application/json')
    operations = [{'route_id':'ratings', 'uri':'/ratings', 'operations':['GET', 'POST']},
                 {'route_id':'users', 'uri':'/users', 'operations':['GET']},
                 {'route_id':'targets', 'uri':'/targets', 'operations':['GET']}]
    json_operations = json.dumps(operations)
    return json_operations

# Ratings
@route('/ratings', method='GET')
def get_ratings():
    "Devuelve una lista de valoraciones, de la forma {'id': '1234567890', 'uri': '/ratings/1234567890'}"
    ratings = collection.find()
    json_docs = []
    for doc in ratings:
        _normalize_object(doc)
        json_docs.append({'id': doc['id'], 'uri': '/ratings/{}'.format(doc['id'])})
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
    "Devuelve un objeto rating de la forma {'id':'1234567890', 'user_id':'test', 'target_id':'la cullar', 'value':'2', 'comment':'Malo, malo'}"
    entity = collection.find_one({'_id': ObjectId(rating_id)})
    #normalize
    entity["id"] = str(entity["_id"])
    del entity["_id"]
    response.set_header('Content-Type', 'application/json')
    if not entity:
        abort(404, 'No document with id %s' % rating_id)
    return json.dumps(entity)

@route('/ratings/<rating_id>', method='DELETE')
def delete_rating(rating_id):
    try:
        doc_id = collection.remove({'_id': ObjectId(rating_id)})
        response.status = 202
        logger.debug('Rating {} deleted'.format(str(rating_id)))
    except ValidationError as ve:
        abort(400, str(ve))

@route('/ratings/<rating_id>', method='PUT')
def modify_rating(rating_id):
    #{"user_id":"test", "target_id":"la cullar", "value":"2", "comment":"Malo, malo"}
    data = request.body.readline()
    logger.debug('data %s', data)
    if not data:
        logger.warning('Status 400 - No data received')
        abort(400, 'No data received')
    entity = json.loads(data)
    logger.debug('entity %s', entity)
    try:
        doc_id = collection.update({'_id': ObjectId(rating_id)}, entity)
        response.status = 202
        logger.debug('Rating {} modified'.format(str(rating_id)))
    except ValidationError as ve:
        abort(400, str(ve))

@route('/users', method='GET')
def get_users():
    ratings = collection.find()
    json_docs = []
    for doc in ratings:
        _normalize_object(doc)
        user = {'user_id': doc['user_id'], 'uri': '/users/{}'.format(doc['user_id'])}
        if user not in json_docs:
            json_docs.append(user)
    json_docs = json.dumps(json_docs)
    logger.info('json_docs: %s', json_docs)
    response.set_header('Content-Type', 'application/json')
    return json_docs

@route('/users/<user_id>', method='GET')
def get_user(user_id):
    ratings = collection.find({'user_id': user_id})
    if not ratings:
        abort(404, 'No document with id %s' % user_id)
    json_docs = []
    for doc in ratings:
        _normalize_object(doc)
        json_docs.append({'id': doc['id'], 'uri': '/ratings/{}'.format(doc['id'])})
    json_docs = json.dumps({ 'user_id': user_id, 'ratings':json_docs})
    logger.info('json_docs: %s', json_docs)
    response.set_header('Content-Type', 'application/json')
    return json_docs

@route('/targets', method='GET')
def get_targets():
    ratings = collection.find()
    json_docs = []
    for doc in ratings:
        _normalize_object(doc)
        target = {'target_id': doc['target_id'], 'uri': '/targets/{}'.format(doc['target_id'])}
        if target not in json_docs:
            json_docs.append(target)
    json_docs = json.dumps(json_docs)
    logger.info('json_docs: %s', json_docs)
    response.set_header('Content-Type', 'application/json')
    return json_docs

@route('/targets/<target_id>', method='GET')
def get_target(target_id):
    ratings = collection.find({'target_id': target_id})
    if not ratings:
        abort(404, 'No document with id %s' % target_id)
    json_docs = []
    for doc in ratings:
        _normalize_object(doc)
        json_docs.append({'id': doc['id'], 'uri': '/ratings/{}'.format(doc['id'])})
    json_docs = json.dumps({ 'target_id': target_id, 'ratings':json_docs})
    logger.info('json_docs: %s', json_docs)
    response.set_header('Content-Type', 'application/json')
    return json_docs

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

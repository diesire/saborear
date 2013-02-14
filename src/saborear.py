import json
import bottle
from bottle import run, route, request, template
from pymongo import Connection

#Mongo config
connection = Connection('localhost', 27017)
db = connection.mydatabase


@route('/rating', method='PUT')
def put_rating():
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    entity = json.loads(data)
    try:
        db['rating'].save(entity)
    except ValidationError as ve:
        abort(400, str(ve))

@route('/rating/:id', method='GET')
def get_rating(id):
    entity = db['rating'].find_one({'_id':id})
    if not entity:
        abort(404, 'No document with id %s' % id)
    return entity


#Main
if __name__ == '__main__':        
    # To run the server, type-in $ python server.py
    bottle.debug(True) # display traceback 
    run(host='localhost', port=8080, reloader=True)
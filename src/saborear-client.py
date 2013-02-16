import requests
import json

_base_url = "http://localhost:8080"

print '                          Cliente REST'
print '='*80
print ''
print ''
print 'http://localhost:8080/ratings - GET'
print '-'*80
raw_input()
ws_url = _base_url + '/ratings'
r = requests.get(ws_url)
r = r.json()
print json.dumps(r, sort_keys=True, indent=2)
raw_input()


print ''
print ''
print 'http://localhost:8080/ratings - POST'
print '-'*80
raw_input()
ws_url = _base_url + '/ratings'
data = json.dumps({"user_id":"tutorial", "target_id":"Casa Pepe", "value":10, "comment":"Muy bueno"})
r = requests.post(ws_url, data)
print 'Status:', r.status_code
assert r.status_code == 201
r_uri = r.headers['Location']
print 'Header - Location:', r_uri
raw_input()


print ''
print ''
print 'http://localhost:8080{} - GET'.format(r_uri)
print '-'*80
raw_input()
ws_url = _base_url + r_uri
r = requests.get(ws_url)
r = r.json()
print json.dumps(r, sort_keys=True, indent=2)
print ''
print ''

##data = json.dumps({'name':'test', 'description':'some test repo'}) 

'''
Created on Jan 25, 2013

@author: AKIN
'''

from bottle import get, post, delete, put, route, run, template, request

'''
This is the method that responds to Create command 
'''
@post('/api/types/<entityType>/entities')
def handleCreate(entityType):
    #TODO: This requires authentication
    #TODO: Edit response code: 201
    return template('<b>Create called for {{entityType}}</b>!', entityType=entityType)

@delete('/api/types/<entityType>/entities/<entityId>')
def handleDelete(entityType, entityId):
    #TODO: This requires authentication
    #TODO: Edit response code: 204
    return template('<b>Delete called for {{entityType}}:{{entityId}}</b>!', entityType=entityType, entityId=entityId)

@put('/api/types/<entityType>/entities/<entityId>')
def handleEdit(entityType, entityId):
    #TODO: This requires authentication
    #TODO: Edit response code: 200
    return template('<b>Edit called for {{entityType}}:{{entityId}}</b>!', entityType=entityType, entityId=entityId)

@get('/api/types/<entityType>/entities/<entityId>')
def handleGetSingleEntity(entityType, entityId):
    #TODO: Edit response code: 200
    #handle the query parameters
    detached=request.query.detached
    deleted=request.query.deleted
    if detached == "":
        print("Query Parameter detached is null")
    else:
        print("Detached:" + detached)
        
    if deleted == "":
        print("Query Parameter deleted is null")
    else:
        print("deleted:" + deleted)
        
    return template('<b>GetSingleEntity called for {{entityType}}:{{entityId}}</b>!', entityType=entityType, entityId=entityId)

@route('/hello/:name')
def index(name='World'):
    return template('<b>Hello {{name}}</b>!', name=name)

if __name__ == '__main__':
    print("akin")
    run(host='localhost', port=6060, debug=True)
    pass
'''
Created on Jan 25, 2013

@author: AKIN
'''

import json
import string

from bottle import get, post, delete, put, route, run, template, request
from warlock.core import model_factory

'''
This is the method that responds to Create command 
'''
@post('/api/types/<entityType>/entities')
def handleCreate(entityType):
    
    # check if the request is with content-type header
    tmpIndex = (request.headers.get('Content-Type')).find('application/json')
    if tmpIndex != -1:
        print("Content-Type header is correct!")
    else:
        # TODO Return a proper message!
        print("Return a proper message! " + request.headers.get('Content-Type'))
    
    # check if the request is with authentication header
    if request.headers.get('Authorization') != '':
        print("Authorization header is implemented!")
    else:
        # TODO Return a proper message!
        print("Return a proper message!")
        
    # check if the request is with authentication header
    if request.headers.get('Accept') == 'application/vnd.mediamanager.jbpm+json':
        print("WARNING! This is required for now.")
        print("Accept header is received!")
    else:
        # TODO Return a proper message!
        print("Return a proper message!")
    
    
    # get the request body
    jsonInputData = json.load(request.body)
    strInputData = json.dumps(jsonInputData)
    print("request = " + strInputData)
    newStr = string.replace(strInputData, 'false', 'False')
    newStr = string.replace(strInputData, 'true', 'True')
    print("New str = " + newStr)
    newJsonInput = json.dumps(newStr)
    newJsonInput = json.loads(newJsonInput)
    
    
    
    # we know the entity type so load the right schema
    
    # for now I am loading a simple one
    schema = {
      "name": "imageSubcontent",
      "type": "object",
      "javaType": "ImageSubcontent",
      "additionalProperties": False,
      "properties": {
        "xResolution": {
          "title": "xResolution",
          "type": "integer",
          "javaType": "XResolution",
          "additionalProperties": False
        },
        "yResolution": {
          "title": "yResolution",
          "type": "integer",
          "javaType": "YResolution",
          "additionalProperties": False
        },
        "language": {
          "title": "language",
          "type": "object",
          "javaType": "Locale",
          "properties": {
            "en_US": {
              "title": "en_US",
              "type": "string",
              "additionalProperties": False
            },
            "fr_FR": {
              "title": "fr_FR",
              "type": "string",
              "additionalProperties": False
            },
            "de_DE": {
              "title": "de_DE",
              "type": "string",
              "additionalProperties": False
            },
            "zh_CN": {
              "title": "zh_CN",
              "type": "string",
              "additionalProperties": False
            }
          },
          "additionalProperties": False
        },
        "_links": {
          "title": "Links",
          "type": "array",
          "items": [
            {
              "$ref": "#\/properties\/_link"
            }
          ],
          "additionalProperties": False
        }
      },
      "extends": {
        "$ref": "#\/properties\/subcontent"
      }
    }
    
    schema2 = {
        'name': 'Country',
        'properties': {
            'name': {'type': 'string'},
            'abbreviation': {'type': 'string'},
        },
        'additionalProperties': False,
    }
    
    imageSubcontent = model_factory(schema)
    
    imageSubcontent.xResolution = 10 
    imageSubcontent.yResolution = 15
    lang = {"en_US": "111", "fr_FR":"222", "de_DE":"3333", "zh_CN":"444" }
    imageSubcontent.language = lang
    print(imageSubcontent.language)
    
    sample = model_factory(schema2)
    
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
    run(host='localhost', port=6060, debug=True)
    
    pass
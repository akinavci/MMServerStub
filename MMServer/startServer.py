'''
Created on Jan 25, 2013

@author: AKIN
'''

import json
import string
import glob
import os
import pickle

from bottle import get, post, delete, put, route, run, template, request, response
from warlock.core import model_factory

listResponses = []
indexResponses = 0
maxIndexResponses = 0
responseFilesFolderUrl = ''

def prepare(testSuiteFileUrl, responseFolderUrl):
    # read the response file
    global listResponses
    global indexResponses
    global responseFilesFolderUrl
    global maxIndexResponses
    
    # set global variables
    indexResponses = 0
    responseFilesFolderUrl = responseFolderUrl
    
    if os.path.isfile(testSuiteFileUrl):
        listResponses = [line.strip() for line in open(testSuiteFileUrl)]
        maxIndexResponses = len(listResponses)
        return True
    else:
        # TODO: handle
        print('problem: no file')
        return False

'''
    This method reads the proper response file depending on the response code
    from the file, entity type, and the operation (create, read, update, etc.) 
'''
def readResponseFile(entityType, operationType):
    
    global listResponses
    global indexResponses
    global responseFilesFolderUrl
    global maxIndexResponses
    
    if indexResponses == maxIndexResponses:
        print('end of the file, should stop')
        return None
    else:
        pass
    
    # build the string for the filename
    strFilename = operationType + '_' + entityType + '_' + listResponses[indexResponses] + '.json'
    
    strFileUrl = responseFilesFolderUrl + '/' + strFilename
    
    fileContent = ''
    
    # read the file content
    if(os.path.isfile(strFileUrl)):
        # this is a file, read
        fileContent = json.load(open(strFileUrl))
        return fileContent
    else:
        # file does not exist, failed
        print('File does not exist, failed: ' + strFileUrl)  
        return None 
       
def checkContentType(request):
    # check if the request is with content-type header
    tmpIndex = (request.headers.get('Content-Type')).find('application/json')
    if tmpIndex != -1:
        print("Content-Type header is correct!")
        return True
    else:
        # TODO Return a proper message!
        print("Return a proper message! " + request.headers.get('Content-Type'))
        return False
    
def checkAuthorization(request):
    # check if the request is with authentication header
    if request.headers.get('Authorization') != '':
        print("Authorization header is implemented!")
        return True
    else:
        # TODO Return a proper message!
        print("Return a proper message!")
        return False  
    
def checkMm8Request(request):
    # check if the request is with authentication header
    if request.headers.get('Accept') == 'application/vnd.mediamanager.jbpm+json':
        print("WARNING! This is required for now.")
        print("Accept header is received!")
        return True
    else:
        # TODO Return a proper message!
        print("Return a proper message!")
        return False
          
     
'''
    This is the method that responds to Create command 
'''
@post('/api/types/<entityType>/entities')
def handleCreate(entityType):
        
    if checkAuthorization(request) and checkContentType(request) and checkMm8Request(request):
        # all required headers are provided
        pass
    else:
        # TODO: do something meaningful
        # headers are not complete, fail assertion
        pass
    
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
    
    # TODO: This requires authentication
    # TODO: Edit response code: 201
    return template('<b>Create called for {{entityType}}</b>!', entityType=entityType)

@delete('/api/types/<entityType>/entities/<entityId>')
def handleDelete(entityType, entityId):
    # TODO: This requires authentication
    # TODO: Edit response code: 204
    return template('<b>Delete called for {{entityType}}:{{entityId}}</b>!', entityType=entityType, entityId=entityId)

@put('/api/types/<entityType>/entities/<entityId>')
def handleEdit(entityType, entityId):
    # TODO: This requires authentication
    # TODO: Edit response code: 200
    return template('<b>Edit called for {{entityType}}:{{entityId}}</b>!', entityType=entityType, entityId=entityId)

@get('/api/types/<entityType>/entities/<entityId>')
def handleGetSingleEntity(entityType, entityId):
    global indexResponses
    global listResponses
    
    # TODO: Edit response code: 200
    # handle the query parameters
    detached = request.query.detached
    deleted = request.query.deleted
    if detached == "":
        print("Query Parameter detached is null")
    else:
        print("Detached:" + detached)
        
    if deleted == "":
        print("Query Parameter deleted is null")
    else:
        print("deleted:" + deleted)
    
    dictResponse = readResponseFile(entityType, 'readSingle')
    
    if dictResponse == None:
        # TODO: file not found
        pass
    
    dictResponseHeaders = dictResponse['headers']
    dictResponseBody = dictResponse['body'] 
    
    print(dictResponseHeaders)
    print(dictResponseBody)
    
    newJsonResponse = json.dumps(dictResponseBody)
    print(newJsonResponse)
    
    # set headers
    for key in dictResponseHeaders.keys():
        response.set_header(key, dictResponseHeaders[key])
    
    response.status = int(listResponses[indexResponses])
    
    # finally increase the index
    indexResponses += 1
    
#    newStrResponse = string.replace(strResponse, 'false', 'False')
#    newStrResponse = string.replace(strResponse, 'true', 'True')
#    print("New str = " + newStrResponse)
#    newJsonResponse = json.dumps(newStrResponse)
#    newJsonResponse = json.loads(newJsonResponse)
#    
#    print(newJsonResponse[0])
        
    return template('<b>GetSingleEntity called for {{entityType}}:{{entityId}}</b>!', entityType=entityType, entityId=entityId)
    

if __name__ == '__main__':
    
    if prepare('testSuite.txt', 'C:/Users/Administrator/Documents/GitHub/MMServerStub/MMServer/test'):
        print('ready to run the server')
    else:
        print('there is a problem, server will not start')
    
#    print(listResponses)
#    print(indexResponses)
#    print(responseFilesFolderUrl)
#    print(listResponses[indexResponses])
    
    run(host='localhost', port=6060, debug=True)
    
    pass

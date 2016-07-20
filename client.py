from requests.auth import HTTPBasicAuth

import requests
import os
import json

requests.packages.urllib3.disable_warnings()

class NotFoundError(Exception):
    def __init__(self, msg=""):
        Exception.__init__(self, msg)

class UnauthorizedError(Exception):
    def __init__(self, msg=""):
        Exception.__init__(self, msg)

class MalformedError(Exception):
    def __init__(self, msg=""):
        Exception.__init__(self, msg)

class InternalError(Exception):
    def __init__(self, msg=""):
        Exception.__init__(self, msg)

HTTP_ENDPOINT = os.environ.get("HTTP_ENDPOINT", "")
HTTP_USER = os.environ.get("HTTP_USER", "")
HTTP_PASS = os.environ.get("HTTP_PASS", "")

session = requests.Session()        

def send_req(method, path, body=None):
    url = "%s/%s" % (HTTP_ENDPOINT, path)
    resp = session.request(
        method, 
        url,
        json=body if body else "",
        auth=HTTPBasicAuth(HTTP_USER, HTTP_PASS),
        verify=False
    )

    if resp.status_code == 400:
        raise MalformedError(resp.text)
    elif resp.status_code == 404:
        raise NotFoundError(resp.text)
    elif resp.status_code == 401:
        raise UnauthorizedError(resp.text)
    elif resp.status_code >= 500:
        raise InternalError(resp.text)

    try:
        return resp.json()
    except Exception, e:
        return resp.text

class Function(object):
    def __init__(self):
        self.methods = ["execute"]
        self.definition = send_req("GET", "/function/")
    
    def __getattr__(self, func):
        self.name = str(func)
        if self.name in self.methods:
            return func
        elif self.name in self.definition:
            return self
        else:
            raise NotFoundError("Invalid function or method")
    
    def describe(self):
        print json.dumps(self.definition[self.name], indent=4, sort_keys=True)            

    def execute(self, **kwargs):
        args = "&".join(["%s=%s" % (arg, kwargs[arg]) for arg in kwargs])
        return send_req("GET", "/function/%s/%s" % (
            self.name, 
            ("?%s" % args) if len(args) > 0 else ""
        ))    

class Collection(object):
    def __init__(self):
        self.methods = ["all", "get", "delete", "save", "count"]
        self.definition = send_req("GET", "/collection/")
    
    def __getattr__(self, func):
        self.name = str(func)
        if self.name in self.methods:
            return func
        elif self.name in self.definition:
            return self
        else:
            raise NotFoundError("Invalid collection or method")

    def describe(self):
        print json.dumps(self.definition[self.name], indent=4, sort_keys=True)

    def get(self, pk):
        return send_req("GET", "/collection/%s/%s" % (self.name, pk))

    def filter(self, **kwargs):
        args = "&".join(["%s=%s" % (arg, kwargs[arg]) for arg in kwargs])
        return send_req("GET", "/collection/%s/%s" % (
            self.name, 
            ("?%s" % args) if len(args) > 0 else ""
        ))

    def count(self, **kwargs):
        args = "&".join(["%s=%s" % (arg, kwargs[arg]) for arg in kwargs])
        return send_req("GET", "/collection/%s/count/%s" % (
            self.name, 
            ("?%s" % args) if len(args) > 0 else ""
        ))["count"]

    def delete(self, pk):
        return send_req("DELETE", "/collection/%s/%s" % (self.name, pk))
        
    def insert(self, objs):
        return send_req("PUT", "/collection/%s/" % self.name, objs)

    def update(self, pk, obj):
        return send_req("POST", "/collection/%s/%s/" % (self.name, pk), obj)

collection = Collection()
function = Function()
__author__ = 'Richie Foreman <richie.foreman@gmail.com>'

import json
import httplib2

API_ROOT = "%s://api.4chan.org"
RESPONSE_TYPE = 'json'
FILE_ROOT = "%s://images.4chan.org/%s/src/%s%s"
SSL = False

# JSON Decoder, throw which ever decoder you like here. (e.g. SimpleJson, etc)
JSON_DECODER = json.loads

http = httplib2.Http()

class HttpException(Exception):
    pass

class Post(dict):
    def get_file_url(self):
        '''
            For a post, return the applicable file url
        '''
        try:
            return FILE_ROOT % (_get_transport(), self["board"], self["tim"], self["ext"])
        except KeyError:
            return None

def _get_transport():
    '''
        Depending upon settings, return the appropriate http transport
    '''
    if SSL:
        return "https"
    else:
        return "http"

def _get_api_root():
    '''
        Get the HTTPS/HTTP specific api root
    '''
    if SSL:
        return API_ROOT % _get_transport()
    else:
        return API_ROOT % _get_transport()

def get_thread(board, threadnumber):
    '''
        Given a board and thread number, yield a Post object

        Raises HttpException
    '''

    _uri = "%s/%s/res/%s.%s" % (_get_api_root(), board, threadnumber, RESPONSE_TYPE)

    headers, body = http.request(uri=_uri,
                                 method='GET')

    if headers["status"] == "200":
        for p in JSON_DECODER(body)["posts"]:
            post = Post()
            post.update(p)
            post["board"] = board
            yield post
    else:
        raise HttpException(int(headers["status"]))
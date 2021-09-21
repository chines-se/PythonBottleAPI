""" A Web server with a simple API using Bottle

    This server maintains a local data structure (a Python set) of widget names
    An agent connecting to this API server can use the following HTTP methods:
    GET    - retrieve a list of all widgets in the set
    POST   - add a new widget to the set
    PUT    - change the name of a widget
    DELETE - remove a widget from the set
"""

from bottle import run, default_app, static_file
from bottle import get, post, put, delete, response, request
import json, re
import sys

# TCP listening port for this server
PORT = 5000

# the widget "database" is emulated with a Python set data structure
WIDGET_MODELS = set()

# limit the widget names to alphanumeric characters with max length of 64
NAME_PATTERN = re.compile(r'^[a-zA-Z\d]{1,64}$')


@get('/<filepath:re:.*\.js>')
def get_js(filepath):
    """ Add a static route to find separate js files
    """
    return static_file(filepath, root='./')


@get('/')
def homepage_handler():
    """ Home page route handler...serve up client_browser.html (home page HTML)
    """
    response.headers['Cache-Control'] = 'no-cache'
    with open('client_browser_stub.html') as fp:
        s = fp.read()
        return s


@post('/widget_models')  
def creation_handler():
    """ Creates a new widget entry in the data set
        Use JSON Content-Type in this format: {'model': 'WIDGET_NAME'}  
        ...where "model" is the literal keyname and WIDGET_NAME is the user-supplied widget name
        POST http://HOSTNAME/widget_models        
    """
    try:
        # parse input data
        try: data = request.json
        except: raise ValueError

        if data is None: raise ValueError

        # extract and validate name
        try:
            if NAME_PATTERN.match(data['model']) is None:
                raise ValueError
            name = data['model']
        except (TypeError, KeyError): raise ValueError

        # check for existence
        if name in WIDGET_MODELS: raise KeyError

    except ValueError:
        # if bad request data, return 400 Bad Request
        response.status = 400
        return

    except KeyError:
        # if name already exists, return 409 Conflict
        response.status = 409
        return

    # add name
    WIDGET_MODELS.add(name)

    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'model': name})


@get('/widget_models')
def listing_handler():
    """ Returns a json list of widgets that exist in the set
        GET http://HOSTNAME/widget_models
    """
    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps({'widget_models': list(WIDGET_MODELS)})


@put('/widget_models/<oldname>')
def update_handler(oldname):
    """ Updates the name of an existing widget with a newly provided name
        PUT http://HOSTNAME/widget_models/EXISTING_WIDGET_NAME
    """
    try:
        # parse input data
        try: data = request.json
        except: raise ValueError

        # extract and validate new name
        try:
            if NAME_PATTERN.match(data['model']) is None: raise ValueError
            newname = data['model']
        except (TypeError, KeyError): raise ValueError

        # check if updated name exists
        if oldname not in WIDGET_MODELS: raise KeyError(404)

        # check if new name exists
        if newname in WIDGET_MODELS: raise KeyError(409)

    except ValueError:
        response.status = 400
        return
    except KeyError as e:
        response.status = e.args[0]
        return

    # remove old name and add new name
    WIDGET_MODELS.remove(oldname)
    WIDGET_MODELS.add(newname)

    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'model': newname})


@delete('/widget_models/<name>')
def delete_handler(name):
    """ Deletes an entry from the set
        DELETE http://HOSTNAME/widget_models/EXISTING_WIDGET_NAME
    """
    try:
        # Check if name exists
        if (name not in WIDGET_MODELS) and (name != 'all'): raise KeyError
    except KeyError:
        response.status = 404
        return

    # Remove name
    if name == 'all':
        WIDGET_MODELS.clear()
    else:
        WIDGET_MODELS.remove(name)
    return

if __name__ == '__main__':
    print('widget API server listening on port {}'.format(PORT))
    run(host='0.0.0.0', port=PORT, debug=True)

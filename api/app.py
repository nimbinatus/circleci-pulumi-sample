import json
import falcon

api = application = falcon.App()


# Home resource
class Home(object):
    def on_get(self, req, resp):
        payload = {
            "response": "OK"
        }
        resp.text = json.dumps(payload)
        resp.status = falcon.HTTP_200


# Greeting resource
class Greeting(object):
    def on_get(self, req, resp):
        if "name" in req.params:
            payload = {
                "response": f'hello, {req.params["name"]}'
            }
        else:
            payload = {
                "response": "hello, world!!"
            }
        resp.text = json.dumps(payload)
        resp.status = falcon.HTTP_200


# Instantiation
home = Home()
greeting = Greeting()

# Routes
api.add_route('/', home)
api.add_route('/hello', greeting)

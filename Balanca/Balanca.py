from flask import Flask, request
from flask_restful import Resource, Api
import random

app = Flask(__name__)
api = Api(app)

class Balanca(Resource):
    def get(self):
        ret = random.randint(20, 60)
        return {"peso": ret}

api.add_resource(Balanca, '/')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

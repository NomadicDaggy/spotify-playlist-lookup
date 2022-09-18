from flask_restful import Api
from app.resources.test import Test

api = Api(prefix="/api/v1")  # Note, no app

api.add_resource(Test, "/test", "/test/<string:id>")

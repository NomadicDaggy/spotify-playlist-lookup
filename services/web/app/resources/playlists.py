from flask_restful import Resource


class Playlists(Resource):
    def get(self, search_term):
        print(search_term)
        return {"task": 'Say "Hello, World!"'}

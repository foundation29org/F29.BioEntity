from flask import current_app, request, make_response, jsonify
from flask_restplus import Resource

from ._api import *

'''
    Disease Successors/Predecessors
'''
@API.route('/disease/successors/<string:ids>')
@API.param('ids', 'Disease IDs')
class disease_successors(Resource):
    def get(self, ids):
        ids = [id.strip() for id in ids.split(',')]
        depth = int(request.args.get('depth') or 1)
        bio = get_bio_phens('en')
        res = bio.Mondo.successors(ids, depth)
        return jsonify(res)
@API.route('/disease/successors')
class disease_post(Resource):
    def post(self):
        ids = json.loads(request.data)
        depth = int(request.args.get('depth') or 1)
        bio = get_bio_phens('en')
        res = bio.Mondo.predecessors(ids, depth)
        return jsonify(res)

@API.route('/disease/predecessors/<string:ids>')
@API.param('ids', 'Disease IDs')
class disease_predecessors(Resource):
    def get(self, ids):
        ids = [id.strip() for id in ids.split(',')]
        depth = int(request.args.get('depth') or 1)
        bio = get_bio_phens('en')
        res = bio.Mondo.predecessors(ids, depth)
        return jsonify(res)
@API.route('/disease/predecessors')
class disease_predecessors_post(Resource):
    def post(self):
        ids = json.loads(request.data)
        depth = int(request.args.get('depth') or 1)
        bio = get_bio_phens('en')
        res = bio.Mondo.predecessors(ids, depth)
        return jsonify(res)

'''
    Validation
'''
@API.route('/disease/validation/<string:ids>')
@API.param('ids', 'Disease IDs')
class disease_validation(Resource):
    def get(self, ids):
        ids = [id.strip() for id in ids.split(',')]
        bio = get_bio_phens('en')
        res = bio.Mondo.validate_terms(ids)
        return jsonify(res)
@API.route('/disease/validation')
class disease_validation_post(Resource):
    def post(self):
        ids = json.loads(request.data)
        bio = get_bio_phens('en')
        res = bio.Mondo.validate_terms(ids)
        return jsonify(res)

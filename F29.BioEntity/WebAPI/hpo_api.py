from flask import current_app, request, make_response, jsonify
from flask_restplus import Resource

from ._api import *

'''
    Phenotype Successors/Predecessors
'''
@API.route('/phenotype/successors/<string:ids>')
@API.param('ids', 'Phenotype IDs')
class phenotypes_successors(Resource):
    def get(self, ids):
        ids = [id.strip() for id in ids.split(',')]
        depth = int(request.args.get('depth') or 1)
        bio = get_bio_phens('en')
        res = bio.Phens.successors(ids, depth)
        return jsonify(res)
@API.route('/phenotype/successors')
class phenotypes_post(Resource):
    def post(self):
        ids = json.loads(request.data)
        depth = int(request.args.get('depth') or 1)
        bio = get_bio_phens('en')
        res = bio.Phens.successors(ids, depth)
        return jsonify(res)

@API.route('/phenotype/predecessors/<string:ids>')
@API.param('ids', 'Phenotype IDs')
class phenotypes_predecessors(Resource):
    def get(self, ids):
        ids = [id.strip() for id in ids.split(',')]
        depth = int(request.args.get('depth') or 1)
        bio = get_bio_phens('en')
        res = bio.Phens.predecessors(ids, depth)
        return jsonify(res)
@API.route('/phenotype/predecessors')
class phenotypes_predecessors_post(Resource):
    def post(self):
        ids = json.loads(request.data)
        depth = int(request.args.get('depth') or 1)
        bio = get_bio_phens('en')
        res = bio.Phens.predecessors(ids, depth)
        return jsonify(res)

'''
    Validation
'''
@API.route('/phenotype/validation/<string:ids>')
@API.param('ids', 'Phenotype IDs')
class phenotype_validation(Resource):
    def get(self, ids):
        ids = [id.strip() for id in ids.split(',')]
        bio = get_bio_phens('en')
        res = bio.Phens.validate_terms(ids)
        return jsonify(res)
@API.route('/phenotype/validation')
class phenotype_validation_post(Resource):
    def post(self):
        ids = json.loads(request.data)
        bio = get_bio_phens('en')
        res = bio.Phens.validate_terms(ids)
        return jsonify(res)

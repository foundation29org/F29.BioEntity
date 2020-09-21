from flask import current_app, request, make_response, jsonify
from flask_restplus import Resource

from ._api import *

'''
    Disease_Gene
'''
@API.route('/disease/gene/<string:ids>')
@API.param('ids', 'i.e: Orphanet:171629, OMIM:607208')
class disease_gene_get(Resource):
    def get(self, ids):
        ids = [id.strip() for id in ids.split(',')]
        res = bio_genes.get_genes(ids)
        return jsonify(res)
@API.route('/disease/gene')
class disease_gene_post(Resource):
    def post(self):
        ids = json.loads(request.data)
        res = bio_genes.get_genes(ids)
        return jsonify(res)

'''
    Gene_Disease
'''
@API.route('/gene/disease/<string:ids>')
@API.param('ids', 'i.e: SCN1A, HGNC:10589')
class gene_disease_get(Resource):
    def get(self, ids):
        ids = [id.strip() for id in ids.split(',')]
        res = bio_genes.get_diseases(ids)
        return jsonify(res)
@API.route('/gene/disease')
class gene_disease_post(Resource):
    def post(self):
        ids = json.loads(request.data)
        res = bio_genes.get_diseases(ids)
        return jsonify(res)

from flask import current_app, request, make_response, jsonify
from flask_restplus import Resource

from ._api import *

'''
    ALL
'''
@API.route('/diseases/<string:lan>/all')
class diseases_all(Resource):
    def get(self, lan):
        bio = get_bio_phens(lan)
        res = bio.all_conds()
        return jsonify(res)

@API.route('/phenotypes/<string:lan>/all')
class phenotypes_all(Resource):
    def get(self, lan):
        bio = get_bio_phens(lan)
        res = bio.all_phens()
        return jsonify(res)

'''
    Obsolete
'''
@API.route('/diseases/<string:lan>/obsolete')
class diseases_obsolete(Resource):
    def get(self, lan):
        bio = get_bio_phens(lan)
        res = bio.all_obsolete_conds()
        return jsonify(res)

@API.route('/phenotypes/<string:lan>/obsolete')
class phenotypes_obsolete(Resource):
    def get(self, lan):
        bio = get_bio_phens(lan)
        res = bio.all_obsolete_phens()
        return jsonify(res)

'''
    Diseases / Phenotypes
'''
@API.route('/diseases/<string:lan>/<string:ids>')
@API.param('ids', 'Disease IDs')
@API.doc(params={
    'depth': {'description': 'depth', 'in': 'query', 'default': 0},
    'include_obsolete': {'description': 'if True, include obsolete terms', 'in': 'query', 'type': 'bool', 'default': False}
    })
class describe_diseases(Resource):
    def get(self, ids, lan):
        ids = [id.strip() for id in ids.split(',')]
        depth = int(request.args.get('depth') or -1)
        include_obsolete = str(request.args.get('include_obsolete')).lower() == 'true'
        bio = get_bio_phens(lan)
        res = bio.describe_conds(ids, depth=depth, include_obsolete=include_obsolete)
        return jsonify(res)
@API.route('/diseases/<string:lan>')
@API.doc(params={
    'depth': {'description': 'depth', 'in': 'query', 'default': 0},
    'include_obsolete': {'description': 'if True, include obsolete terms', 'in': 'query', 'type': 'bool', 'default': False}
    })
class describe_diseases_post(Resource):
    def post(self, lan):
        ids = json.loads(request.data)
        depth = int(request.args.get('depth') or -1)
        include_obsolete = str(request.args.get('include_obsolete')).lower() == 'true'
        bio = get_bio_phens(lan)
        res = bio.describe_conds(ids, depth=depth, include_obsolete=include_obsolete)
        return jsonify(res)

@API.route('/phenotypes/<string:lan>/<string:ids>')
@API.param('ids', 'Phenotype IDs')
@API.doc(params={
    'depth': {'description': 'depth', 'in': 'query', 'default': 0},
    'include_obsolete': {'description': 'if True, include obsolete terms', 'in': 'query', 'type': 'bool', 'default': False}
    })
class describe_phenotypes(Resource):
    def get(self, ids, lan):
        ids = [id.strip() for id in ids.split(',')]
        depth = int(request.args.get('depth') or -1)
        include_obsolete = str(request.args.get('include_obsolete')).lower() == 'true'
        bio = get_bio_phens(lan)
        res = bio.describe_phens(ids, depth=depth, include_obsolete=include_obsolete)
        return jsonify(res)
@API.route('/phenotypes/<string:lan>')
@API.doc(params={
    'depth': {'description': 'depth', 'in': 'query', 'default': 0},
    'include_obsolete': {'description': 'if True, include obsolete terms', 'in': 'query', 'type': 'bool', 'default': False}
    })
class describe_phenotypes_post(Resource):
    def post(self, lan):
        ids = json.loads(request.data)
        depth = int(request.args.get('depth') or -1)
        include_obsolete = str(request.args.get('include_obsolete')).lower() == 'true'
        bio = get_bio_phens(lan)
        res = bio.describe_phens(ids, depth=depth, include_obsolete=include_obsolete)
        return jsonify(res)

'''
    Disease_Phenotypes
'''
@API.route('/disease/phenotypes/<string:lan>/tree/<string:ids>')
@API.param('ids', 'i.e: MONDO:0007299, OMIM:607208')
@API.doc(params={
    'depth': {'description': 'depth', 'in': 'query', 'default': 0},
    'obsolete_action': {'description': "strategy with obsolete terms: ('show', 'hide', 'replace')", 'in': 'query', 'type': 'bool', 'default': 'replace'}
    })
class disease_phenotypes_tree(Resource):
    def get(self, ids, lan):
        ids = [id.strip() for id in ids.split(',')]
        depth = int(request.args.get('depth') or -1)
        obsolete_action = request.args.get('depth') or 'replace'
        bio = get_bio_phens(lan)
        res = bio.conditions_phens_recursive(ids, depth=depth, obsolete_action=obsolete_action)
        return jsonify(res)
@API.route('/disease/phenotypes/<string:lan>/tree')
@API.doc(params={
    'depth': {'description': 'depth', 'in': 'query', 'default': 0},
    'obsolete_action': {'description': "strategy with obsolete terms: ('show', 'hide', 'replace')", 'in': 'query', 'type': 'bool', 'default': 'replace'}
    })
class disease_phenotypes_tree_post(Resource):
    def post(self, lan):
        ids = json.loads(request.data)
        depth = int(request.args.get('depth') or -1)
        obsolete_action = request.args.get('depth') or 'replace'
        bio = get_bio_phens(lan)
        res = bio.conditions_phens_recursive(ids, depth=depth, obsolete_action=obsolete_action)
        return jsonify(res)

@API.route('/disease/phenotypes/<string:lan>/graph/<string:ids>')
@API.param('ids', 'i.e: MONDO:0007299, OMIM:607208')
class disease_phenotypes_graph(Resource):
    def get(self, ids, lan):
        ids = [id.strip() for id in ids.split(',')]
        bio = get_bio_phens(lan)
        G = bio.conditions_phens_graph(ids)
        L = js.node_link_data(G)
        return jsonify(L)
@API.route('/disease/phenotypes/<string:lan>/graph')
class disease_phenotypes_graph_post(Resource):
    def post(self, lan):
        ids = json.loads(request.data)
        bio = get_bio_phens(lan)
        G = bio.conditions_phens_graph(ids)
        L = js.node_link_data(G)
        return jsonify(L)

'''
    Groups
'''
@API.route('/phenotype/groups/<string:lan>/all')
class groups(Resource):
    def get(self, lan):
        bio = get_bio_phens(lan)
        res = bio.describe_groups()
        return jsonify(res)

@API.route('/phenotype/groups/<string:lan>/<string:ids>')
@API.param('ids', 'Phenotype IDs')
class groups(Resource):
    def get(self, ids, lan):
        ids = [id.strip() for id in ids.split(',')]
        empty = request.args.get('includeEmpty') or 'false'
        empty = empty.lower() == 'true'
        bio = get_bio_phens(lan)
        res = bio.group_phens(ids, empty)
        return jsonify(res)
@API.route('/phenotype/groups/<string:lan>')
class groups_post(Resource):
    def post(self, lan):
        ids = json.loads(request.data)
        empty = request.args.get('includeEmpty') or 'false'
        empty = empty.lower() == 'true'
        bio = get_bio_phens(lan)
        res = bio.group_phens(ids, empty)
        return jsonify(res)

'''
    Phenotype Leaves
'''
@API.route('/phenotype/leaves')
class phenotype_leaves_post(Resource):
    def post(self):
        dic = json.loads(request.data)
        depth = int(request.args.get('depth') or -1)
        bio = get_bio_phens('en')
        lea = PhenLeaves(bio)
        res = lea.leaves(dic, depth)
        return jsonify(res)

'''
    Common Ancestor
'''
@API.route('/common_ancestor/<string:ids>')
@API.param('ids', 'i.e: HP:0000002, HP:0000003')
class common_ancestor(Resource):
    def get(self, ids):
        ids = [id.strip() for id in ids.split(',')]
        bio = get_bio_phens('en')
        G = bio.common_ancestor(ids)
        L = js.node_link_data(G)
        return jsonify(L)
@API.route('/common_ancestor')
class common_ancestor_post(Resource):
    def post(self):
        ids = json.loads(request.data)
        bio = get_bio_phens('en')
        G = bio.common_ancestor(ids)
        L = js.node_link_data(G)
        return jsonify(L)

import pickle
import networkx as nx

from pronto import Ontology

from ._helpers import *
from .onto_graph import OntoGraph

class MondoGraph(OntoGraph):
    def __init__(self, ontology=None, G=None, version=None):
        self.mapping = {}
        self.xrefs = {}
        super().__init__(ontology, G, version)

    def _preprocess(self, G, id, term):
        uid = id.upper()
        self.mapping[uid] = uid
        if not id in self.xrefs:
            self.xrefs[uid] = []
        for xref in term.xrefs:
            uxr = xref.id.upper()
            self.mapping[uxr] = uid
            self.xrefs[uid].append(uxr)
            if uxr.startswith('ORPHANET'):
                uxr = uxr.replace('ORPHANET', 'ORPHA')
                self.mapping[uxr] = uid
                self.xrefs[uid].append(uxr)
        self.xrefs[uid].sort()

    def _add_edge(self, G, id, term):
        if id.startswith('MONDO'):
            for sub in term.subclasses(1):
                if sub.id != term.id:
                    G.add_edge(term.id, sub.id)

    '''
        Validate Terms
    '''
    def validate_terms(self, ids):
        dic = {}
        ids = ensure_upper_list(ids)
        for id in ids:
            mid = self.alias(id)
            dic[id] = self.validate_term(mid)
        return dic

    '''
        Misc
    '''
    def __getitem__(self, id):
        id = self.alias(id)
        if id:
            return self.Graph.nodes.get(id)
        return None

    def alias(self, id):
        id = id.upper()
        return self.mapping.get(id, None)

    def aliases(self, ids):
        items = []
        for id in ids:
            id = self.alias(id)
            if id:
                items.append(id)
        return items

    '''
        Load / Save
    '''
    @staticmethod
    def load(path):
        with open(path, 'rb') as fp:
            meta = pickle.load(fp)
        gx = MondoGraph(G=meta['graph'], version=meta['version'])
        gx.mapping = meta['alias']
        gx.xrefs = meta['xrefs']
        return gx

    def save(self, path):
        meta = {'graph': self.Graph, 'alias': self.mapping, 'xrefs': self.xrefs, 'version': self.version}
        with open(path, 'wb') as fp:
            pickle.dump(meta, fp, protocol=pickle.HIGHEST_PROTOCOL)

import pickle
import networkx as nx

from ._helpers import capitalize_text
from .onto_graph import OntoGraph

class HPOGraph(OntoGraph):
    def __init__(self, ontology=None, G=None, version=None):
        super().__init__(ontology, G, version)

    def _get_attributes(self, G, id, term):
        attrs = super()._get_attributes(G, id, term)
        name = attrs['name']
        synonyms = attrs['synonyms']
        layperson = self._get_layperson(synonyms, name)
        first_attrs = {
                'id': attrs['id'],
                'name': name,
                'layperson': layperson
            }
        first_attrs.update(attrs)
        return first_attrs

    def _get_layperson(self, synonyms, name):
        if synonyms:
            for synonym in synonyms:
                if synonym['type'] == 'layperson':
                    if synonym['scope'] == 'EXACT':
                        return synonym['label'] or name
        return name

    '''
        Load / Save
    '''
    @staticmethod
    def load(path):
        with open(path, 'rb') as fp:
            meta = pickle.load(fp)
        gx = HPOGraph(G=meta['graph'], version=meta['version'])
        return gx

    def save(self, path):
        meta = {'graph': self.Graph, 'version': self.version}
        with open(path, 'wb') as fp:
            pickle.dump(meta, fp, protocol=pickle.HIGHEST_PROTOCOL)

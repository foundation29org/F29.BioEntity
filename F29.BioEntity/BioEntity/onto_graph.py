import networkx as nx

from networkx.algorithms.lowest_common_ancestors import tree_all_pairs_lowest_common_ancestor

from ._helpers import *

class OntoGraph():
    def __init__(self, ontology=None, G=None, version=None):
        self.Graph = G or self._load_graph(ontology)
        self.root = [nd for nd, d in self.Graph.in_degree() if d == 0][0]
        self.version = version or ontology.metadata.data_version

    def _load_graph(self, ontology):
        G = nx.DiGraph()
        for id in ontology:
            term = ontology[id]
            self._preprocess(G, id, term)
            attrs = self._get_attributes(G, id, term)
            G.add_node(id, **attrs)
        for id in ontology:
            term = ontology[id]
            self._add_edge(G, id, term)
        return G

    def _preprocess(self, G, id, term):
        pass

    def _get_attributes(self, G, id, term):
        attrs = {
                'id': term.id,
                'name': capitalize_text(term.name),
                'desc': capitalize_text(term.definition),
                'comment': capitalize_text(self._parse_comment(term)),
                'synonyms': self._parse_synonyms(term),
                'subsets': self._parse_subsets(term),
                'is_a': self._parse_is_a(term),
                'obsolete': term.obsolete
            }
        if attrs['obsolete']:
            attrs['replaced_by'] = self._get_replaced_by(term)
            attrs['consider'] = self._get_consider(term)
        return attrs

    def _get_replaced_by(self, term):
        try:
            items = [r.id for r in term.replaced_by]
        except :
            items = []
        items.sort()
        return items

    def _get_consider(self, term):
        try:
            items = [r.id for r in term.consider]
        except :
            items = []
        items.sort()
        return items

    def _add_edge(self, G, id, term):
        for sub in term.subclasses(1):
            if sub.id != term.id:
                G.add_edge(term.id, sub.id)

    def _parse_comment(self, term):
        return term.comment if term.comment else ''

    def _parse_synonyms(self, term):
        syms = []
        for sym in term.synonyms:
            item = {
                    'label': capitalize_text(sym.description),
                    'scope': sym.scope,
                    'type': sym.type.id if sym.type else None,
                    'xrefs': [xr.id for xr in sym.xrefs] if sym.xrefs else None
                }
            if item['xrefs']:
                item['xrefs'].sort()
            syms.append(item)
        syms.sort(key=lambda x: x['label'] + ' ' + x['scope'])
        return syms

    def _parse_subsets(self, term):
        subsets = []
        for subset in term.subsets:
            subsets.append(subset)
        subsets.sort()
        return subsets

    def _parse_is_a(self, term):
        is_a = []
        try:
            for item in term.superclasses(distance=1, with_self=False):
                is_a.append(item.id)
        except :
            pass
        is_a.sort()
        return is_a

    '''
        Obsolete Terms
    '''
    def obsolete_terms(self):
        dic = {}
        for id in self.Graph.nodes:
            attrs = self.Graph.nodes[id]
            if attrs['obsolete']:
                syms = self._flat_synonyms(attrs['synonyms'])
                item = { 'id': id, 'name': attrs['name'], 'desc': attrs['desc'], 'synonyms': syms }
                item['obsolete'] = True
                item['replaced_by'] = attrs['replaced_by']
                item['consider'] = attrs['consider']
                dic[id] = item
        items = list(dic.values())
        items.sort(key=lambda x: x['id'])
        return items

    def _flat_synonyms(self, syms):
        items = set()
        for sym in syms:
            items.add(sym['label'])
        items = list(items)
        items.sort()
        return items

    '''
        Validate Terms
    '''
    def validate_terms(self, ids):
        dic = {}
        ids = ensure_upper_list(ids)
        for id in ids:
            dic[id] = self.validate_term(id)
        return dic

    def validate_term(self, id):
        if self.exists(id):
            attrs = self.Graph.nodes[id]
            item = { 'id': id, 'obsolete': False }
            if attrs['obsolete']:
                item['obsolete'] = True
                item['replaced_by'] = attrs['replaced_by']
                item['consider'] = attrs['consider']
            return item
        return None

    '''
        Misc
    '''
    def __getitem__(self, id):
        id = id.upper()
        return self.Graph.nodes.get(id)

    def exists(self, id):
        return self.Graph.has_node(id)

    '''
        Successors
    '''
    def successors_plain(self, id, depth=1):
        hash = set()
        if depth == 0: return []
        if self.Graph.has_node(id):
            for item in self.Graph.successors(id):
                hash.add(item)
                for subitem in self.successors_plain(item, depth - 1):
                    hash.add(subitem)
        return list(hash)

    def successors(self, ids, depth=1):
        dic = {}
        ids = ensure_upper_list(ids)
        for id in ids:
            items = self._successors(id, depth)
            if not items is None:
                dic[id] = items
        return dic
    def _successors(self, id, depth):
        if self.Graph.has_node(id):
            if depth == 0: return {}
            dic = {}
            for item in self.Graph.successors(id):
                dic[item] = self._successors(item, depth - 1)
            return dic
        return None

    '''
        Predecessors
    '''
    def predecessors_plain(self, id, depth=1):
        hash = set()
        if depth == 0: return []
        if self.Graph.has_node(id):
            for item in self.Graph.predecessors(id):
                hash.add(item)
                for subitem in self.predecessors_plain(item, depth - 1):
                    hash.add(subitem)
        return list(hash)

    def predecessors(self, ids, depth=1):
        dic = {}
        ids = ensure_upper_list(ids)
        for id in ids:
            items = self._predecessors(id, depth)
            if items:
                dic[id] = items
        return dic
    def _predecessors(self, id, depth):
        if self.Graph.has_node(id):
            if depth == 0: return {}
            dic = {}
            if self.Graph.has_node(id):
                for item in self.Graph.predecessors(id):
                    dic[item] = self._predecessors(item, depth - 1)
            return dic
        return None

    '''
        Common Ancestor
    '''
    def common_ancestor(self, ids):
        ids = ensure_upper_list(ids)
        pairs = self.get_pairs(ids)
        commons = self._pairs_common_ancestor(pairs)
        if commons:
            return commons
        return None

    def _pairs_common_ancestor(self, pairs):
        hash = set()
        lcas = tree_all_pairs_lowest_common_ancestor(self.Graph, self.root, pairs)
        for lca in lcas:
            hash.add(lca[1])
        if self.root in hash:
            return [self.root]
        if len(hash) == 1:
            return list(hash)
        current = pairs
        pairs = self.get_pairs(list(hash))
        if str(current) == str(pairs):
            return None
        return self._pairs_common_ancestor(pairs)

    def get_pairs(self, items):
        pairs = []
        for n in range(len(items)):
            id1 = items[n]
            if self.Graph.has_node(id1):
                for m in range(n + 1, len(items)):
                    id2 = items[m]
                    if self.Graph.has_node(id2):
                        if id1 != id2:
                            pairs.append((id1, id2))
        return pairs

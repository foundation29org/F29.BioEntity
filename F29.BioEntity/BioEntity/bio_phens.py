import copy
import pickle
import pandas as pd
import networkx as nx

from pronto import Ontology

from ._helpers import *
from .mondo_graph import MondoGraph
from .hpo_graph import HPOGraph

class BioPhens():
    def __init__(self, *args, **kwargs):
        self.Mondo = args[0]
        self.Phens = args[1]
        if(len(args) > 2):
            self.Graph = args[2]
        else:
            self.Graph = self._load_graph(self.Mondo, self.Phens, kwargs['df_phens'], kwargs['df_annts'])
        self.groups = None

    '''
        Load
    '''
    def _load_graph(self, gfx_mondo, gfx_phens, df_phens, df_annts):
        G = nx.DiGraph()

        # Feed condition nodes and condition-hpo edges
        df_phens = df_phens.fillna('')
        groupby = df_phens.groupby('subject')
        for ido, rows in groupby:
            id = gfx_mondo.alias(ido)
            if id:
                attrs = gfx_mondo[id]
                attrs = copy.deepcopy(attrs)
                attrs['type'] = 'cond'
                G.add_node(id, **attrs)
                for row in rows[['object', 'relation', 'evidence']].values:
                    if row[0].startswith('HP:'):
                        G.add_edge(id, row[0], relation=row[1], evidence=row[2], source=[ido], aspect='P')

        # Add annotations
        df_annts = df_annts.fillna('')
        groupby = df_annts.groupby('DatabaseID')
        for ido, rows in groupby:
            id = gfx_mondo.alias(ido)
            if id:
                for row in rows[['HPO_ID', 'Onset', 'Frequency', 'Sex', 'Modifier', 'Aspect']].values:
                    if row[0].startswith('HP:'):
                        self._append_annts(G, ido, id, row[0], row[1], row[2], row[3], row[4], row[5])

        # Set hpo node attributes
        for node in G.nodes:
            if node.startswith('HP:'):
                attrs = gfx_phens[node]
                if attrs:
                    attrs['type'] = 'phen'
                    nx.set_node_attributes(G, {node: attrs})
        return G

    def _append_annts(self, G, ido, id, hpo, onset, frequency, sex, modifier, aspect):
        if not G.has_edge(id, hpo):
            G.add_edge(id, hpo, source=[])
        edge = G[id][hpo]
        edge['source'].append(ido)
        edge['aspect'] = 'P'
        if onset: edge['onset'] = onset
        if frequency: edge['frequency'] = frequency
        if sex: edge['sex'] = sex
        if modifier: edge['modifier'] = modifier
        if aspect: edge['aspect'] = aspect

    '''
        Properties
    '''
    @property
    def nodes(self):
        return self.Graph.nodes

    @property
    def edges(self):
        return self.Graph.edges

    '''
        All Conds/Phens
    '''
    def all_conds(self, parent='MONDO:0000001'):
        dic = {}
        conds = self.Mondo.successors(parent, -1)
        if parent in conds:
            for id in enum_dic(conds[parent]):
                attrs = self.Mondo.Graph.nodes[id]
                if not attrs['obsolete']:
                    syms = self._flat_synonyms(attrs['synonyms'])
                    item = { 'id': id, 'name': attrs['name'], 'desc': attrs['desc'], 'synonyms': syms, 'obsolete': attrs['obsolete'] }
                    dic[id] = item
        items = list(dic.values())
        items.sort(key=lambda x: x['id'])
        return items

    def all_phens(self, parent='HP:0000118'):
        dic = {}
        phens = self.Phens.successors(parent, -1)
        if parent in phens:
            for id in enum_dic(phens[parent]):
                attrs = self.Phens.Graph.nodes[id]
                if not attrs['obsolete']:
                    syms = self._flat_synonyms(attrs['synonyms'])
                    item = { 'id': id, 'name': attrs['name'], 'layperson': attrs['layperson'], 'desc': attrs['desc'], 'synonyms': syms, 'obsolete': attrs['obsolete'] }
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
        Obsolete Conds/Phens
    '''
    def all_obsolete_conds(self):
        return self.Mondo.obsolete_terms()

    def all_obsolete_phens(self):
        return self.Phens.obsolete_terms()

    '''
        Validate Conds/Phens
    '''
    def validate_conds(self, ids):
        return self.Mondo.validate_terms(ids)

    def validate_phens(self, ids):
        return self.Phens.validate_terms(ids)

    '''
        Successors / Predecessors
    '''
    def successors_conds(self, ids, depth=1):
        return self.Mondo.successors(ids, depth)

    def successors_phens(self, ids, depth=1):
        return self.Phens.successors(ids, depth)

    def predecessors_conds(self, ids, depth=1):
        return self.Mondo.predecessors(ids, depth)

    def predecessors_phens(self, ids, depth=1):
        return self.Phens.predecessors(ids, depth)

    '''
        Describe Conds / Phens
    '''
    def describe_conds(self, ids, depth=0, include_obsolete=False):
        ids = ensure_upper_list(ids)
        items = {}
        for id in ids:
            aid = self.Mondo.alias(id)
            if aid:
                item = self._describe_cond(aid, depth, include_obsolete=include_obsolete)
                if item:
                    items[id] = item
        return items
    def _describe_cond(self, id, depth, include_obsolete):
        node = self.Mondo[id]
        if node:
            attrs = copy.deepcopy(node)
            if include_obsolete or not attrs['obsolete']:
                attrs['xrefs'] = self.Mondo.xrefs[id]
                if depth != 0:
                    succs = list(self.Mondo.successors(id, 1)[id])
                    attrs['children'] = self.describe_conds(succs, depth - 1, include_obsolete=include_obsolete)
                return attrs
        return None

    def describe_phens(self, ids, depth=0, include_obsolete=False):
        ids = ensure_upper_list(ids)
        items = {}
        for id in ids:
            item = self._describe_phen(id, depth, include_obsolete=include_obsolete)
            if item:
                items[id] = item
        return items
    def _describe_phen(self, id, depth, include_obsolete):
        node = self.Phens[id]
        if node:
            attrs = copy.deepcopy(node)
            if include_obsolete or not attrs['obsolete']:
                if depth != 0:
                    succs = list(self.Phens.successors(id, 1)[id])
                    attrs['children'] = self.describe_phens(succs, depth - 1, include_obsolete=include_obsolete)
                return attrs
        return None

    '''
        Conditions Phens
    '''
    def conditions_phens_recursive(self, ids, depth=-1, obsolete_action='replace'):
        ids = ensure_upper_list(ids)
        conds = {}
        for id in ids:
            cond_phens = self._conditions_phens_recursive_one(id, depth, obsolete_action)
            if cond_phens:
                conds[id] = cond_phens
        return conds

    def _conditions_phens_recursive_one(self, cond, depth, obsolete_action):
        depth -= 1
        cond = self.Mondo.alias(cond)
        if cond:
            cond_phens = self.conditions_phens([cond], obsolete_action)
            if len(cond_phens) > 0:
                items = {}
                cond_phens = cond_phens[cond]
                cond_phens['id'] = cond
                if depth != -1:
                    children = self.Mondo.successors(cond, depth=1)
                    if len(children) > 0:
                        children = children[cond]
                        for child in children:
                            child_phens = self._conditions_phens_recursive_one(child, depth, obsolete_action)
                            if child_phens:
                                items[child] = child_phens
                        cond_phens['children'] = items
                return cond_phens
        return None

    def conditions_phens(self, ids, obsolete_action='replace'):
        conds = {}
        ids = ensure_upper_list(ids)
        G = self.conditions_phens_graph(ids)
        for id in G.nodes:
            node = G.nodes[id]
            if len(node) > 0:
                if node['type'] == 'cond':
                    attrs = copy.deepcopy(node)
                    phens = {}
                    cours = {}
                    inher = {}
                    modfr = {}
                    for edge in G[id]:
                        aspect = G[id][edge]['aspect']
                        if aspect == 'C':
                            cours[edge] = { **G.nodes[edge], **G[id][edge] }
                        elif aspect == 'I':
                            inher[edge] = { **G.nodes[edge], **G[id][edge] }
                        elif aspect == 'M':
                            modfr[edge] = { **G.nodes[edge], **G[id][edge] }
                        else:
                            phens[edge] = { **G.nodes[edge], **G[id][edge] }
                    attrs['phenotypes'] = self._apply_obsolete_action(phens, obsolete_action)
                    attrs['inheritance'] = self._apply_obsolete_action(inher, obsolete_action)
                    attrs['clinical_course'] = self._apply_obsolete_action(cours, obsolete_action)
                    attrs['clinical_modifier'] = self._apply_obsolete_action(modfr, obsolete_action)
                    attrs['xrefs'] = self.Mondo.xrefs[id]
                    attrs['children'] = []
                    conds[id] = attrs
        return conds

    def _apply_obsolete_action(self, hpos, action):
        dic = {}
        action = action.lower()
        for id in hpos:
            hpo = hpos[id]
            if hpo['obsolete']:
                if action=='hide':
                    continue
                if action == 'show':
                    dic[id] = hpo
                if action == 'replace':
                    for rid in hpo['replaced_by']:
                        rhpo = self.Phens[rid]
                        if rhpo:
                            dic[rid] = rhpo
                    for rid in hpo['consider']:
                        rhpo = self.Phens[rid]
                        if rhpo:
                            dic[rid] = rhpo
            else:
                dic[id] = hpo
        return dic

    '''
        Conditions Phens Graph
    '''
    def conditions_phens_graph(self, ids):
        ids = ensure_upper_list(ids)
        ids = self.Mondo.aliases(ids)
        edges = self.edges(ids)
        H = self.edge_subgraph(edges)
        return H

    '''
        Phen Groups
    '''
    def describe_groups(self):
        groups = {}
        phens = self.describe_phens('HP:0000118', 1)['HP:0000118']['children']
        for id in phens:
            phen = phens[id]
            groups[id] = copy.deepcopy(phen)
        return groups

    def group_phens(self, ids, include_empty=False):
        ids = ensure_upper_list(ids)
        groups = self._get_groups()
        for id in ids:
            for gp in self._group_phen(groups, id):
                item = {
                    'id': id,
                    'name': self.Phens[id]['name']
                }
                groups[gp]['items'][id] = item
        if not include_empty:
            groupx = {}
            for key in groups:
                if len(groups[key]['items']) > 0:
                    groupx[key] = groups[key]
            groups = groupx
        return groups

    def _get_groups(self):
        if not self.groups:
            dic = {}
            groups = self.describe_groups()
            for id in groups:
                group = groups[id]
                dic[id] = {
                    'name': group['name'],
                    'desc': group['desc'],
                    'items': {}
                }
            self.groups = dic
        return copy.deepcopy(self.groups)

    def _group_phen(self, groups, id):
        preds = self.Phens.predecessors(id, -1)
        if id in preds:
            preds = preds[id]
            for gp in groups:
                group = dic_contains(preds, gp)
                if group:
                    yield group

    '''
        Leaves
    '''
    def phen_leaves(self, dic_phens, depth=-1):
        dic = {}
        for key in dic_phens:
            dic[key] = self.clean_phens(dic_phens[key])
        res = {}
        for key in dic:
            lvs = self._leaves_one(dic[key], depth)
            res[key] = lvs
        return res

    def _leaves_one(self, nodes, depth=-1):
        preds = self.Phens.predecessors(nodes, depth)
        preds = list(self._flat_hierarchy(preds))
        return [p for p in nodes if p not in preds]

    def _flat_hierarchy(self, dic, include_root=False):
        for key in dic:
            if include_root:
                yield key
            for item in self._flat_hierarchy(dic[key], True):
                yield item

    '''
        Misc
    '''
    def node_subgraph(self, nodes):
        return nx.node_subgraph(self.Graph, nodes)

    def edge_subgraph(self, edges):
        return nx.edge_subgraph(self.Graph, edges)

    def common_ancestor(self, ids):
        return self.Phens.common_ancestor(ids)

    def clean_conds(self, ids):
        items = [id for id in ids if self.Mondo.exists(id)]
        items = list(dict.fromkeys(items))
        return items

    def clean_phens(self, ids):
        items = [id for id in ids if self.Phens.exists(id)]
        items = list(dict.fromkeys(items))
        return items

    '''
        Load / Save
    '''
    @staticmethod
    def load(fn):
        with open(fn, 'rb') as fp:
            meta = pickle.load(fp)
        return BioPhens(meta['mondo'], meta['phens'], meta['graph'])

    def save(self, fn):
        meta = { 'mondo': self.Mondo, 'phens': self.Phens, 'graph': self.Graph}
        with open(fn, 'wb') as fp:
            pickle.dump(meta, fp, protocol=pickle.HIGHEST_PROTOCOL)

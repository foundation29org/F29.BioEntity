import copy
import pandas as pd

from ._helpers import *

class BioGenes():
    def __init__(self, fn, mondo):
        df = pd.read_csv(fn, sep='\t')
        df = df.where(pd.notnull(df), None)
        self.Mondo = mondo
        self._load_genes(df)
        self._load_diseases(df)
        self._load_relations(df)
        self._load_evidences(df)

    def _load_genes(self, df):
        self.gene_ids = {}
        self.gene_labels = {}
        genes = df[['subject', 'subject_label']].drop_duplicates().values
        for id, label in genes:
            item = { 'id': id, 'label': label, 'diseases': {} }
            self.gene_ids[id] = item
            self.gene_labels[label] = item
        for row in df.iterrows():
            rec = row[1]
            id = rec['object']
            cond = self.Mondo[id]
            if cond:
                disease = {
                        'id': id,
                        'label': cond['name'],
                        'relation': rec['relation'],
                        'evidence': rec['evidence'],
                        'source': rec['source'],
                        'is_defined_by': rec['is_defined_by'],
                        'qualifier': rec['qualifier'],
                        'obsolete': cond['obsolete']
                    }
                if disease['obsolete']:
                    disease['replaced_by'] = cond['replaced_by']
                    disease['consider'] = cond['consider']
                self.gene_ids[rec['subject']]['diseases'][id] = disease

    def _load_diseases(self, df):
        self.diseases = {}
        diseases = df['object'].drop_duplicates().values
        for id in diseases:
            cond = self.Mondo[id]
            if cond:
                disease = { 'id': id, 'label': cond['name'], 'genes': {}, 'obsolete': cond['obsolete'] }
                if disease['obsolete']:
                    disease['replaced_by'] = cond['replaced_by']
                    disease['consider'] = cond['consider']
                self.diseases[id] = disease
        for row in df.iterrows():
            rec = row[1]
            gene = {
                    'id': rec['subject'],
                    'label': rec['subject_label'],
                    'relation': rec['relation'],
                    'evidence': rec['evidence'],
                    'source': rec['source'],
                    'is_defined_by': rec['is_defined_by'],
                    'qualifier': rec['qualifier']
                }
            self.diseases[rec['object']]['genes'][rec['subject']] = gene

    def _load_relations(self, df):
        self.relations = {}
        relations = df[['relation', 'relation_label']].drop_duplicates().values
        for id, label in relations:
            self.relations[id] = label

    def _load_evidences(self, df):
        self.evidences = {}
        evidences = df[['evidence', 'evidence_label']].drop_duplicates().values
        for id, label in evidences:
            if not '|' in id:
                self.evidences[id] = label

    '''
        Get Genes
    '''
    def get_genes(self, ids):
        dic = {}
        ids = ensure_upper_list(ids)
        for id in ids:
            mid = self.Mondo.alias(id)
            if mid:
                dic[id] = self.diseases.get(mid, None)
            else:
                dic[id] = None
        return dic

    '''
        Get Diseases
    '''
    def get_diseases(self, ids, obsolete_action='replace'):
        dic = {}
        ids = ensure_upper_list(ids)
        for id in ids:
            if id in self.gene_ids:
                gen_dis = copy.deepcopy(self.gene_ids[id])
                gen_dis['diseases'] = self._apply_obsolete_action(gen_dis['diseases'], obsolete_action)
                dic[id] = gen_dis
            elif id in self.gene_labels:
                gen_dis = copy.deepcopy(self.gene_labels[id])
                gen_dis['diseases'] = self._apply_obsolete_action(gen_dis['diseases'], obsolete_action)
                dic[id] = gen_dis
            else:
                dic[id] = None
        return dic

    def _apply_obsolete_action(self, conds, action):
        dic = {}
        action = action.lower()
        for id in conds:
            cond = conds[id]
            if cond['obsolete']:
                if action=='hide':
                    continue
                if action == 'show':
                    dic[id] = cond
                if action == 'replace':
                    for rid in cond['replaced_by']:
                        rcond = self.Mondo[rid]
                        if rcond:
                            dic[rid] = rcond
                    for rid in cond['consider']:
                        rcond = self.Mondo[rid]
                        if rcond:
                            dic[rid] = rcond
            else:
                dic[id] = cond
        return dic

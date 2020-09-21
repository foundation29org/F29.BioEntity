import os
import copy
import pandas as pd
import networkx as nx

from BioEntity import *

PATH_FILES = '_files'

USE_CACHE = True

bio_phens = load_bio_phens('en', use_cache=USE_CACHE)

gfx_mondo = bio_phens.Mondo
gfx_phens = bio_phens.Phens

'''
    Check disease_phenotype.all.tsv
'''
df_phens = pd.read_csv(os.path.join(PATH_FILES, 'disease_phenotype.all.tsv'), sep='\t')

conds = set()
hpos_unk = {}
hpos_obs = {}

groupby = df_phens.groupby('subject')
for id, rows in groupby:
    cond = gfx_mondo.alias(id)
    if cond:
        for hp in rows['object'].values:
            hpo = bio_phens.Phens[hp]
            if hpo:
                if hpo['obsolete']:
                    hpos_obs[hp] = (id, cond, len(rows['object'].values), hpo['replaced_by'], hpo['consider'])
            else:
                hpos_unk[hp] = (id, cond, len(rows['object'].values))
    else:
        conds.add(id)

print('Unknown Conditions')
for item in conds:
    print(item)
print()

print('Unknown HPOs')
for item in hpos_unk:
    print(item, *hpos_unk[item], sep='\t')
print()

print('Obsolete HPOs')
for item in hpos_obs:
    print(item, *hpos_obs[item], sep='\t')
print()

'''
    Check phenotype.hpoa
'''
df_annts = pd.read_csv(os.path.join(PATH_FILES, 'phenotype.hpoa'), sep='\t')

conds = set()
hpos_unk = {}
hpos_obs = {}

groupby = df_annts.groupby('DatabaseID')
for id, rows in groupby:
    cond = gfx_mondo.alias(id)
    if cond:
        for hp in rows['HPO_ID'].values:
            hpo = bio_phens.Phens[hp]
            if hpo:
                if hpo['obsolete']:
                    hpos_obs[hp] = (id, cond, len(rows['HPO_ID'].values), hpo['replaced_by'], hpo['consider'])
            else:
                hpos_unk[hp] = (id, cond, len(rows['HPO_ID'].values))
    else:
        conds.add(id)

print('Unknown Conditions')
for item in conds:
    print(item)
print()

print('Unknown HPOs')
for item in hpos_unk:
    print(item, *hpos_unk[item], sep='\t')
print()

print('Obsolete HPOs')
for item in hpos_obs:
    print(item, *hpos_obs[item], sep='\t')

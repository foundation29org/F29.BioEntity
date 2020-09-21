import os
import copy
import pandas as pd
import networkx as nx

from BioEntity import *

PATH_FILES = '_files'

USE_CACHE = True

def analyze_phens_dataframe(df, subject, object):
    conds = set()
    hpos_unk = {}
    hpos_obs = {}
    groupby = df.groupby(subject)
    for id, rows in groupby:
        cond = gfx_mondo.alias(id)
        if cond:
            for hp in rows[object].values:
                hpo = bio_phens.Phens[hp]
                if hpo:
                    if hpo['obsolete']:
                        hpos_obs[hp] = (id, cond, len(rows[object].values), hpo['replaced_by'], hpo['consider'])
                else:
                    hpos_unk[hp] = (id, cond, len(rows[object].values))
        else:
            conds.add(id)
    conds = list(conds)
    conds.sort()
    return conds, hpos_unk, hpos_obs

def analyze_genes_dataframe(df):
    conds_unk = {}
    conds_obs = {}
    groupby = df.groupby('object')
    for id, rows in groupby:
        cond = gfx_mondo[id]
        if cond:
            if cond['obsolete']:
                genes = [row for row in rows['subject']]
                conds_obs[id] = (cond['id'], len(rows['object'].values), cond['replaced_by'], cond['consider'], genes)
        else:
            conds_unk.add(id)
    return conds_unk, conds_obs

def fprint(fp, *args):
    print(*args, sep='\t')
    print(*args, sep='\t', file=fp)

def fprint_header(fp, header):
    fprint(fp, '-' * 64)
    fprint(fp, header)
    fprint(fp, '-' * 64)

def write_phens_analysis(fp, conds, hpos_unk, hpos_obs):
    fprint(fp, 'Unknown Conditions')
    for item in conds:
        fprint(fp, item)
    fprint(fp)

    fprint(fp, 'Unknown HPOs')
    for item in hpos_unk:
        fprint(fp, item, *hpos_unk[item])
    fprint(fp)

    fprint(fp, 'Obsolete HPOs')
    for item in hpos_obs:
        fprint(fp, item, *hpos_obs[item])
    fprint(fp)

def write_phens_analysis(fp, conds, hpos_unk, hpos_obs):
    fprint(fp, 'Unknown Conditions')
    for item in conds:
        fprint(fp, item)
    fprint(fp)

    fprint(fp, 'Unknown HPOs')
    for item in hpos_unk:
        fprint(fp, item, *hpos_unk[item])
    fprint(fp)

    fprint(fp, 'Obsolete HPOs')
    for item in hpos_obs:
        fprint(fp, item, *hpos_obs[item])
    fprint(fp)

def write_genes_analysis(fp, conds_unk, conds_obs):
    fprint(fp, 'Unknown Conditions')
    for item in conds_unk:
        fprint(fp, item, *conds_unk[item])
    fprint(fp)

    fprint(fp, 'Obsolete Conditions')
    for item in conds_obs:
        fprint(fp, item, *conds_obs[item])
    fprint(fp)

'''
    Main
'''
bio_phens = load_bio_phens('en', use_cache=USE_CACHE)

gfx_mondo = bio_phens.Mondo
gfx_phens = bio_phens.Phens

'''
    Analyze disease_phenotype.all.tsv
'''
df = pd.read_csv(os.path.join(PATH_FILES, 'disease_phenotype.all.tsv'), sep='\t')

conds, hpos_unk, hpos_obs = analyze_phens_dataframe(df, 'subject', 'object')
with open('obsolete_terms.txt', 'w', encoding='UTF-8') as fp:
    fprint_header(fp, 'disease_phenotype.all.tsv')
    write_phens_analysis(fp, conds, hpos_unk, hpos_obs)

'''
    Analyze phenotype.hpoa
'''
df = pd.read_csv(os.path.join(PATH_FILES, 'phenotype.hpoa'), sep='\t')

conds, hpos_unk, hpos_obs = analyze_phens_dataframe(df, 'DatabaseID', 'HPO_ID')
with open('obsolete_terms.txt', 'a', encoding='UTF-8') as fp:
    fprint_header(fp, 'phenotype.hpoa')
    write_phens_analysis(fp, conds, hpos_unk, hpos_obs)

'''
    Analyze gene_disease.9606.tsv
'''
df = pd.read_csv(os.path.join(PATH_FILES, 'gene_disease.9606.tsv'), sep='\t')

conds_unk, conds_obs = analyze_genes_dataframe(df)
with open('obsolete_terms.txt', 'a', encoding='UTF-8') as fp:
    fprint_header(fp, 'gene_disease.9606.tsv')
    write_genes_analysis(fp, conds_unk, conds_obs)

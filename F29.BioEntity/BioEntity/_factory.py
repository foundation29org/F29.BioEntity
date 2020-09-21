import os
import pandas as pd

from pronto import Ontology

from .bio_phens import BioPhens
from .bio_genes import BioGenes
from .hpo_graph import HPOGraph
from .mondo_graph import MondoGraph

PATH_FILES = '_files'
PATH_CACHE = '_cache'

def load_hpo_graph(lan='en', use_cache=True):
    fn_cache = os.path.join(PATH_CACHE, F'hp-{lan}.gfx')
    if use_cache:
        if os.path.isfile(fn_cache):
            return HPOGraph.load(fn_cache)
    fn_obo = os.path.join(PATH_FILES, F'hp-{lan}.obo')
    hpo = Ontology(fn_obo)
    gfx = HPOGraph(hpo)
    gfx.save(fn_cache)
    return gfx

def load_mondo_graph(lan='en', use_cache=True):
    fn_cache = os.path.join(PATH_CACHE, F'mondo-{lan}.gfx')
    if use_cache:
        if os.path.isfile(fn_cache):
            return MondoGraph.load(fn_cache)
    fn_obo = os.path.join(PATH_FILES, F'mondo-{lan}.obo')
    mondo = Ontology(fn_obo)
    gfx = MondoGraph(mondo)
    gfx.save(fn_cache)
    return gfx

def load_bio_phens(lan='en', use_cache=True):
    fn_cache = os.path.join(PATH_CACHE, F'biophens-{lan}.pkl')
    if use_cache:
        if os.path.isfile(fn_cache):
            return BioPhens.load(fn_cache)
    hpo_graph = load_hpo_graph(lan, use_cache)
    mondo_graph = load_mondo_graph(lan, use_cache)
    df_phens = pd.read_csv(os.path.join(PATH_FILES, 'disease_phenotype.all.tsv'), sep='\t')
    df_annts = pd.read_csv(os.path.join(PATH_FILES, 'phenotype.hpoa'), sep='\t')
    biophens = BioPhens(mondo_graph, hpo_graph, df_phens=df_phens, df_annts=df_annts)
    biophens.save(fn_cache)
    return biophens

def load_bio_genes(use_cache=True):
    fn_genes = os.path.join(PATH_FILES, 'gene_disease.9606.tsv')
    mondo_graph = load_mondo_graph('en', use_cache)
    return BioGenes(fn_genes, mondo_graph)


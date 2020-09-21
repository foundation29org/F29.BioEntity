from flask import current_app
from flask_restplus import Api

API = Api(title='BioEntity', description='Diseases, Phenotypes and Genes ontology tools.', default='BioEntity')

from BioEntity import load_bio_phens, load_bio_genes

USE_CACHE = True

bio_phens_en = load_bio_phens('en', use_cache=USE_CACHE)
bio_phens_es = load_bio_phens('es', use_cache=USE_CACHE)
bio_genes = load_bio_genes(use_cache=USE_CACHE)

def get_bio_phens(lan='en'):
    if lan.lower() == 'es': return bio_phens_es
    return bio_phens_en

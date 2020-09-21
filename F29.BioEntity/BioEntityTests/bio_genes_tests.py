import unittest

from ._common import *

FOLDER = 'bio_genes'

class BioGenesTests(unittest.TestCase):
    def __init__(self, use_cache=True):
        self.bio = load_bio_genes(use_cache)
        return super().__init__(methodName='runTest')

    def test_get_genes(self):
        items = self.bio.get_genes('')
        self.assertTrue(items == {})
        items = self.bio.get_genes('MONDO:9999999')
        self.assertTrue(items == {'MONDO:9999999': None})
        items = self.bio.get_genes(["orphanet:171629", "omim:607208", "mondo:0011794"])
        assert file_equal(FOLDER, items, F'GET-GENES.json')

    def test_get_genes_obsolete(self):
        items = self.bio.get_genes(["MONDO:0044716", "MONDO:0029146"])
        assert file_equal(FOLDER, items, F'GET-GENES-Obs.json')

    def test_get_diseases(self):
        items = self.bio.get_diseases('')
        self.assertTrue(items == {})
        items = self.bio.get_diseases('HGNC:9999999')
        self.assertTrue(items == {'HGNC:9999999': None})
        items = self.bio.get_diseases(["hgnc:21197", "fa2h"])
        assert file_equal(FOLDER, items, F'GET_DISEASES.json')

    def test_get_diseases_obsolete(self):
        items = self.bio.get_diseases(["HGNC:11825", "HGNC:1388"], obsolete_action='show')
        assert file_equal(FOLDER, items, F'GET_DISEASES-Obs-Show.json')
        items = self.bio.get_diseases(["HGNC:11825", "HGNC:1388"], obsolete_action='replace')
        assert file_equal(FOLDER, items, F'GET_DISEASES-Obs-Replace.json')
        items = self.bio.get_diseases(["HGNC:11825", "HGNC:1388"], obsolete_action='hide')
        assert file_equal(FOLDER, items, F'GET_DISEASES-Obs-Hide.json')

    def runTest(self):
        self.test_get_genes()
        self.test_get_genes_obsolete()
        self.test_get_diseases()
        self.test_get_diseases_obsolete()

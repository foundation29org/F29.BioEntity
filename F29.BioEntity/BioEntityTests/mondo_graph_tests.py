import unittest

from ._common import *

FOLDER = 'mondo_graph'

class MondoGraphTests(unittest.TestCase):
    def __init__(self, lan, use_cache=True):
        self.lan = lan
        self.mondo_graph = load_mondo_graph(lan, use_cache)
        print('MONDO version: ', self.mondo_graph.version)
        super().__init__(methodName='runTest')

    def test_getitem(self):
        # Empty
        item = self.mondo_graph['']
        assert item == None

        # Unknown
        item = self.mondo_graph['MONDO:9999999']
        assert item == None
        item = self.mondo_graph['AB:9999']
        assert item == None

        # Lower case
        item1 = self.mondo_graph['MONDO:0011794']
        item2 = self.mondo_graph['mondo:0011794']
        assert item1 == item2

        # Check content
        item = self.mondo_graph['MONDO:0011794']
        assert file_equal(FOLDER, item, F'MONDO_0011794-{self.lan}.json')

    def test_obsolete(self):
        # Check obsolete1
        item = self.mondo_graph['MONDO:0000055']
        assert file_equal(FOLDER, item, F'MONDO_Obs1_0000055-{self.lan}.json')

        # Check obsolete2
        item = self.mondo_graph['MONDO:0007714']
        assert file_equal(FOLDER, item, F'MONDO_Obs2_0007714-{self.lan}.json')

        # Check obsolete3
        item = self.mondo_graph['MONDO:0007731']
        assert file_equal(FOLDER, item, F'MONDO_Obs3_0007731-{self.lan}.json')

    def test_successors(self):
        # Empty
        result = self.mondo_graph.successors('')
        assert result == {}
        result = self.mondo_graph.successors(['', ''], depth=3)
        assert result == {}

        # Unknown
        result = self.mondo_graph.successors('MONDO:9999999', depth=-1)
        assert result == {}
        result = self.mondo_graph.successors(['', 'MONDO:9999999', 'AB:9999'])
        assert result == {}

        # Lower case
        result1 = self.mondo_graph.successors('mondo:0011794')
        result2 = self.mondo_graph.successors('MONDO:0011794')
        assert result1 == result2

        # Unique values
        result1 = self.mondo_graph.successors(['mondo:0018097', 'MONDO:0011794'])
        result2 = self.mondo_graph.successors(['MONDO:0011794', 'MONDO:0018097', 'mondo:0011794'])
        assert result1 == result2

        # Check content
        result = self.mondo_graph.successors(['MONDO:0011794', 'MONDO:0018097'], 2)
        assert file_equal(FOLDER, result, F'MONDO-Successors-{self.lan}.json')

    # Check all succesors are not obsolete
    def test_successors_obsolete(self):
        result = self.mondo_graph.successors(self.mondo_graph.root, -1)
        def check_obsolete(dic):
            for id in dic:
                item = self.mondo_graph[id]
                assert item['obsolete'] == False
                check_obsolete(dic[id])
        check_obsolete(result)

    def test_predecessors(self):
        # Empty
        result = self.mondo_graph.predecessors('')
        assert result == {}
        result = self.mondo_graph.predecessors(['', ''], depth=3)
        assert result == {}

        # Unknown
        result = self.mondo_graph.predecessors('MONDO:9999999', depth=-1)
        assert result == {}
        result = self.mondo_graph.predecessors(['', 'MONDO:9999999', 'AB:9999'])
        assert result == {}

        # Lower case
        result1 = self.mondo_graph.predecessors('mondo:0011794')
        result2 = self.mondo_graph.predecessors('MONDO:0011794')
        assert result1 == result2

        # Unique values
        result1 = self.mondo_graph.predecessors(['mondo:0018097', 'MONDO:0011794'])
        result2 = self.mondo_graph.predecessors(['MONDO:0011794', 'MONDO:0018097', 'mondo:0011794'])
        assert result1 == result2

        # Check content
        result = self.mondo_graph.predecessors(['MONDO:0011794', 'MONDO:0018097'], 2)
        assert file_equal(FOLDER, result, F'MONDO-Predecessors-{self.lan}.json')

    def test_obsolete_terms(self):
        result = self.mondo_graph.obsolete_terms()
        #print(len(result))
        assert file_equal(FOLDER, result, F'MONDO-Obsoletes-{self.lan}.json')

    def test_validate_terms(self):
        # Empty
        result = self.mondo_graph.validate_terms('')
        assert result == {}

        # Unknown
        result = self.mondo_graph.validate_terms('MONDO:9999999')
        assert result == {'MONDO:9999999': None}

        # Aliases
        result1 = self.mondo_graph.validate_terms(['mondo:0011794', 'MONDO:0011794', 'OMIM:607208', 'orphanet:33069'])
        result2 = self.mondo_graph.validate_terms('MONDO:0011794')
        assert result1['MONDO:0011794'] == result2['MONDO:0011794']
        assert result1.get('mondo:0011794') is None
        assert result1['OMIM:607208'] == result2['MONDO:0011794']
        assert result1['ORPHANET:33069'] == result2['MONDO:0011794']

        # Check content
        result = self.mondo_graph.validate_terms(['', 'XYZ:9999999', 'MONDO:0011794', 'MONDO:0000002', 'MONDO:0000038', 'MONDO:0000002'])
        assert file_equal(FOLDER, result, F'MONDO-Validate-{self.lan}.json')


    def runTest(self):
        self.test_getitem()
        self.test_obsolete()
        self.test_successors()
        self.test_successors_obsolete()
        self.test_predecessors()
        self.test_obsolete_terms()
        self.test_validate_terms()

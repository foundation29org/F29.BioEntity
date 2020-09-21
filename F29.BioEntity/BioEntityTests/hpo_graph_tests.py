import unittest

from ._common import *

FOLDER = 'hpo_graph'

class HPOGraphTests(unittest.TestCase):
    def __init__(self, lan, use_cache=True):
        self.lan = lan
        self.hpo_graph = load_hpo_graph(lan, use_cache)
        print('HPO version: ', self.hpo_graph.version)
        super().__init__(methodName='runTest')

    def test_getitem(self):
        # Empty
        item = self.hpo_graph['']
        assert item == None

        # Unknown
        item = self.hpo_graph['HP:9999999']
        assert item == None
        item = self.hpo_graph['AB:9999']
        assert item == None

        # Lower case
        item1 = self.hpo_graph['hp:0001250']
        item2 = self.hpo_graph['HP:0001250']
        assert item1 == item2

        # Check content
        item = self.hpo_graph['HP:0001250']
        assert file_equal(FOLDER, item, F'HP_0001250-{self.lan}.json')

    def test_obsolete(self):
        # Check obsolete1
        item = self.hpo_graph['HP:0000284']
        assert file_equal(FOLDER, item, F'HP_Obs1_0000284-{self.lan}.json')

        # Check obsolete2
        item = self.hpo_graph['HP:0000489']
        assert file_equal(FOLDER, item, F'HP_Obs2_0000489-{self.lan}.json')

    def test_successors(self):
        # Empty
        result = self.hpo_graph.successors('')
        assert result == {}
        result = self.hpo_graph.successors(['', ''], depth=3)
        assert result == {}

        # Unknown
        result = self.hpo_graph.successors('HP:9999999', depth=-1)
        assert result == {}
        result = self.hpo_graph.successors(['', 'HP:9999999', 'AB:9999'])
        assert result == {}

        # Lower case
        result1 = self.hpo_graph.successors('hp:0001250')
        result2 = self.hpo_graph.successors('HP:0001250')
        assert result1 == result2

        # Unique values
        result1 = self.hpo_graph.successors(['hp:0001250', 'HP:0001945'])
        result2 = self.hpo_graph.successors(['HP:0001945', 'HP:0001250', 'HP:0001945'])
        assert result1 == result2

        # Check content
        result = self.hpo_graph.successors(['HP:0001250', 'HP:0001945'], 2)
        assert file_equal(FOLDER, result, F'HPO-Successors-{self.lan}.json')

    # Check all succesors are not obsolete
    def test_successors_obsolete(self):
        result = self.hpo_graph.successors(self.hpo_graph.root, -1)
        def check_obsolete(dic):
            for id in dic:
                item = self.hpo_graph[id]
                assert item['obsolete'] == False
                check_obsolete(dic[id])
        check_obsolete(result)

    def test_predecessors(self):
        # Empty
        result = self.hpo_graph.predecessors('')
        assert result == {}
        result = self.hpo_graph.predecessors(['', ''], depth=3)
        assert result == {}

        # Unknown
        result = self.hpo_graph.predecessors('HP:9999999', depth=-1)
        assert result == {}
        result = self.hpo_graph.predecessors(['', 'HP:9999999', 'AB:9999'])
        assert result == {}

        # Lower case
        result1 = self.hpo_graph.predecessors('hp:0001250')
        result2 = self.hpo_graph.predecessors('HP:0001250')
        assert result1 == result2

        # Unique values
        result1 = self.hpo_graph.predecessors(['hp:0001250', 'HP:0001945'])
        result2 = self.hpo_graph.predecessors(['HP:0001945', 'HP:0001250', 'HP:0001945'])
        assert result1 == result2

        # Check content
        result = self.hpo_graph.predecessors(['HP:0001250', 'HP:0001945'], 2)
        assert file_equal(FOLDER, result, F'HPO-Predecessors-{self.lan}.json')

    def test_obsolete_terms(self):
        result = self.hpo_graph.obsolete_terms()
        #print(len(result))
        assert file_equal(FOLDER, result, F'HPO-Obsoletes-{self.lan}.json')

    def test_validate_terms(self):
        # Empty
        result = self.hpo_graph.validate_terms('')
        assert result == {}

        # Unknown
        result = self.hpo_graph.validate_terms('HP:9999999')
        assert result == {'HP:9999999': None}

        # Aliases
        result1 = self.hpo_graph.validate_terms(['hp:0001250', 'HP:0001250'])
        result2 = self.hpo_graph.validate_terms('HP:0001250')
        assert result1['HP:0001250'] == result2['HP:0001250']
        assert result1.get('hp:0001250') is None

        # Check content
        result = self.hpo_graph.validate_terms(['', 'XYZ:9999999', 'HP:0001945', 'HP:0000057', 'HP:0003340', 'HP:0000057'])
        assert file_equal(FOLDER, result, F'HPO-Validate-{self.lan}.json')

    def runTest(self):
        self.test_getitem()
        self.test_obsolete()
        self.test_successors()
        self.test_successors_obsolete()
        self.test_predecessors()
        self.test_obsolete_terms()
        self.test_validate_terms()

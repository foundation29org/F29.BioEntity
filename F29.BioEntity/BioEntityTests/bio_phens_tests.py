import unittest

from ._common import *

FOLDER = 'bio_phens'

class BioPhensTests(unittest.TestCase):
    def __init__(self, lan, use_cache=True):
        self.lan = lan
        self.bio = load_bio_phens(lan, use_cache)
        super().__init__(methodName='runTest')

    '''
        Test All Conds/Phens
    '''
    def test_all_conds(self):
        all = self.bio.all_conds()
        assert not all is None
        found = None
        for item in all:
            if item['id'] == 'MONDO:0011794':
                found = item
                break
        assert not found is None
        assert file_equal(FOLDER, found, F'ALL-MONDO_0011794-{self.lan}.json')
        assert file_equal(FOLDER, all, F'ALL-MONDO-{self.lan}.json')

    def test_all_phens(self):
        all = self.bio.all_phens()
        assert not all is None
        found = None
        for item in all:
            if item['id'] == 'HP:0001250':
                found = item
                break
        assert not found is None
        assert file_equal(FOLDER, found, F'ALL-HP_0001250-{self.lan}.json')
        assert file_equal(FOLDER, all, F'ALL-HP-{self.lan}.json')

    '''
        Desc Conds
    '''
    def test_desc_conds(self):
        item = self.bio.describe_conds('')
        assert item == {}
        item = self.bio.describe_conds('MONDO:9999999')
        assert item == {}
        item = self.bio.describe_conds('MONDO:0019349', 2)
        assert not item is None
        assert file_equal(FOLDER, item, F'DESC-MONDO_0019349-{self.lan}.json')
        items = self.bio.describe_conds(['MONDO:0019349', 'MONDO:9999999'], 2)
        assert item == items
        items = self.bio.describe_conds(['MONDO:0019349', 'MONDO:0019349'], 2)
        assert item == items
        items = self.bio.describe_conds(['MONDO:0019349', 'MONDO:0011794'])
        assert len(list(items)) == 2

    def test_desc_conds_obsolete(self):
        item = self.bio.describe_conds('MONDO:0007659', 2, include_obsolete=False)
        assert item == {}
        item = self.bio.describe_conds('MONDO:0007659', 2, include_obsolete=True)
        assert not item is None
        assert file_equal(FOLDER, item, F'DESC-Obs-MONDO_0007659-{self.lan}.json')

    '''
        Desc Phens
    '''
    def test_desc_phens(self):
        item = self.bio.describe_phens('')
        assert item == {}
        item = self.bio.describe_phens('HP:9999999')
        assert item == {}
        item = self.bio.describe_phens('HP:0000010', 2)
        assert not item is None
        assert file_equal(FOLDER, item, F'DESC-HP_0000010-{self.lan}.json')
        items = self.bio.describe_phens(['HP:0000010', 'HP:9999999'], 2)
        assert item == items
        items = self.bio.describe_phens(['HP:0000010', 'HP:0000010'], 2)
        assert item == items
        items = self.bio.describe_phens(['HP:0000010', 'HP:0000008'])
        assert len(list(items)) == 2

    def test_desc_phens_obsolete(self):
        item = self.bio.describe_phens('HP:0007901', 2, include_obsolete=False)
        assert item == {}
        item = self.bio.describe_phens('HP:0007901', 2, include_obsolete=True)
        assert not item is None
        assert file_equal(FOLDER, item, F'DESC-Obs-HP_0007901-{self.lan}.json')

    '''
        Condition -> Phens
    '''
    def test_cond_phens(self):
        item = self.bio.conditions_phens('')
        assert item == {}
        item = self.bio.conditions_phens('MONDO:9999999')
        assert item == {}
        item = self.bio.conditions_phens(['MONDO:0018097', 'MONDO:0007299', 'MONDO:9999999'])
        assert not item is None
        assert file_equal(FOLDER, item, F'COND-PHENS-{self.lan}.json')

    def test_cond_phens_recursive(self):
        item = self.bio.conditions_phens_recursive('')
        assert item == {}
        item = self.bio.conditions_phens_recursive('MONDO:9999999')
        assert item == {}
        item = self.bio.conditions_phens_recursive(['MONDO:0018097', 'MONDO:0007299', 'MONDO:9999999'], 3)
        assert not item is None
        assert file_equal(FOLDER, item, F'COND-PHENS-REC-{self.lan}.json')

    def test_cond_phens_obsolete_show(self):
        item = self.bio.conditions_phens(['MONDO:0054577', 'MONDO:0020607'], obsolete_action='show')
        assert not item is None
        assert file_equal(FOLDER, item, F'COND-PHENS-Obs-Show-{self.lan}.json')

    def test_cond_phens_obsolete_replace(self):
        item = self.bio.conditions_phens(['MONDO:0054577', 'MONDO:0020607'], obsolete_action='replace')
        assert not item is None
        assert file_equal(FOLDER, item, F'COND-PHENS-Obs-Replace-{self.lan}.json')

    def test_cond_phens_obsolete_hide(self):
        item = self.bio.conditions_phens(['MONDO:0054577', 'MONDO:0020607'], obsolete_action='hide')
        assert not item is None
        assert file_equal(FOLDER, item, F'COND-PHENS-Obs-Hide-{self.lan}.json')

    '''
        Groups
    '''
    def test_describe_groups(self):
        items = self.bio.describe_groups()
        assert not items is None
        assert file_equal(FOLDER, items, F'GROUPS-{self.lan}.json')

    def test_group_phens(self):
        result = self.bio.group_phens('')
        assert result == {}
        result = self.bio.group_phens('HP:9999999')
        assert result == {}
        result = self.bio.group_phens(['', 'HP:9999999'])
        assert result == {}
        result = self.bio.group_phens(['HP:0000223'])
        assert result != {}
        result2 = self.bio.group_phens(['HP:0000223', 'HP:9999999', ''])
        assert result2 == result
        result = self.bio.group_phens(['HP:0000223', 'HP:0000008', 'HP:0000223', 'HP:0000010'])
        assert result != {}
        assert file_equal(FOLDER, result, F'GROUPED-{self.lan}.json')

    '''
        Common Ancestor
    '''
    def test_common_ancestor(self):
        result = self.bio.common_ancestor('')
        assert result is None
        result = self.bio.common_ancestor('HP:9999999')
        assert result is None
        result = self.bio.common_ancestor('HP:0000010')
        assert result is None
        result = self.bio.common_ancestor(['HP:0000008', 'HP:0000010'])
        assert result[0] == 'HP:0000119'
        result = self.bio.common_ancestor(['HP:9999999', 'HP:0000010', 'HP:0000008', 'HP:0000010', ''])
        assert result[0] == 'HP:0000119'

    '''
        Phen Leaves
    '''
    def test_phen_leaves(self):
        result = self.bio.phen_leaves('')
        assert result == {}
        result = self.bio.phen_leaves({ 'sample': '' })
        assert result == { 'sample': [] }
        result = self.bio.phen_leaves({ 'sample': ['HP:0000008', 'HP:0000010', 'HP:0000008'] })
        assert result == { 'sample': ['HP:0000008', 'HP:0000010'] }
        result = self.bio.phen_leaves({
            'sample1': ['HP:0000008', 'HP:0000010', 'HP:0000130'],
            'sample2': ['HP:0000008', 'HP:0000010', 'HP:0000008'],
            'sample3': ['HP:9999999', '', 'HP:0000008']
        })
        assert result == {
            'sample1': ['HP:0000010', 'HP:0000130'],
            'sample2': ['HP:0000008', 'HP:0000010'],
            'sample3': ['HP:0000008']
        }


    def runTest(self):
        self.test_all_conds()
        self.test_all_phens()
        self.test_desc_conds()
        self.test_desc_conds_obsolete()
        self.test_desc_phens()
        self.test_desc_phens_obsolete()
        self.test_cond_phens()
        self.test_cond_phens_recursive()
        self.test_cond_phens_obsolete_show()
        self.test_cond_phens_obsolete_replace()
        self.test_cond_phens_obsolete_hide()
        self.test_describe_groups()
        self.test_group_phens()
        self.test_common_ancestor()
        self.test_phen_leaves()

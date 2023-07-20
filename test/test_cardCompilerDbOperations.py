import sys
sys.path.append("..")

import cardCompilerDbOperations
import unittest
from db_config import DATABASE_FILENAME
import dbOperations


class TestCardCompilerDbOperations(unittest.TestCase):
    def test_create_group(self):
        expected_name = "some name"
        group_id = cardCompilerDbOperations.create_group("some name")
        actual_name = dbOperations.select("group_name", "groups", 
                                          f'group_id="{group_id}"')[0][0]
        self.assertEqual(expected_name, actual_name)

    def test_register_contributer_sunny_path(self):
        # does not check password currently
        import init_db # clear the db
        expected_name = "some name"
        expected_group_id = str(cardCompilerDbOperations.create_group("some name"))
        cardCompilerDbOperations.register_contributer(expected_name, 
                                                      "fhbujse", 
                                                      expected_group_id)
        where = f'group_id="{expected_group_id}" AND contributer_name="{expected_name}"'
        actual = dbOperations.select("contributer_name,group_id",
                                     "contributers", where)
        self.assertEqual(len(actual), 1)
    
    def test_register_bad_group_id(self):
        import init_db # clear the db
        expected_name = "some name"
        expected_group_id = 24
        self.assertRaises(KeyError, cardCompilerDbOperations.register_contributer, expected_name, "fgdujnb", expected_group_id)
        where = f'group_id="{expected_group_id}" AND contributer_name="{expected_name}"'
        actual = dbOperations.select("contributer_name,group_id",
                                     "contributers", where)
        self.assertEqual(len(actual), 0)

    def test_add_card_sunny_path(self):
        import init_db # clear the db
        
        expected_card_text = "this is some card text"
        group_id = str(cardCompilerDbOperations.create_group("some name"))
        name="blah"
        cardCompilerDbOperations.register_contributer(name, 
                                                      "fhbujse", 
                                                      group_id)
        where = f'group_id="{group_id}" AND contributer_name="{name}"'
        expected_contributer_id = dbOperations.select("contributer_id",
                                     "contributers", where)[0][0]
        cardCompilerDbOperations.add_card(expected_card_text, expected_contributer_id)
        where = f'contributer_id="{expected_contributer_id}" AND card_text="{expected_card_text}"'
        actual = dbOperations.select("*", "cards", where)
        self.assertEqual(len(actual), 1)

    def test_add_card_bad_contributer_id(self):
        import init_db # clear the db
        expected_card_text = "this is some card text"
        expected_contributer_id = 24
        self.assertRaises(KeyError, cardCompilerDbOperations.add_card, expected_card_text, expected_contributer_id)
        where = f'contributer_id="{expected_contributer_id}" AND card_text="{expected_card_text}"'
        actual = dbOperations.select("*","cards", where)
        self.assertEqual(len(actual), 0)
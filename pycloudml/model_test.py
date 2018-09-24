import unittest

from pycloudml.model import Model

PROJECT_ID = "project_id"


class ModelTest(unittest.TestCase):

    def test_full_model_name_builds_full_name(self):
        model_name = "model_name"
        full_name = "projects/{}/models/{}".format(PROJECT_ID, model_name)

        self.assertEqual(Model._full_model_name(PROJECT_ID, model_name), full_name)

    def test_full_model_name_without_project_id_raises_assertion_error(self):
        model_name = "model_name"

        with self.assertRaises(AssertionError):
            Model._full_model_name(None, model_name)

    def test_full_model_name_without_model_name_raises_assertion_error(self):
        with self.assertRaises(AssertionError):
            Model._full_model_name(PROJECT_ID, None)

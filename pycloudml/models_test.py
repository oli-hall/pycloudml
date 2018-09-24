import unittest

from pycloudml.models import Models

PROJECT_ID = "project_id"


class ModelsTest(unittest.TestCase):

    def test_simplify_simplifies_full_name(self):
        model_name = "model_name"
        full_name = "projects/{}/models/{}".format(PROJECT_ID, model_name)

        self.assertEqual(Models._simplify(PROJECT_ID, full_name), model_name)

    def test_simplify_returns_simple_name_unchanged(self):
        model_name = "model_name"

        self.assertEqual(Models._simplify(PROJECT_ID, model_name), model_name)

    def test_simplify__without_project_id_raises_assertion_error(self):
        model_name = "model_name"

        with self.assertRaises(AssertionError):
            Models._simplify(None, model_name)

    def test_simplify__without_model_name_raises_assertion_error(self):
        with self.assertRaises(AssertionError):
            Models._simplify(PROJECT_ID, None)

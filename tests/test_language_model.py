import unittest
from language_model.openai_api import OpenAIAPI
from language_model.local_model_api import LocalModelAPI

class TestLanguageModel(unittest.TestCase):
    def setUp(self):
        self.openai_api = OpenAIAPI("api_key")
        self.local_model_api = LocalModelAPI("path/to/local/model")

    def test_openai_code_completion(self):
        prompt = "def hello_world():"
        completion = self.openai_api.complete_code(prompt)
        self.assertIsNotNone(completion)
        self.assertGreater(len(completion), len(prompt))

    def test_local_model_code_completion(self):
        prompt = "def hello_world():"
        completion = self.local_model_api.complete_code(prompt)
        self.assertIsNotNone(completion)
        self.assertGreater(len(completion), len(prompt))

if __name__ == '__main__':
    unittest.main()
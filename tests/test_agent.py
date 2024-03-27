import unittest
from agent.agent import AutomatedSoftwareEngineer

class TestAgent(unittest.TestCase):
    def setUp(self):
        self.agent = AutomatedSoftwareEngineer("TestAgent", [])

    def test_complete_task(self):
        task_description = "Write a function to calculate the factorial of a number"
        generated_code = self.agent.complete_task(task_description)
        self.assertIsNotNone(generated_code)
        self.assertIn("def factorial", generated_code)

    def test_reflection(self):
        generated_content = "This is a sample generated content"
        reflection = self.agent.reflect(generated_content)
        self.assertIsNotNone(reflection)
        self.assertGreater(len(reflection), 0)

if __name__ == '__main__':
    unittest.main()
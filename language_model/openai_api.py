from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class OpenAIAPI:
    def __init__(self, api_key):
        self.smart_model = "mistral"
        self.fast_model = "stablelm2"
        self.base_url="http://localhost:11434/v1"
        self.api_key="ollama"
        self.client = OpenAI(base_url=self.base_url,api_key=self.api_key)
        logger.info("OpenAI API initialized.")

    def complete_task(self, task_description):
        try:
            response = self.client.chat.completions.create(
                model=self.fast_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that completes programming tasks based on the given description and your tools provided."
                    },
                    {
                        "role": "user",
                        "content": f"Please provide the code for the following task: {task_description}"
                    }
                ],
                max_tokens=4000,
                n=1,
                stop=None,
                temperature=0.7,
            )
            completed_code = response.choices[0].message.content.strip()
            logger.info(f"Task completed: {completed_code}")
            return completed_code
        except Exception as e:
            logger.error(f"Error completing task: {e}")
            return "Error completing task."

    def complete(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.fast_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that provides information and answers questions while using tools."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=4096,
                n=1,
                stop=None,
                temperature=0.7,
            )
            completion = response.choices[0].message.content.strip()
            logger.info(f"Completion: {completion}")
            return completion
        except Exception as e:
            logger.error(f"Error generating completion: {e}")
            return "Error generating completion."
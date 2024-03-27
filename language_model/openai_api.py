from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class OpenAIAPI:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)
        logger.info("OpenAI API initialized.")

    def complete_task(self, task_description):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that completes programming tasks based on the given description."
                    },
                    {
                        "role": "user",
                        "content": f"Please provide the code for the following task: {task_description}"
                    }
                ],
                max_tokens=1000,
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
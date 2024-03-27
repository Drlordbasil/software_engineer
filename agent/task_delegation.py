import logging

logger = logging.getLogger(__name__)

class SubAgent:
    def __init__(self, name, task):
        self.name = name
        self.task = task

    def improve_code(self, code):
        logger.info(f"SubAgent {self.name} improving code for task: {self.task}")
        # Placeholder for code improvement logic
        improved_code = code + "\n# Code improved by SubAgent\n"
        return improved_code

def create_subagent(task_description):
    subagent_name = f"SubAgent_{task_description[:10]}"
    subagent = SubAgent(subagent_name, task_description)
    logger.info(f"Created SubAgent: {subagent_name}")
    return subagent
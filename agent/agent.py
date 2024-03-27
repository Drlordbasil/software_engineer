import logging
import os
import subprocess
import re
from language_model import openai_api
from browser_automation.browser import Browser

logger = logging.getLogger(__name__)

class AutomatedSoftwareEngineer:
    def __init__(self, name, tools, api_key):
        self.name = name
        self.tools = tools
        self.openai_api = openai_api.OpenAIAPI(api_key)
        self.inner_thoughts = []
        self.browser = Browser()
        self.repo_path = "agent_workspace"

    def complete_task(self, task_description):
        logger.info(f"Completing task: {task_description}")
        
        # Use OpenAI API to generate code
        generated_code = self.openai_api.complete_task(task_description)
        
        # Reflect on the task and navigate webpages if necessary
        self.reflect_and_navigate(task_description)
        
        # Save the generated code to a file
        self.save_code_to_file(generated_code, task_description)
        
        # Execute the generated code
        self.execute_code(task_description)
        
        # Commit and push changes to version control
        self.commit_and_push_changes(task_description)
        
        return generated_code

    def reflect_and_navigate(self, task_description):
        prompt = f"Based on the task '{task_description}', what webpages should be navigated to gather relevant information? Provide the URLs separated by commas."
        reflection = self.openai_api.complete(prompt)
        logger.info(f"Reflection: {reflection}")
        self.inner_thoughts.append(reflection)
        
        urls = [url.strip() for url in reflection.split(",")]
        for url in urls:
            if url.startswith("http://") or url.startswith("https://"):
                try:
                    self.browser.navigate(url)
                    logger.info(f"Navigated to: {url}")
                except Exception as e:
                    logger.error(f"Error navigating to URL: {url}. Error: {e}")
            else:
                logger.warning(f"Invalid URL: {url}. Skipping navigation.")

    def save_code_to_file(self, generated_code, task_description):
        # Create the agent workspace directory if it doesn't exist
        os.makedirs(self.repo_path, exist_ok=True)
        
        # Generate a file name based on the task description
        file_name = re.sub(r'[^\w\-_\. ]', '_', task_description.lower())
        file_name = '_'.join(file_name.split())
        file_path = os.path.join(self.repo_path, f"{file_name}.py")
        
        # Save the generated code to the file
        with open(file_path, "w") as file:
            file.write(generated_code)
        
        logger.info(f"Generated code saved to: {file_path}")

    def execute_code(self, task_description):
        # Generate a file name based on the task description
        file_name = re.sub(r'[^\w\-_\. ]', '_', task_description.lower())
        file_name = '_'.join(file_name.split())
        file_path = os.path.join(self.repo_path, f"{file_name}.py")
        
        try:
            # Execute the generated code
            subprocess.run(["python", file_path], check=True)
            logger.info(f"Executed code: {file_path}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error executing code: {file_path}. Error: {e}")

    def commit_and_push_changes(self, task_description):
        try:
            # Stage all changes
            subprocess.run(["git", "add", "."], cwd=self.repo_path, check=True)
            
            # Commit changes with a descriptive message
            commit_message = f"Implement task: {task_description}"
            subprocess.run(["git", "commit", "-m", commit_message], cwd=self.repo_path, check=True)
            
            # Push changes to the remote repository
            subprocess.run(["git", "push"], cwd=self.repo_path, check=True)
            
            logger.info("Changes committed and pushed to version control.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error committing and pushing changes. Error: {e}")

    def quit(self):
        self.browser.quit()